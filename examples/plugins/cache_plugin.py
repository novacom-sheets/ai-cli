"""Example: Cache plugin that caches AI responses."""

import hashlib
import json
from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import Field

from ai_cli.plugins import Plugin, PluginConfig


class CachePluginConfig(PluginConfig):
    """Configuration for cache plugin."""
    cache_dir: str = Field(default="~/.ai-cli/cache", description="Cache directory")
    max_cache_size: int = Field(default=1000, description="Maximum cached items")
    ttl_seconds: int = Field(default=3600, description="Cache TTL in seconds")


class CachePlugin(Plugin):
    """
    Plugin that caches AI responses to avoid redundant API calls.

    Features:
    - Caches responses by prompt hash
    - Configurable TTL and cache size
    - Disk-based persistence
    """

    def __init__(self, config: CachePluginConfig = None):
        super().__init__(config or CachePluginConfig())
        self.config: CachePluginConfig
        self.cache_dir = Path(self.config.cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_name(self) -> str:
        return "cache"

    def get_version(self) -> str:
        return "1.0.0"

    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        """Add cache control fields."""
        return {
            "GenerateRequest": {
                "use_cache": (bool, Field(default=True, description="Use cached response if available")),
                "cache_key": (str, Field(default="", description="Custom cache key")),
            },
            "GenerateResponse": {
                "from_cache": (bool, Field(default=False, description="Response was from cache")),
                "cache_key": (str, Field(default="", description="Cache key used")),
            }
        }

    def _get_cache_key(self, request: Dict[str, Any]) -> str:
        """Generate cache key from request."""
        # Use custom cache key if provided
        if request.get("cache_key"):
            return request["cache_key"]

        # Generate hash from model + prompt + system
        key_data = {
            "model": request.get("model"),
            "prompt": request.get("prompt"),
            "system": request.get("system"),
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if available."""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)

            # Check TTL
            import time
            if time.time() - cached.get("timestamp", 0) > self.config.ttl_seconds:
                cache_file.unlink()
                return None

            return cached.get("response")

        except Exception:
            return None

    def _save_to_cache(self, cache_key: str, response: Dict[str, Any]):
        """Save response to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            import time
            cached = {
                "timestamp": time.time(),
                "response": response
            }

            with open(cache_file, 'w') as f:
                json.dump(cached, f)

        except Exception:
            pass

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check cache before making request."""
        if not request.get("use_cache", True):
            return request

        cache_key = self._get_cache_key(request)
        request["cache_key"] = cache_key

        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            # Mark that we have cached response
            request["_cached_response"] = cached_response

        return request

    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Save response to cache."""
        cache_key = response.get("cache_key")

        if cache_key:
            # Save to cache
            self._save_to_cache(cache_key, response)
            response["from_cache"] = False

        return response


# Example usage
if __name__ == "__main__":
    from ai_cli.plugin_manager import get_global_manager

    # Create and register plugin
    config = CachePluginConfig(ttl_seconds=3600, max_cache_size=1000)
    plugin = CachePlugin(config)

    manager = get_global_manager()
    manager.register_plugin(plugin)

    print(f"Registered plugin: {plugin.get_name()} v{plugin.get_version()}")
    print(f"Cache directory: {plugin.cache_dir}")
