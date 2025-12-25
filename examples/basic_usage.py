"""Basic usage examples for AI CLI."""

import asyncio
from ai_cli import OllamaClient
from ai_cli.types import Message


async def basic_generate():
    """Basic text generation example."""
    async with OllamaClient() as client:
        # Simple generation
        response = await client.generate(
            model="llama3.2",
            prompt="Write a Python function to calculate factorial",
            system="You are a helpful coding assistant."
        )

        print("Response:", response.response)
        print(f"Took {response.total_duration / 1e9:.2f} seconds")


async def streaming_generate():
    """Streaming generation example."""
    async with OllamaClient() as client:
        print("Streaming response:")

        async for chunk in await client.generate(
            model="llama3.2",
            prompt="Explain how async/await works in Python",
            stream=True
        ):
            if not chunk.done:
                print(chunk.response, end="", flush=True)

        print()


async def chat_example():
    """Chat conversation example."""
    async with OllamaClient() as client:
        messages = [
            Message(role="system", content="You are a helpful coding assistant."),
            Message(role="user", content="How do I read a file in Python?"),
        ]

        response = await client.chat(
            model="llama3.2",
            messages=messages
        )

        print("Assistant:", response["message"]["content"])


async def resource_monitoring():
    """Resource monitoring example."""
    async with OllamaClient(enable_resource_monitoring=True) as client:
        # Generate something
        await client.generate(
            model="llama3.2",
            prompt="Hello, how are you?"
        )

        # Check resources
        usage = client.get_resource_usage()
        if usage:
            print(f"CPU: {usage['cpu_percent']:.1f}%")
            print(f"Memory: {usage['memory_percent']:.1f}%")
            print(f"Available RAM: {usage['memory_available_gb']:.2f} GB")


if __name__ == "__main__":
    print("=== Basic Generate ===")
    asyncio.run(basic_generate())

    print("\n=== Streaming Generate ===")
    asyncio.run(streaming_generate())

    print("\n=== Chat Example ===")
    asyncio.run(chat_example())

    print("\n=== Resource Monitoring ===")
    asyncio.run(resource_monitoring())
