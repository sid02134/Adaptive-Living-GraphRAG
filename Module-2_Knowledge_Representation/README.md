# Module 2: Knowledge Representation

## Purpose
Module 2 handles the transformation of cleaned document chunks (output from Module 1) into dense vector embeddings stored in ChromaDB and structured graph nodes/relationships stored in Neo4j.

---

## Workflow Architecture

```
Module 1 Output (Processed Documents)
               │
               ▼
┌──────────────────────────────┐
│     GraphBuilder Pipeline    │
└──────────────┬───────────────┘
               │
       ┌───────┴─────────────────────────────────────────┐
       ▼                                                 ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  EmbeddingGenerator          │        │  EntityExtractor (spaCy)     │
│  (all-MiniLM-L6-v2)          │        │  & RelationshipBuilder       │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               ▼                                         ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  ChromaManager               │        │  Neo4jManager                │
│  (ChromaDB Vector Store)     │        │  (Graph DB Batch Insert)     │
└──────────────────────────────┘        └──────────────────────────────┘
```

---

## Graph Schema

### Node Labels
- **`Document`**: Source PDF document (`id`)
- **`Chunk`**: Document chunk string (`id`)
- **`Entity`**: Extracted named entity (`name`, `label`)
- **`Topic`**: High-level domain topic (`name`)
- **`Keyword`**: Key technical term (`name`)

### Relationships
- `(Document)-[:CONTAINS]->(Chunk)`
- `(Chunk)-[:MENTIONS]->(Entity)`
- `(Entity)-[:RELATED_TO {weight, context_chunk}]->(Entity)`
- `(Chunk)-[:BELONGS_TO]->(Topic)`
- `(Chunk)-[:HAS_KEYWORD]->(Keyword)`

---

## Class & Method Index

### 1. `EmbeddingGenerator` (`embedding_generator.py`)
- `generate_embeddings(texts: Union[str, List[str]]) -> List[List[float]]`: Generates 384-dimensional dense vectors using SentenceTransformer.
- `generate_single_embedding(text: str) -> List[float]`: Returns vector for a single text.

### 2. `ChromaManager` (`chroma_manager.py`)
- `add_chunks(chunks, embeddings, metadatas, ids) -> List[str]`: Persists vector chunks and metadata into ChromaDB.
- `query_similarity(query_embedding, n_results=5) -> List[Dict]`: Executes vector similarity search.
- `get_stats() -> Dict`: Returns count of stored vectors and collection status.

### 3. `EntityExtractor` (`entity_extractor.py`)
- `extract_entities(text: str) -> List[Dict]`: Extracts named entities (PERSON, ORG, GPE, DATE, CONCEPT) using spaCy.
- `extract_keywords(text: str, max_keywords=8) -> List[str]`: Extracts key nouns and technical terms.
- `extract_topics(text: str) -> List[str]`: Categorizes chunk into high-level domain topics.

### 4. `RelationshipBuilder` (`relationship_builder.py`)
- `build_chunk_relationships(doc_name, chunk_id, chunk_text, entities, topics, keywords) -> Dict`: Constructs structured node-link dictionary matching schema.

### 5. `Neo4jManager` (`neo4j_manager.py`)
- `batch_insert_graph_data(relationships_dict) -> None`: Inserts nodes and relationships using Neo4j Cypher batching.
- `query_subgraph(entity_names, max_depth=2) -> Dict`: Returns 1-hop and 2-hop subgraphs.

### 6. `GraphBuilder` (`graph_builder.py`)
- `build_knowledge_graph(processed_documents) -> Dict`: Complete pipeline connecting Module 1 output with ChromaDB and Neo4j.

---

## Testing & Execution

Run standalone module unit and integration tests:
```bash
python Module-2_Knowledge_Representation/test_module2.py
```
