"""
Module 2: Knowledge Representation
File: neo4j_manager.py
Purpose: Neo4j graph database manager supporting node/edge batching, indexes, and queries.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
try:
    from .config import Module2Config
    from .exceptions import Neo4jConnectionError
    from .utils import logger, chunk_iterable
except (ImportError, ValueError):
    try:
        from config import Module2Config
    except (ImportError, AttributeError):
        import importlib.util
        _cfg_path = Path(__file__).resolve().parent / "config.py"
        _spec = importlib.util.spec_from_file_location("module2_config", _cfg_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        Module2Config = _mod.Module2Config
    try:
        from exceptions import Neo4jConnectionError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module2_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        Neo4jConnectionError = getattr(_mod, "Neo4jConnectionError")
    try:
        from utils import logger, chunk_iterable
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")
        chunk_iterable = getattr(_mod, "chunk_iterable")



class Neo4jManager:
    """Manages connection, constraints, batch write transactions, and Cypher queries in Neo4j.

    Attributes:
        uri (str): Neo4j bolt URI.
        username (str): Database username.
        password (str): Database password.
        driver (Any): Neo4j Driver object.
    """

    def __init__(
        self,
        uri: str = Module2Config.NEO4J_URI,
        username: str = Module2Config.NEO4J_USERNAME,
        password: str = Module2Config.NEO4J_PASSWORD
    ) -> None:
        """Initialize Neo4jManager with connection credentials.

        Args:
            uri (str): Neo4j connection bolt URL.
            username (str): Username.
            password (str): Password.
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None
        self._fallback_mode = False
        self._init_connection()

    def _init_connection(self) -> None:
        """Connect to Neo4j database and create initial indexes."""
        try:
            from neo4j import GraphDatabase
            logger.info(f"Connecting to Neo4j database at: {self.uri}")
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j.")
            self._create_indexes()
        except Exception as e:
            logger.warning(f"Could not connect to Neo4j database ({e}). Operating in lightweight graph fallback mode.")
            self._driver = None
            self._fallback_mode = True
            self._init_fallback_graph()

    def _init_fallback_graph(self) -> None:
        """Initialize in-memory fallback graph store."""
        self.nodes = {}  # (type, id) -> properties
        self.edges = []  # dict of edge properties

    def _create_indexes(self) -> None:
        """Create Cypher database indexes for fast query execution."""
        index_queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (k:Keyword) REQUIRE k.name IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (e:Entity) ON (e.label)"
        ]
        try:
            with self.driver.session() as session:
                for q in index_queries:
                    session.run(q)
            logger.info("Neo4j constraints and indexes verified.")
        except Exception as e:
            logger.warning(f"Failed to create Neo4j indexes: {e}")

    def batch_insert_graph_data(self, relationships_dict: Dict[str, List[Dict[str, Any]]]) -> None:
        """Insert nodes and relationships into Neo4j in batch transactions.

        Args:
            relationships_dict (Dict[str, List[Dict[str, Any]]]): Dictionary of relationships by type.

        Raises:
            Neo4jConnectionError: If Cypher execution fails.
        """
        if self._fallback_mode:
            self._fallback_batch_insert(relationships_dict)
            return

        try:
            with self.driver.session() as session:
                # 1. Batch Insert CONTAINS (Document -> Chunk)
                contains_list = relationships_dict.get("CONTAINS", [])
                if contains_list:
                    cypher = """
                    UNWIND $batch AS row
                    MERGE (d:Document {id: row.source_id})
                    MERGE (c:Chunk {id: row.target_id})
                    MERGE (d)-[:CONTAINS]->(c)
                    """
                    session.run(cypher, batch=contains_list)

                # 2. Batch Insert MENTIONS (Chunk -> Entity)
                mentions_list = relationships_dict.get("MENTIONS", [])
                if mentions_list:
                    cypher = """
                    UNWIND $batch AS row
                    MERGE (c:Chunk {id: row.source_id})
                    MERGE (e:Entity {name: row.target_id})
                    ON CREATE SET e.label = row.entity_label
                    MERGE (c)-[:MENTIONS]->(e)
                    """
                    session.run(cypher, batch=mentions_list)

                # 3. Batch Insert RELATED_TO (Entity -> Entity)
                related_list = relationships_dict.get("RELATED_TO", [])
                if related_list:
                    cypher = """
                    UNWIND $batch AS row
                    MERGE (e1:Entity {name: row.source_id})
                    MERGE (e2:Entity {name: row.target_id})
                    MERGE (e1)-[r:RELATED_TO]->(e2)
                    ON CREATE SET r.weight = row.weight, r.context_chunk = row.context_chunk
                    ON MATCH SET r.weight = r.weight + 1.0
                    """
                    session.run(cypher, batch=related_list)

                # 4. Batch Insert BELONGS_TO (Chunk -> Topic)
                belongs_list = relationships_dict.get("BELONGS_TO", [])
                if belongs_list:
                    cypher = """
                    UNWIND $batch AS row
                    MERGE (c:Chunk {id: row.source_id})
                    MERGE (t:Topic {name: row.target_id})
                    MERGE (c)-[:BELONGS_TO]->(t)
                    """
                    session.run(cypher, batch=belongs_list)

                # 5. Batch Insert HAS_KEYWORD (Chunk -> Keyword)
                keyword_list = relationships_dict.get("HAS_KEYWORD", [])
                if keyword_list:
                    cypher = """
                    UNWIND $batch AS row
                    MERGE (c:Chunk {id: row.source_id})
                    MERGE (k:Keyword {name: row.target_id})
                    MERGE (c)-[:HAS_KEYWORD]->(k)
                    """
                    session.run(cypher, batch=keyword_list)

            logger.info("Successfully completed Neo4j batch insertion.")
        except Exception as e:
            logger.error(f"Neo4j batch insertion error: {e}")
            raise Neo4jConnectionError(f"Neo4j batch execution error: {e}") from e

    def query_subgraph(self, entity_names: List[str], max_depth: int = 2) -> Dict[str, Any]:
        """Retrieve 1-hop and 2-hop subgraphs for given entities.

        Args:
            entity_names (List[str]): List of query entity names.
            max_depth (int): Traversal depth.

        Returns:
            Dict[str, Any]: Graph dictionary containing nodes and relationships.
        """
        if self._fallback_mode:
            return self._fallback_query_subgraph(entity_names)

        query = """
        MATCH (e:Entity) WHERE e.name IN $entity_names
        OPTIONAL MATCH (e)-[r:RELATED_TO|MENTIONS|BELONGS_TO|CONTAINS]-(target)
        RETURN e.name AS source, labels(e)[0] AS source_label,
               type(r) AS relationship,
               coalesce(target.name, target.id) AS target,
               labels(target)[0] AS target_label
        LIMIT 50
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, entity_names=entity_names)
                nodes = []
                edges = []
                seen_nodes = set()

                for record in result:
                    src = record["source"]
                    tgt = record["target"]
                    rel = record["relationship"]

                    if src and src not in seen_nodes:
                        seen_nodes.add(src)
                        nodes.append({"id": src, "label": record["source_label"] or "Entity"})

                    if tgt and tgt not in seen_nodes:
                        seen_nodes.add(tgt)
                        nodes.append({"id": tgt, "label": record["target_label"] or "Node"})

                    if src and tgt and rel:
                        edges.append({"source": src, "target": tgt, "relationship": rel})

                return {"nodes": nodes, "edges": edges}
        except Exception as e:
            logger.error(f"Failed to query Neo4j subgraph: {e}")
            return {"nodes": [], "edges": []}

    def _fallback_batch_insert(self, relationships_dict: Dict[str, List[Dict[str, Any]]]) -> None:
        """Store nodes and edges in memory when Neo4j is offline."""
        for rel_type, rel_list in relationships_dict.items():
            for item in rel_list:
                src_key = (item["source_type"], item["source_id"])
                tgt_key = (item["target_type"], item["target_id"])

                self.nodes[src_key] = {"type": item["source_type"], "id": item["source_id"]}
                self.nodes[tgt_key] = {"type": item["target_type"], "id": item["target_id"]}

                self.edges.append({
                    "source": item["source_id"],
                    "target": item["target_id"],
                    "relationship": rel_type
                })
        logger.info(f"Fallback graph now contains {len(self.nodes)} nodes and {len(self.edges)} edges.")

    def _fallback_query_subgraph(self, entity_names: List[str]) -> Dict[str, Any]:
        """Perform fallback memory graph search."""
        matched_nodes = [
            {"id": node_id, "label": ntype}
            for (ntype, node_id) in self.nodes.keys()
            if any(name.lower() in node_id.lower() for name in entity_names)
        ]
        matched_ids = {n["id"] for n in matched_nodes}
        matched_edges = [
            e for e in self.edges
            if e["source"] in matched_ids or e["target"] in matched_ids
        ]
        return {"nodes": matched_nodes, "edges": matched_edges}

    def close(self) -> None:
        """Close Neo4j connection driver."""
        if self.driver:
            self.driver.close()


if __name__ == "__main__":
    manager = Neo4jManager()
    print("Neo4jManager initialized. Fallback mode:", manager._fallback_mode)
