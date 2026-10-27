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
        import sys
        from pathlib import Path
        import importlib.util
        if "Module-5_Backend_API.config" in sys.modules:
            Module5Config = sys.modules["Module-5_Backend_API.config"].Module5Config
        else:
            _cfg_path = Path(__file__).resolve().parent / "config.py"
            _spec = importlib.util.spec_from_file_location("Module-5_Backend_API.config", _cfg_path)
            _mod = importlib.util.module_from_spec(_spec)
            sys.modules["Module-5_Backend_API.config"] = _mod
            _spec.loader.exec_module(_mod)
            Module5Config = _mod.Module5Config
        from app import app
        from routes import api_v1_router

__all__ = [
    "Module5Config",
    "app",
    "api_v1_router"
]
