# Plugin Quick Start Guide

Get started with AI CLI plugins in 5 minutes.

## Basic Plugin in 3 Steps

### Step 1: Create Plugin

Create file `my_plugin.py`:

```python
from ai_cli.plugins import Plugin
from typing import Dict, Any

class MyPlugin(Plugin):
    def get_name(self) -> str:
        return "my_plugin"

    def get_version(self) -> str:
        return "1.0.0"

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Processing: {request.get('prompt')[:50]}...")
        return request
```

### Step 2: Register Plugin

```python
from ai_cli.plugin_manager import get_global_manager

manager = get_global_manager()
manager.register_plugin(MyPlugin())
await manager.initialize_all()
```

### Step 3: Use It

Now all requests will print the prompt!

## Adding Custom Parameters

Want to add `top_k` parameter to agent config?

```python
from pydantic import Field

class TopKPlugin(Plugin):
    def get_name(self) -> str:
        return "topk"

    def get_version(self) -> str:
        return "1.0.0"

    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        return {
            "AgentConfig": {
                "top_k": (int, Field(default=40, description="Top-K sampling"))
            }
        }

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if "top_k" in request:
            if "options" not in request:
                request["options"] = {}
            request["options"]["top_k"] = request["top_k"]
        return request
```

Now use it:

```python
from ai_cli.types import AgentConfig

agent = AgentConfig(
    name="agent",
    role="assistant",
    system_prompt="You are helpful.",
    top_k=50  # New parameter!
)
```

## Complete Examples

### Logging Everything

```python
import logging
from ai_cli.plugins import Plugin

logger = logging.getLogger(__name__)

class LoggingPlugin(Plugin):
    def get_name(self) -> str:
        return "logger"

    def get_version(self) -> str:
        return "1.0.0"

    def on_generate_request(self, request):
        logger.info(f"Request: {request}")
        return request

    def on_generate_response(self, response):
        logger.info(f"Response: {response}")
        return response
```

### Caching Responses

```python
import hashlib
import json
from pathlib import Path

class SimpleCache(Plugin):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def get_name(self) -> str:
        return "cache"

    def get_version(self) -> str:
        return "1.0.0"

    def _cache_key(self, request):
        key = f"{request.get('model')}:{request.get('prompt')}"
        return hashlib.md5(key.encode()).hexdigest()

    def on_generate_request(self, request):
        key = self._cache_key(request)
        if key in self.cache:
            request["_cached"] = self.cache[key]
        return request

    def on_generate_response(self, response):
        # Save to cache
        if "prompt" in response:
            key = self._cache_key(response)
            self.cache[key] = response
        return response
```

### Timing Requests

```python
import time

class TimingPlugin(Plugin):
    def get_name(self) -> str:
        return "timing"

    def get_version(self) -> str:
        return "1.0.0"

    def on_generate_request(self, request):
        request["_start_time"] = time.time()
        return request

    def on_generate_response(self, response):
        if "_start_time" in response:
            duration = time.time() - response["_start_time"]
            print(f"Request took {duration:.2f}s")
        return response
```

## Plugin Priority

Control execution order:

```python
from ai_cli.plugins import PluginConfig

# High priority - runs first
logging_config = PluginConfig(priority=100)
logging_plugin = LoggingPlugin(logging_config)

# Low priority - runs last
timing_config = PluginConfig(priority=10)
timing_plugin = TimingPlugin(timing_config)
```

Execution order: 100 → 50 → 10 → 0 (higher = earlier)

## Enable/Disable Plugins

```python
manager = get_global_manager()

# Disable
manager.disable_plugin("cache")

# Enable
manager.enable_plugin("cache")

# Change priority
manager.set_plugin_priority("logging", 200)
```

## Configuration File

Save to `~/.ai-cli/plugins.json`:

```json
{
  "logging": {
    "enabled": true,
    "priority": 100,
    "log_file": "/var/log/ai-cli.log"
  },
  "cache": {
    "enabled": true,
    "priority": 50,
    "ttl_seconds": 3600
  }
}
```

Load config:

```python
from pydantic import Field
from ai_cli.plugins import PluginConfig

class LoggingConfig(PluginConfig):
    log_file: str = Field(default="ai-cli.log")

# Config auto-loaded from JSON
plugin = LoggingPlugin()
```

## Auto-Discovery

Place plugins in `~/.ai-cli/plugins/`:

```bash
mkdir -p ~/.ai-cli/plugins
cp my_plugin.py ~/.ai-cli/plugins/
```

Auto-loaded on startup!

## Hooks Reference

All available hooks:

```python
class MyPlugin(Plugin):
    def on_agent_init(self, agent_config: Dict) -> Dict:
        """Called when agent is created."""
        return agent_config

    def on_generate_request(self, request: Dict) -> Dict:
        """Called before generation."""
        return request

    def on_generate_response(self, response: Dict) -> Dict:
        """Called after generation."""
        return response

    def on_chat_message(self, message: Dict) -> Dict:
        """Called for each message."""
        return message

    async def initialize(self):
        """Called once on startup."""
        pass

    async def shutdown(self):
        """Called once on shutdown."""
        pass
```

## Common Patterns

### Add Field to Request

```python
def get_schema_extensions(self):
    return {
        "GenerateRequest": {
            "my_field": (str, Field(default=""))
        }
    }
```

### Modify Request

```python
def on_generate_request(self, request):
    request["my_field"] = "value"
    return request
```

### Transform Response

```python
def on_generate_response(self, response):
    response["response"] = response["response"].upper()
    return response
```

### Store State

```python
class StatePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def on_generate_request(self, request):
        self.counter += 1
        print(f"Request #{self.counter}")
        return request
```

## Next Steps

1. Check out example plugins in `examples/plugins/`
2. Read full documentation in `docs/PLUGINS.md`
3. See architecture in `docs/ARCHITECTURE.md`
4. Run demo: `python examples/plugin_usage.py`

## Troubleshooting

**Plugin not working?**

```python
# Check if registered
manager = get_global_manager()
print(manager.list_plugins())

# Check if enabled
plugin = manager.get_plugin("my_plugin")
print(f"Enabled: {plugin.config.enabled}")

# Initialize
await manager.initialize_all()
```

**Fields not appearing?**

Make sure plugin is registered BEFORE creating models:

```python
# ✅ Correct order
manager.register_plugin(MyPlugin())
agent = AgentConfig(my_field="value")

# ❌ Wrong order
agent = AgentConfig(my_field="value")  # Field doesn't exist yet!
manager.register_plugin(MyPlugin())
```

## Tips

1. **Start simple** - Begin with basic hooks
2. **Test in isolation** - Test plugin separately
3. **Handle errors** - Always return data, even on error
4. **Document** - Add docstrings and comments
5. **Use priorities** - Order plugins logically

Happy plugin building! 🚀
