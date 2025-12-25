"""Example of using different model providers."""

import asyncio
from ai_cli.models import (
    ModelRegistry,
    OllamaProvider,
    LlamaCppProvider,
    create_standard_registry
)
from ai_cli.types import Message


async def ollama_provider_example():
    """Use Ollama provider directly."""
    provider = OllamaProvider(base_url="http://localhost:11434")

    await provider.initialize()

    try:
        # List available models
        models = await provider.list_models()
        print(f"Available Ollama models: {models}")

        # Generate text
        response = await provider.generate(
            prompt="Explain asyncio in Python",
            system="You are a helpful Python tutor",
            model="llama3.2"
        )

        print(f"\nResponse:\n{response}")

    finally:
        await provider.shutdown()


async def llama_cpp_provider_example():
    """Use llama.cpp provider directly."""
    # NOTE: You need to have a GGUF model file
    # Download from: https://huggingface.co/models?library=gguf

    model_path = "/path/to/your/model.gguf"  # Change this!

    provider = LlamaCppProvider(model_path=model_path)

    try:
        await provider.initialize(
            n_ctx=4096,
            n_gpu_layers=-1  # Use all GPU layers
        )

        response = await provider.generate(
            prompt="What is machine learning?",
            system="You are a helpful AI assistant"
        )

        print(f"Response:\n{response}")

    except ImportError:
        print("llama-cpp-python not installed!")
        print("Install with: pip install llama-cpp-python")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await provider.shutdown()


async def model_registry_example():
    """Use model registry to switch between providers."""
    # Create registry with standard providers
    registry = await create_standard_registry(
        ollama_url="http://localhost:11434",
        # llama_cpp_model="/path/to/model.gguf"  # Optional
    )

    try:
        # List available providers
        providers = registry.list_providers()
        print(f"Available providers: {providers}")

        # Use active provider (Ollama by default)
        active = registry.get_active_provider()
        print(f"\nActive provider: {active.model_type.value}")

        # Generate using active provider
        response = await active.generate(
            prompt="Write a haiku about coding",
            model="llama3.2"
        )

        print(f"\nHaiku:\n{response}")

        # Chat using active provider
        messages = [
            Message(role="system", content="You are a helpful assistant"),
            Message(role="user", content="What is the difference between await and async?")
        ]

        chat_response = await active.chat(messages, model="llama3.2")
        print(f"\nChat response:\n{chat_response}")

    finally:
        await registry.shutdown_all()


async def switching_providers_example():
    """Demonstrate switching between providers."""
    registry = ModelRegistry()

    # Register multiple Ollama providers with different configurations
    provider1 = OllamaProvider(base_url="http://localhost:11434")
    provider2 = OllamaProvider(base_url="http://another-host:11434")

    registry.register_provider("local_ollama", provider1)
    registry.register_provider("remote_ollama", provider2)

    await registry.initialize_provider("local_ollama")
    # await registry.initialize_provider("remote_ollama")  # If you have a remote instance

    try:
        # Use local provider
        registry.set_active_provider("local_ollama")
        local_provider = registry.get_active_provider()

        response = await local_provider.generate(
            prompt="Hello from local!",
            model="llama3.2"
        )

        print(f"Local response: {response[:100]}...")

        # Switch to remote provider (if available)
        # registry.set_active_provider("remote_ollama")
        # remote_provider = registry.get_active_provider()
        # response = await remote_provider.generate(...)

    finally:
        await registry.shutdown_all()


async def streaming_with_providers():
    """Stream responses from different providers."""
    provider = OllamaProvider()
    await provider.initialize()

    try:
        print("Streaming response:")

        stream = await provider.generate(
            prompt="Count from 1 to 10 slowly",
            model="llama3.2",
            stream=True
        )

        async for chunk in stream:
            print(chunk, end="", flush=True)

        print()

    finally:
        await provider.shutdown()


if __name__ == "__main__":
    print("=== Ollama Provider Example ===")
    asyncio.run(ollama_provider_example())

    print("\n\n=== Model Registry Example ===")
    asyncio.run(model_registry_example())

    print("\n\n=== Switching Providers Example ===")
    asyncio.run(switching_providers_example())

    print("\n\n=== Streaming Example ===")
    asyncio.run(streaming_with_providers())

    # Uncomment to test llama.cpp (requires GGUF model file)
    # print("\n\n=== Llama.cpp Provider Example ===")
    # asyncio.run(llama_cpp_provider_example())
