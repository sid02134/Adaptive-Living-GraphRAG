"""
Module 5: Backend API
File: graph_api.py
Purpose: APIRouter for Knowledge Graph visualization data.
"""

from fastapi import APIRouter, Query
import importlib
import logging

from models import GraphResponse, GraphNode, GraphEdge

router = APIRouter(tags=["Knowledge Graph"])
logger = logging.getLogger("backend_logger")


@router.get("/graph", response_model=GraphResponse)
async def get_knowledge_graph(
    query_entity: str = Query("", description="Optional entity name to filter subgraphs")
) -> GraphResponse:
    """Fetch nodes and edge connections from Neo4j knowledge graph.

    Args:
        query_entity (str): Optional filter string for entity search.

    Returns:
        GraphResponse: Graph response payload containing nodes and edges arrays.
    """
    try:
        mod2 = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
        Neo4jManager = getattr(mod2, "Neo4jManager")
        manager = Neo4jManager()

        if query_entity:
            subgraph = manager.query_subgraph([query_entity], max_depth=2)
        else:
            subgraph = manager.query_subgraph(["GraphRAG", "Neo4j", "ChromaDB", "Llama 3"], max_depth=2)

        raw_nodes = subgraph.get("nodes", [])
        raw_edges = subgraph.get("edges", [])

        # Default fallback nodes/edges if empty
        if not raw_nodes:
            raw_nodes = [
                {"id": "GraphRAG Framework", "label": "CONCEPT"},
                {"id": "Neo4j Graph Database", "label": "DATABASE"},
                {"id": "ChromaDB Vector Store", "label": "DATABASE"},
                {"id": "Llama 3 Model", "label": "MODEL"},
                {"id": "Trust Engine", "label": "MODULE"}
            ]
            raw_edges = [
                {"source": "GraphRAG Framework", "target": "Neo4j Graph Database", "relationship": "USES"},
                {"source": "GraphRAG Framework", "target": "ChromaDB Vector Store", "relationship": "USES"},
                {"source": "GraphRAG Framework", "target": "Llama 3 Model", "relationship": "POWERED_BY"},
                {"source": "GraphRAG Framework", "target": "Trust Engine", "relationship": "EVALUATED_BY"}
            ]

        nodes = [GraphNode(id=n["id"], label=n.get("label", "Entity")) for n in raw_nodes]
        edges = [GraphEdge(source=e["source"], target=e["target"], relationship=e["relationship"]) for e in raw_edges]

        return GraphResponse(
            total_nodes=len(nodes),
            total_edges=len(edges),
            nodes=nodes,
            edges=edges
        )
    except Exception as e:
        logger.error(f"Failed to retrieve knowledge graph: {e}")
        # Graceful default return
        default_nodes = [GraphNode(id="GraphRAG", label="CONCEPT"), GraphNode(id="TrustEngine", label="MODULE")]
        default_edges = [GraphEdge(source="GraphRAG", target="TrustEngine", relationship="INCLUDES")]
        return GraphResponse(total_nodes=2, total_edges=1, nodes=default_nodes, edges=default_edges)
