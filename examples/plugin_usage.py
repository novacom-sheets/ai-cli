"""Complete example of using the plugin system."""

import asyncio
from ai_cli.plugin_manager import get_global_manager
from ai_cli.types import AgentConfig, GenerateRequest

# Import example plugins
from plugins.logging_plugin import LoggingPlugin, LoggingPluginConfig
from plugins.cache_plugin import CachePlugin, CachePluginConfig
from plugins.custom_params_plugin import CustomParamsPlugin, CustomParamsPluginConfig


async def main():
    """Demonstrate plugin system usage."""

    # Get plugin manager
    manager = get_global_manager()

    print("=== AI CLI Plugin System Demo ===\n")

    # 1. Register plugins
    print("1. Registering plugins...")

    # Logging plugin
    logging_config = LoggingPluginConfig(
        enabled=True,
        priority=100,  # High priority - runs first
        log_requests=True,
        log_responses=True,
        log_file="ai_cli_demo.log"
    )
    logging_plugin = LoggingPlugin(logging_config)
    manager.register_plugin(logging_plugin)

    # Cache plugin
    cache_config = CachePluginConfig(
        enabled=True,
        priority=50,  # Medium priority
        ttl_seconds=3600,
        max_cache_size=1000
    )
    cache_plugin = CachePlugin(cache_config)
    manager.register_plugin(cache_plugin)

    # Custom params plugin
    params_config = CustomParamsPluginConfig(
        enabled=True,
        priority=10,  # Lower priority
        enable_top_k=True,
        enable_repeat_penalty=True,
        enable_seed=True
    )
    params_plugin = CustomParamsPlugin(params_config)
    manager.register_plugin(params_plugin)

    # 2. List registered plugins
    print("\n2. Registered plugins:")
    for plugin_info in manager.list_plugins():
        print(f"   - {plugin_info['name']} v{plugin_info.get('version', 'unknown')}")
        print(f"     Enabled: {plugin_info['enabled']}, Priority: {plugin_info['priority']}")

    # 3. Initialize all plugins
    print("\n3. Initializing plugins...")
    await manager.initialize_all()

    # 4. Create agent config with extended fields
    print("\n4. Creating agent config with plugin extensions...")
    agent_config = AgentConfig(
        name="demo_agent",
        role="AI assistant with plugins",
        system_prompt="You are a helpful AI assistant.",
        model="llama3.2",
        temperature=0.7,
        # Custom fields from custom_params_plugin:
        top_k=50,
        repeat_penalty=1.2,
        seed=42
    )

    print(f"   Agent: {agent_config.name}")
    print(f"   Custom params: top_k={agent_config.top_k}, "
          f"repeat_penalty={agent_config.repeat_penalty}, seed={agent_config.seed}")

    # Process through plugins
    agent_dict = agent_config.model_dump()
    processed_agent = await manager.process_agent_config(agent_dict)
    print(f"   Processed through {len(manager.list_plugins())} plugins")

    # 5. Create generate request with extended fields
    print("\n5. Creating generate request with plugin extensions...")
    request = GenerateRequest(
        model="llama3.2",
        prompt="What is the meaning of life?",
        system="You are a philosophical assistant.",
        # Cache plugin fields:
        use_cache=True,
        # Logging plugin fields:
        log_id="demo_request_001",
        # Custom params plugin fields:
        top_k=40,
        repeat_penalty=1.1
    )

    # Process through plugins
    request_dict = request.model_dump()
    processed_request = await manager.process_generate_request(request_dict)
    print(f"   Request processed through plugin hooks")
    print(f"   Cache enabled: {processed_request.get('use_cache')}")
    print(f"   Log ID: {processed_request.get('log_id')}")

    # 6. Show generated modelfile with extensions
    print("\n6. Generated Modelfile with plugin extensions:")
    print("   " + "-" * 50)
    for line in agent_config.to_modelfile().split('\n'):
        print(f"   {line}")
    print("   " + "-" * 50)

    # 7. Plugin management
    print("\n7. Plugin management:")

    # Disable a plugin
    print("   Disabling cache plugin...")
    manager.disable_plugin("cache")

    # Change priority
    print("   Changing logging plugin priority to 200...")
    manager.set_plugin_priority("logging", 200)

    # List plugins again
    print("\n   Updated plugin status:")
    for plugin_info in manager.list_plugins():
        print(f"   - {plugin_info['name']}: enabled={plugin_info['enabled']}, "
              f"priority={plugin_info['priority']}")

    # 8. Cleanup
    print("\n8. Shutting down plugins...")
    await manager.shutdown_all()

    print("\n=== Demo Complete ===")
    print("\nKey features demonstrated:")
    print("  ✓ Plugin registration and configuration")
    print("  ✓ Schema extensions (adding new fields)")
    print("  ✓ Hook execution (processing data through plugins)")
    print("  ✓ Plugin priority management")
    print("  ✓ Enable/disable plugins")
    print("  ✓ Modelfile generation with extensions")


if __name__ == "__main__":
    asyncio.run(main())
