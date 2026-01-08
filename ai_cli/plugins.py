"""Plugin system for extensible AI CLI."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, List, Callable
from pydantic import BaseModel, Field


class PluginConfig(BaseModel):
    """Base plugin configuration that can be extended."""
    enabled: bool = Field(default=True, description="Whether plugin is enabled")
    priority: int = Field(default=0, description="Plugin execution priority (higher = earlier)")

    model_config = {"extra": "allow"}  # Allow arbitrary fields from plugins


class Plugin(ABC):
    """
    Base plugin interface.

    Plugins can extend AI CLI with new parameters, hooks, and functionality.
    """

    def __init__(self, config: Optional[PluginConfig] = None):
        self.config = config or PluginConfig()
        self._hooks: Dict[str, List[Callable]] = {}

    @abstractmethod
    def get_name(self) -> str:
        """Return unique plugin name."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Return plugin version."""
        pass

    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        """
        Return field extensions for base models.

        Returns:
            Dict mapping model names to field definitions.
            Example:
            {
                "AgentConfig": {
                    "my_field": (str, Field(default="value", description="..."))
                },
                "GenerateRequest": {
                    "custom_param": (int, Field(default=10))
                }
            }
        """
        return {}

    def on_agent_init(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called when agent is initialized.
        Can modify agent configuration.
        """
        return agent_config

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called before generation request.
        Can modify request parameters.
        """
        return request

    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called after generation response.
        Can modify or process response.
        """
        return response

    def on_chat_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called for each chat message.
        Can modify or filter messages.
        """
        return message

    async def initialize(self):
        """Initialize plugin resources."""
        pass

    async def shutdown(self):
        """Cleanup plugin resources."""
        pass


class PluginRegistry:
    """
    Central registry for managing plugins.

    Allows dynamic registration and execution of plugins.
    """

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._schema_extensions: Dict[str, Dict[str, Any]] = {}
        self._hooks: Dict[str, List[tuple[int, Plugin]]] = {
            "agent_init": [],
            "generate_request": [],
            "generate_response": [],
            "chat_message": [],
        }

    def register(self, plugin: Plugin):
        """
        Register a plugin.

        Args:
            plugin: Plugin instance to register
        """
        name = plugin.get_name()

        if name in self._plugins:
            raise ValueError(f"Plugin {name} already registered")

        self._plugins[name] = plugin

        # Register schema extensions
        extensions = plugin.get_schema_extensions()
        for model_name, fields in extensions.items():
            if model_name not in self._schema_extensions:
                self._schema_extensions[model_name] = {}
            self._schema_extensions[model_name].update(fields)

        # Register hooks (sorted by priority)
        priority = plugin.config.priority
        for hook_name in self._hooks.keys():
            self._hooks[hook_name].append((priority, plugin))
            self._hooks[hook_name].sort(key=lambda x: -x[0])  # Higher priority first

    def unregister(self, plugin_name: str):
        """Unregister a plugin."""
        if plugin_name in self._plugins:
            plugin = self._plugins.pop(plugin_name)

            # Remove from hooks
            for hook_list in self._hooks.values():
                hook_list[:] = [(p, pl) for p, pl in hook_list if pl != plugin]

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        return list(self._plugins.keys())

    def get_schema_extensions(self, model_name: str) -> Dict[str, Any]:
        """Get all schema extensions for a model."""
        return self._schema_extensions.get(model_name, {})

    async def execute_hook(self, hook_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all plugins for a specific hook.

        Args:
            hook_name: Name of hook to execute
            data: Data to pass through plugins

        Returns:
            Modified data after all plugins processed it
        """
        if hook_name not in self._hooks:
            return data

        result = data
        for priority, plugin in self._hooks[hook_name]:
            if not plugin.config.enabled:
                continue

            if hook_name == "agent_init":
                result = plugin.on_agent_init(result)
            elif hook_name == "generate_request":
                result = plugin.on_generate_request(result)
            elif hook_name == "generate_response":
                result = plugin.on_generate_response(result)
            elif hook_name == "chat_message":
                result = plugin.on_chat_message(result)

        return result

    async def initialize_all(self):
        """Initialize all registered plugins."""
        for plugin in self._plugins.values():
            if plugin.config.enabled:
                await plugin.initialize()

    async def shutdown_all(self):
        """Shutdown all plugins."""
        for plugin in self._plugins.values():
            try:
                await plugin.shutdown()
            except Exception as e:
                print(f"Error shutting down plugin {plugin.get_name()}: {e}")


# Global plugin registry instance
_global_registry: Optional[PluginRegistry] = None


def get_global_registry() -> PluginRegistry:
    """Get or create global plugin registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PluginRegistry()
    return _global_registry


def register_plugin(plugin: Plugin):
    """Register plugin in global registry."""
    registry = get_global_registry()
    registry.register(plugin)
