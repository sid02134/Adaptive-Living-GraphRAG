"""
Module 5: Backend API
File: models.py
Purpose: Pydantic request and response models for API validation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# ----------------------------------------------------
# 1. Health API Models
# ----------------------------------------------------
class ComponentStatus(BaseModel):
    status: str = Field(..., description="Status string (online / offline / degraded)")
    details: Optional[str] = Field(None, description="Detailed component description")


class HealthResponse(BaseModel):
    status: str = Field("healthy", description="Overall system health status")
    api_version: str = Field("/api/v1", description="API version")
    components: Dict[str, ComponentStatus] = Field(..., description="Health status of components")


# ----------------------------------------------------
# 2. Upload API Models
# ----------------------------------------------------
class UploadResponse(BaseModel):
    status: str = Field(..., description="Processing status (success / error)")
    filename: str = Field(..., description="Uploaded PDF filename")
    chunks_processed: int = Field(..., description="Number of text chunks created")
    entities_extracted: int = Field(..., description="Number of entities extracted")
    graph_building_summary: Dict[str, Any] = Field(..., description="Summary of graph relationship construction")


# ----------------------------------------------------
# 3. Chat / Query API Models
# ----------------------------------------------------
class AskRequest(BaseModel):
    query: str = Field(..., min_length=2, description="User question string")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Top-K context chunks to retrieve")
    alpha: Optional[float] = Field(0.6, ge=0.0, le=1.0, description="Hybrid vector score weight alpha")


class TrustBreakdown(BaseModel):
    semantic_similarity: float = Field(..., description="Semantic similarity score percentage")
    source_reliability: float = Field(..., description="Source reliability score percentage")
    graph_consistency: float = Field(..., description="Graph consistency score percentage")
    citation_coverage: float = Field(..., description="Citation coverage score percentage")


class SourceCitation(BaseModel):
    citation_id: str = Field(..., description="Citation identifier (e.g. [1])")
    source_file: str = Field(..., description="Source PDF document filename")
    chunk_id: str = Field(..., description="Chunk ID string")
    relevance_score: float = Field(..., description="Hybrid relevance score")
    formatted_citation: str = Field(..., description="Formatted inline citation string")


class AskResponse(BaseModel):
    query: str = Field(..., description="Original query text")
    answer: str = Field(..., description="Generated text answer")
    markdown_response: str = Field(..., description="Complete GitHub Markdown response")
    trust_score: float = Field(..., description="Overall Trust score [0.0 - 1.0]")
    trust_percentage: float = Field(..., description="Trust score percentage")
    confidence_level: str = Field(..., description="Confidence rating text")
    trust_breakdown: TrustBreakdown = Field(..., description="4-tier metric breakdown")
    citations: List[SourceCitation] = Field(default_factory=list, description="Verified source citations")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Ranked context sources")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


# ----------------------------------------------------
# 4. Graph API Models
# ----------------------------------------------------
class GraphNode(BaseModel):
    id: str = Field(..., description="Node unique ID or name")
    label: str = Field("Entity", description="Node label/category")


class GraphEdge(BaseModel):
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    relationship: str = Field(..., description="Edge relationship type")


class GraphResponse(BaseModel):
    total_nodes: int = Field(..., description="Total nodes count")
    total_edges: int = Field(..., description="Total edges count")
    nodes: List[GraphNode] = Field(..., description="List of graph nodes")
    edges: List[GraphEdge] = Field(..., description="List of graph edges")


# ----------------------------------------------------
# 5. Dashboard & Trust API Models
# ----------------------------------------------------
class DashboardResponse(BaseModel):
    total_documents: int = Field(..., description="Total PDF documents ingested")
    total_chunks: int = Field(..., description="Total text chunks in ChromaDB")
    total_entities: int = Field(..., description="Total entities in Neo4j")
    total_relationships: int = Field(..., description="Total edges in Neo4j")
    queries_processed: int = Field(..., description="Total user chat queries processed")
    avg_trust_score: float = Field(..., description="Average trust score percentage")
    avg_processing_time_ms: float = Field(..., description="Average processing speed in ms")


# ----------------------------------------------------
# 6. Settings Models
# ----------------------------------------------------
class SettingsUpdateRequest(BaseModel):
    chunk_size: Optional[int] = Field(500, description="Chunk character size")
    chunk_overlap: Optional[int] = Field(100, description="Chunk overlap size")
    top_k: Optional[int] = Field(5, description="Default Top-K retrieval count")
    temperature: Optional[float] = Field(0.2, description="LLM sampling temperature")
    embedding_model: Optional[str] = Field("all-MiniLM-L6-v2", description="Embedding model name")
    llm_model: Optional[str] = Field("llama3", description="LLM model name")
    neo4j_uri: Optional[str] = Field("bolt://localhost:7687", description="Neo4j URI")
    ollama_url: Optional[str] = Field("http://localhost:11434", description="Ollama base URL")
