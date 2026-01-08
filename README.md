# ai-cli

Offline AI assistant for code writing, command execution, and chat working with any offline models.

**Website:** [novacom.ru](https://novacom.ru)

## Installation

```bash
pip install ai-offline-cli
```

## Usage

```bash
ai-cli --help
```

## Features

- **Code generation and assistance** - AI-powered code writing and refactoring
- **Command execution** - Execute commands with AI assistance
- **Chat interface** - Interactive chat with offline models
- **Multiple model providers** - Works with Ollama, llama.cpp, and more
- **Plugin system** - Extend functionality with custom plugins
- **Resource monitoring** - Track CPU, memory, and GPU usage

## Plugin System

AI CLI features a powerful plugin system that allows extending functionality without modifying core code.

### Quick Example

```python
from ai_cli.plugins import Plugin
from ai_cli.plugin_manager import get_global_manager

class MyPlugin(Plugin):
    def get_name(self) -> str:
        return "my_plugin"

    def get_version(self) -> str:
        return "1.0.0"

    # Add custom fields to models
    def get_schema_extensions(self):
        return {
            "AgentConfig": {
                "my_param": (int, Field(default=10))
            }
        }

# Register and use
manager = get_global_manager()
manager.register_plugin(MyPlugin())
```

### Built-in Example Plugins

- **Logging Plugin** - Log all requests/responses
- **Cache Plugin** - Cache responses to avoid redundant calls
- **Custom Parameters Plugin** - Add model parameters like top_k, seed, etc.

See [Plugin Documentation](docs/PLUGINS.md) for complete guide.

## Examples

Check out the `examples/` directory for:
- Basic usage
- Multi-agent systems
- Different model providers
- Resource optimization
- **Plugin examples and usage**
