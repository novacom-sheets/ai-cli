"""Plugin manager with auto-discovery and lifecycle management."""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

from .plugins import Plugin, PluginRegistry, get_global_registry


class PluginManager:
    """
    Manages plugin lifecycle, discovery, and configuration.

    Supports:
    - Auto-discovery from plugins directory
    - Plugin configuration loading
    - Hook integration with core components
    """

    def __init__(
        self,
        plugins_dir: Optional[Path] = None,
        config_path: Optional[Path] = None,
        registry: Optional[PluginRegistry] = None
    ):
        self.plugins_dir = plugins_dir or Path.home() / ".ai-cli" / "plugins"
        self.config_path = config_path or Path.home() / ".ai-cli" / "plugins.json"
        self.registry = registry or get_global_registry()
        self._plugin_configs: Dict[str, Dict[str, Any]] = {}

    def load_config(self):
        """Load plugin configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self._plugin_configs = json.load(f)

    def save_config(self):
        """Save plugin configuration to JSON file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self._plugin_configs, f, indent=2)

    def discover_plugins(self) -> List[str]:
        """
        Auto-discover plugins from plugins directory.

        Returns:
            List of discovered plugin module names
        """
        if not self.plugins_dir.exists():
            return []

        discovered = []
        for path in self.plugins_dir.glob("*.py"):
            if path.stem.startswith("_"):
                continue

            module_name = f"ai_cli_plugin_{path.stem}"
            discovered.append(module_name)

            # Load module dynamically
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

        return discovered

    def register_plugin(
        self,
        plugin: Plugin,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Register a plugin with optional configuration.

        Args:
            plugin: Plugin instance
            config: Plugin-specific configuration
        """
        plugin_name = plugin.get_name()

        # Merge with saved config
        if config:
            self._plugin_configs[plugin_name] = config
        elif plugin_name in self._plugin_configs:
            # Apply saved config to plugin
            for key, value in self._plugin_configs[plugin_name].items():
                if hasattr(plugin.config, key):
                    setattr(plugin.config, key, value)

        self.registry.register(plugin)

    async def initialize_all(self):
        """Initialize all registered plugins."""
        await self.registry.initialize_all()

    async def shutdown_all(self):
        """Shutdown all plugins."""
        await self.registry.shutdown_all()

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self.registry.get_plugin(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        List all plugins with their info.

        Returns:
            List of plugin info dicts
        """
        plugins_info = []
        for name in self.registry.list_plugins():
            plugin = self.registry.get_plugin(name)
            if plugin:
                plugins_info.append({
                    "name": plugin.get_name(),
                    "version": plugin.get_version(),
                    "enabled": plugin.config.enabled,
                    "priority": plugin.config.priority,
                })
        return plugins_info

    def enable_plugin(self, name: str):
        """Enable a plugin."""
        plugin = self.registry.get_plugin(name)
        if plugin:
            plugin.config.enabled = True
            if name not in self._plugin_configs:
                self._plugin_configs[name] = {}
            self._plugin_configs[name]["enabled"] = True
            self.save_config()

    def disable_plugin(self, name: str):
        """Disable a plugin."""
        plugin = self.registry.get_plugin(name)
        if plugin:
            plugin.config.enabled = False
            if name not in self._plugin_configs:
                self._plugin_configs[name] = {}
            self._plugin_configs[name]["enabled"] = False
            self.save_config()

    def set_plugin_priority(self, name: str, priority: int):
        """Set plugin execution priority."""
        plugin = self.registry.get_plugin(name)
        if plugin:
            plugin.config.priority = priority
            if name not in self._plugin_configs:
                self._plugin_configs[name] = {}
            self._plugin_configs[name]["priority"] = priority
            self.save_config()

    async def process_agent_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent config through all plugins."""
        return await self.registry.execute_hook("agent_init", config)

    async def process_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process generate request through all plugins."""
        return await self.registry.execute_hook("generate_request", request)

    async def process_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process generate response through all plugins."""
        return await self.registry.execute_hook("generate_response", response)

    async def process_chat_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process chat message through all plugins."""
        return await self.registry.execute_hook("chat_message", message)


# Global plugin manager instance
_global_manager: Optional[PluginManager] = None


def get_global_manager() -> PluginManager:
    """Get or create global plugin manager."""
    global _global_manager
    if _global_manager is None:
        _global_manager = PluginManager()
        _global_manager.load_config()
    return _global_manager
