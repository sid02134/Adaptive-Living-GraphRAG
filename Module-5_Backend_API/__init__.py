"""
Module 5: Backend API Package
"""

import importlib

try:
    from .config import Module5Config
    from .app import app
    from .routes import api_v1_router
except (ImportError, ValueError):
    try:
        mod_cfg = importlib.import_module("Module-5_Backend_API.config")
        Module5Config = getattr(mod_cfg, "Module5Config")
        mod_app = importlib.import_module("Module-5_Backend_API.app")
        app = getattr(mod_app, "app")
        mod_routes = importlib.import_module("Module-5_Backend_API.routes")
        api_v1_router = getattr(mod_routes, "api_v1_router")
    except Exception:
        from config import Module5Config
        from app import app
        from routes import api_v1_router

__all__ = [
    "Module5Config",
    "app",
    "api_v1_router"
]
