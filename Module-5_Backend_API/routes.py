"""
Module 5: Backend API
File: routes.py
Purpose: Route aggregator registering all APIRouters under /api/v1.
"""

from fastapi import APIRouter

try:
    from .health_api import router as health_router
    from .upload_api import router as upload_router
    from .chat_api import router as chat_router
    from .graph_api import router as graph_router
    from .trust_api import router as trust_router
    from .evolution_api import router as evolution_router
except (ImportError, ValueError):
    from health_api import router as health_router
    from upload_api import router as upload_router
    from chat_api import router as chat_router
    from graph_api import router as graph_router
    from trust_api import router as trust_router
    from evolution_api import router as evolution_router


api_v1_router = APIRouter(prefix="/api/v1")

# Register Routers
api_v1_router.include_router(health_router)
api_v1_router.include_router(upload_router)
api_v1_router.include_router(chat_router)
api_v1_router.include_router(graph_router)
api_v1_router.include_router(trust_router)
api_v1_router.include_router(evolution_router)

