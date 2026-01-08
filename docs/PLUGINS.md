# Plugin System Documentation

AI CLI features a powerful plugin system that allows you to extend functionality by adding new parameters, hooks, and features without modifying the core codebase.

## Quick Start

### Creating a Simple Plugin

```python
from ai_cli.plugins import Plugin, PluginConfig
from pydantic import Field
from typing import Dict, Any

class MyPluginConfig(PluginConfig):
    """Your plugin configuration."""
    my_setting: str = Field(default="value", description="A custom setting")

class MyPlugin(Plugin):
    """Your custom plugin."""

    def __init__(self, config: MyPluginConfig = None):
        super().__init__(config or MyPluginConfig())
        self.config: MyPluginConfig

    def get_name(self) -> str:
        return "my_plugin"

    def get_version(self) -> str:
        return "1.0.0"

    # Add custom fields to existing models
    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        return {
            "AgentConfig": {
                "my_param": (int, Field(default=10, description="My parameter"))
            }
        }

    # Hook into request processing
    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Modify request before it's sent
        print(f"Processing request with {self.config.my_setting}")
        return request
```

### Registering a Plugin

```python
from ai_cli.plugin_manager import get_global_manager

# Create plugin instance
plugin = MyPlugin()

# Register with manager
manager = get_global_manager()
manager.register_plugin(plugin)

# Initialize
await manager.initialize_all()
```

## Core Concepts

### 1. Schema Extensions

Plugins can add new fields to existing Pydantic models:

```python
def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
    return {
        "AgentConfig": {
            "top_k": (int, Field(default=40, description="Top-K sampling")),
            "seed": (int, Field(default=-1, description="Random seed"))
        },
        "GenerateRequest": {
            "custom_field": (str, Field(default="", description="Custom field"))
        }
    }
```

Available models to extend:
- `Message` - Chat messages
- `GenerateRequest` - Generation requests
- `GenerateResponse` - Generation responses
- `AgentConfig` - Agent configuration
- `ResourceUsage` - Resource monitoring

### 2. Hooks

Plugins can intercept and modify data at key points:

```python
def on_agent_init(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
    """Called when agent is initialized."""
    # Modify agent configuration
    return agent_config

def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """Called before generation request."""
    # Add/modify request parameters
    return request

def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
    """Called after generation response."""
    # Process or modify response
    return response

def on_chat_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
    """Called for each chat message."""
    # Filter or modify messages
    return message
```

### 3. Plugin Priority

Plugins execute in priority order (higher = earlier):

```python
config = PluginConfig(
    enabled=True,
    priority=100  # High priority - runs before priority 50
)
```

Default priority is 0. Use:
- 100+ for logging/monitoring
- 50-99 for caching
- 10-49 for transformations
- 0-9 for low-priority tasks

### 4. Lifecycle Management

```python
async def initialize(self):
    """Called once when plugin starts."""
    # Setup resources, connections, etc.
    pass

async def shutdown(self):
    """Called when plugin stops."""
    # Cleanup resources
    pass
```

## Example Plugins

### 1. Logging Plugin

Logs all requests and responses:

```python
class LoggingPlugin(Plugin):
    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Request: {request.get('prompt')[:100]}...")
        return request

    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Response: {response.get('response')[:100]}...")
        return response
```

See `examples/plugins/logging_plugin.py` for full implementation.

### 2. Cache Plugin

Caches responses to avoid redundant API calls:

```python
class CachePlugin(Plugin):
    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        cache_key = self._get_cache_key(request)
        cached = self._get_cached_response(cache_key)
        if cached:
            request["_cached_response"] = cached
        return request

    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        self._save_to_cache(response)
        return response
```

See `examples/plugins/cache_plugin.py` for full implementation.

### 3. Custom Parameters Plugin

Adds new model parameters:

```python
class CustomParamsPlugin(Plugin):
    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        return {
            "AgentConfig": {
                "top_k": (int, Field(default=40, description="Top-K sampling")),
                "repeat_penalty": (float, Field(default=1.1, description="Repeat penalty"))
            }
        }

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if "options" not in request:
            request["options"] = {}
        if "top_k" in request:
            request["options"]["top_k"] = request["top_k"]
        return request
```

See `examples/plugins/custom_params_plugin.py` for full implementation.

## Plugin Configuration

### Configuration File

Plugins can be configured via `~/.ai-cli/plugins.json`:

```json
{
  "logging": {
    "enabled": true,
    "priority": 100,
    "log_file": "ai_cli.log",
    "log_requests": true,
    "log_responses": true
  },
  "cache": {
    "enabled": true,
    "priority": 50,
    "ttl_seconds": 3600,
    "max_cache_size": 1000
  }
}
```

### Programmatic Configuration

```python
from ai_cli.plugin_manager import get_global_manager

manager = get_global_manager()

# Enable/disable
manager.enable_plugin("cache")
manager.disable_plugin("logging")

# Set priority
manager.set_plugin_priority("cache", 75)

# Get plugin info
plugins = manager.list_plugins()
for p in plugins:
    print(f"{p['name']}: enabled={p['enabled']}, priority={p['priority']}")
```

## Auto-Discovery

Place plugins in `~/.ai-cli/plugins/` for automatic discovery:

```bash
~/.ai-cli/plugins/
  my_plugin.py
  another_plugin.py
```

The plugin manager will automatically load them on startup.

## Using Extended Fields

Once a plugin adds fields, you can use them directly:

```python
from ai_cli.types import AgentConfig

# If CustomParamsPlugin is loaded, these fields are available:
agent = AgentConfig(
    name="my_agent",
    role="assistant",
    system_prompt="You are helpful.",
    # Extended fields from plugin:
    top_k=50,
    repeat_penalty=1.2,
    seed=42
)

# Fields appear in modelfile:
print(agent.to_modelfile())
# Output:
# FROM llama3.2
# SYSTEM You are helpful.
# PARAMETER temperature 0.7
# PARAMETER top_k 50
# PARAMETER repeat_penalty 1.2
# PARAMETER seed 42
```

## Best Practices

### 1. Configuration

Always use Pydantic models for plugin config:

```python
class MyPluginConfig(PluginConfig):
    setting1: str = Field(default="value", description="Setting description")
    setting2: int = Field(default=10, ge=1, le=100)  # With validation
```

### 2. Error Handling

Don't let plugin errors crash the system:

```python
def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Your logic here
        return request
    except Exception as e:
        logger.error(f"Plugin error: {e}")
        return request  # Return unmodified request
```

### 3. Documentation

Document your plugin well:

```python
class MyPlugin(Plugin):
    """
    Short description.

    Features:
    - Feature 1
    - Feature 2

    Configuration:
    - setting1: Description
    - setting2: Description

    Example:
        >>> plugin = MyPlugin(config)
        >>> plugin.do_something()
    """
```

### 4. Testing

Test plugins in isolation:

```python
def test_my_plugin():
    plugin = MyPlugin()
    request = {"model": "llama3.2", "prompt": "test"}
    result = plugin.on_generate_request(request)
    assert "my_field" in result
```

## Advanced Topics

### Custom Model Types

Create entirely new model types:

```python
from ai_cli.types import ExtensibleModel
from pydantic import Field

class CustomModel(ExtensibleModel):
    """Your custom model."""
    field1: str = Field(..., description="Field 1")
    field2: int = Field(default=0)
```

### Plugin Dependencies

If your plugin depends on others:

```python
async def initialize(self):
    manager = get_global_manager()
    cache_plugin = manager.get_plugin("cache")
    if not cache_plugin:
        raise RuntimeError("Cache plugin required")
```

### Dynamic Schema Modification

Modify schemas based on runtime conditions:

```python
def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
    extensions = {}
    if self.config.enable_feature_x:
        extensions["AgentConfig"] = {
            "feature_x_param": (str, Field(default=""))
        }
    return extensions
```

## Complete Example

See `examples/plugin_usage.py` for a complete working example demonstrating:
- Plugin registration
- Schema extensions
- Hook execution
- Priority management
- Configuration

## API Reference

### Plugin Base Class

```python
class Plugin(ABC):
    def get_name(self) -> str: ...
    def get_version(self) -> str: ...
    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]: ...
    def on_agent_init(self, agent_config: Dict[str, Any]) -> Dict[str, Any]: ...
    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]: ...
    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]: ...
    def on_chat_message(self, message: Dict[str, Any]) -> Dict[str, Any]: ...
    async def initialize(self): ...
    async def shutdown(self): ...
```

### PluginManager

```python
class PluginManager:
    def register_plugin(self, plugin: Plugin, config: Optional[Dict] = None): ...
    def get_plugin(self, name: str) -> Optional[Plugin]: ...
    def list_plugins(self) -> List[Dict[str, Any]]: ...
    def enable_plugin(self, name: str): ...
    def disable_plugin(self, name: str): ...
    def set_plugin_priority(self, name: str, priority: int): ...
    async def initialize_all(self): ...
    async def shutdown_all(self): ...
    async def process_agent_config(self, config: Dict) -> Dict: ...
    async def process_generate_request(self, request: Dict) -> Dict: ...
    async def process_generate_response(self, response: Dict) -> Dict: ...
    async def process_chat_message(self, message: Dict) -> Dict: ...
```

## Troubleshooting

### Plugin not loading

- Check plugin name doesn't conflict
- Verify `get_name()` returns unique name
- Check plugin file location

### Fields not appearing

- Verify schema extensions are correctly formatted
- Check plugin is enabled
- Confirm plugin is registered before model creation

### Hooks not executing

- Check plugin is enabled
- Verify priority is set correctly
- Ensure `initialize_all()` was called

## Contributing Plugins

Share your plugins with the community:

1. Create plugin following best practices
2. Add documentation
3. Add tests
4. Submit PR to `examples/plugins/`

## Resources

- Example plugins: `examples/plugins/`
- Full demo: `examples/plugin_usage.py`
- Core plugin system: `ai_cli/plugins.py`
- Plugin manager: `ai_cli/plugin_manager.py`
