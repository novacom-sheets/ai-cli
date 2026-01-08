# AI CLI Architecture

## Overview

AI CLI is built with a modular, extensible architecture that separates concerns and allows easy customization through plugins.

## Core Components

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                      (CLI / API)                         │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                  Plugin Manager                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Plugin Registry                                  │  │
│  │  - Logging Plugin                                 │  │
│  │  - Cache Plugin                                   │  │
│  │  - Custom Params Plugin                           │  │
│  │  - User Plugins...                                │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                  Core Types                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ExtensibleModel (Base)                          │  │
│  │  - Message                                        │  │
│  │  - GenerateRequest                                │  │
│  │  - GenerateResponse                               │  │
│  │  - AgentConfig                                    │  │
│  │  - ResourceUsage                                  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│               Model Providers                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ModelProvider (ABC)                              │  │
│  │  ├─ OllamaProvider                                │  │
│  │  ├─ LlamaCppProvider                              │  │
│  │  └─ Custom Providers...                           │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│            Supporting Services                          │
│  - OllamaClient (HTTP client)                          │
│  - ResourceMonitor (CPU/Memory/GPU tracking)           │
│  - PromptManager (Prompt templates)                    │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Request Processing

```
User Request
    ↓
Plugin Manager (on_agent_init hooks)
    ↓
AgentConfig (with plugin extensions)
    ↓
Plugin Manager (on_generate_request hooks)
    ↓
GenerateRequest (with plugin extensions)
    ↓
Model Provider
    ↓
Underlying Model (Ollama/llama.cpp)
```

### 2. Response Processing

```
Model Response
    ↓
Model Provider
    ↓
Plugin Manager (on_generate_response hooks)
    ↓
GenerateResponse (with plugin extensions)
    ↓
User
```

## Plugin System Architecture

### Plugin Lifecycle

```python
# 1. Plugin Creation
plugin = MyPlugin(config)

# 2. Registration
manager.register_plugin(plugin)
# - Registers schema extensions
# - Registers hooks by priority
# - Loads configuration

# 3. Initialization
await manager.initialize_all()
# - Calls plugin.initialize()
# - Sets up resources

# 4. Execution
# Hooks are called at appropriate points:
# - on_agent_init
# - on_generate_request
# - on_generate_response
# - on_chat_message

# 5. Shutdown
await manager.shutdown_all()
# - Calls plugin.shutdown()
# - Cleanup resources
```

### Schema Extension System

```python
# Plugin declares extensions
def get_schema_extensions(self):
    return {
        "AgentConfig": {
            "new_field": (str, Field(default="value"))
        }
    }

# ExtensibleModel accepts extra fields
class AgentConfig(ExtensibleModel):
    # Base fields...
    model_config = ConfigDict(extra="allow")

# Usage
agent = AgentConfig(
    name="agent",
    new_field="custom_value"  # From plugin!
)
```

### Hook Execution

```python
# Plugins registered with priority
plugins = [
    (100, LoggingPlugin),    # High priority
    (50, CachePlugin),       # Medium
    (10, CustomPlugin)       # Low
]

# Execute in order
async def execute_hook(hook_name, data):
    result = data
    for priority, plugin in sorted_plugins:
        if plugin.enabled:
            result = plugin.hook_method(result)
    return result
```

## Component Details

### 1. ExtensibleModel

Base class for all models that can be extended by plugins:

```python
class ExtensibleModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    def get_extensions(self) -> Dict[str, Any]:
        """Get all fields added by plugins."""
        base_fields = set(self.model_fields.keys())
        all_fields = set(self.model_dump().keys())
        return {k: v for k, v in ... if k not in base_fields}
```

### 2. Plugin

Abstract base for all plugins:

```python
class Plugin(ABC):
    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_version(self) -> str: ...

    def get_schema_extensions(self) -> Dict: ...
    def on_agent_init(self, config: Dict) -> Dict: ...
    def on_generate_request(self, request: Dict) -> Dict: ...
    def on_generate_response(self, response: Dict) -> Dict: ...
    async def initialize(self): ...
    async def shutdown(self): ...
```

### 3. PluginManager

Central coordinator for plugin system:

```python
class PluginManager:
    def __init__(self):
        self.registry = PluginRegistry()
        self._plugin_configs = {}

    def register_plugin(self, plugin): ...
    def discover_plugins(self): ...
    async def process_agent_config(self, config): ...
    async def process_generate_request(self, request): ...
    # ...
```

### 4. ModelProvider

Abstract interface for different model backends:

```python
class ModelProvider(ABC):
    async def generate(self, prompt, **kwargs): ...
    async def chat(self, messages, **kwargs): ...
    async def list_models(self): ...
    # ...
```

## Extension Points

### 1. Adding New Model Types

Create new extensible models:

```python
class MyCustomModel(ExtensibleModel):
    field1: str
    field2: int
```

### 2. Adding New Providers

Implement ModelProvider interface:

```python
class MyProvider(ModelProvider):
    async def generate(self, prompt, **kwargs):
        # Your implementation
        pass
```

### 3. Adding New Plugins

Extend Plugin base class:

```python
class MyPlugin(Plugin):
    def get_name(self):
        return "my_plugin"

    def on_generate_request(self, request):
        # Your logic
        return request
```

### 4. Custom Hooks

Add new hook types in PluginManager:

```python
# In PluginManager
self._hooks["my_custom_hook"] = []

# In Plugin
def on_my_custom_hook(self, data):
    return data
```

## Configuration Management

### Plugin Configuration

```json
{
  "plugin_name": {
    "enabled": true,
    "priority": 50,
    "custom_setting": "value"
  }
}
```

### Agent Configuration

```python
agent = AgentConfig(
    # Base fields
    name="agent",
    model="llama3.2",
    temperature=0.7,

    # Plugin-added fields
    top_k=40,
    seed=42,
    log_id="123"
)
```

## Best Practices

### 1. Separation of Concerns

- **Core**: Basic functionality only
- **Providers**: Model integration
- **Plugins**: Extensions and customization

### 2. Plugin Independence

Each plugin should:
- Be self-contained
- Not depend on other plugins (unless documented)
- Handle errors gracefully
- Return data even if processing fails

### 3. Configuration

- Use Pydantic models for type safety
- Provide sensible defaults
- Document all settings

### 4. Testing

Test each layer independently:
- Unit tests for plugins
- Integration tests for providers
- End-to-end tests for workflows

## Performance Considerations

### 1. Plugin Priority

Order plugins by impact:
- Logging: High priority (100+)
- Caching: Medium priority (50-99)
- Transformations: Low priority (0-49)

### 2. Async Operations

Use async for I/O operations:
```python
async def initialize(self):
    await self.setup_connection()
```

### 3. Resource Management

Clean up in shutdown:
```python
async def shutdown(self):
    await self.close_connections()
    self.cache.clear()
```

## Security

### 1. Plugin Isolation

Plugins run in same process - be careful with:
- File system access
- Network requests
- Resource usage

### 2. Configuration Validation

Use Pydantic validators:
```python
class Config(PluginConfig):
    path: str = Field(...)

    @validator('path')
    def validate_path(cls, v):
        # Validate path is safe
        return v
```

## Future Enhancements

Potential improvements:

1. **Async Hooks** - Make all hooks async
2. **Plugin Sandboxing** - Isolate plugin execution
3. **Hot Reload** - Reload plugins without restart
4. **Plugin Marketplace** - Share and discover plugins
5. **Dependency Management** - Plugin dependencies
6. **Version Constraints** - Plugin compatibility checks

## Summary

The architecture provides:

✅ **Extensibility** - Add features without modifying core
✅ **Flexibility** - Support multiple model providers
✅ **Modularity** - Clean separation of concerns
✅ **Type Safety** - Pydantic models throughout
✅ **Configurability** - Rich configuration system
✅ **Performance** - Async operations, efficient hooks

The plugin system is the key differentiator, allowing users to customize and extend AI CLI to fit their specific needs.
