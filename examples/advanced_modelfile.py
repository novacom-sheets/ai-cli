"""Advanced examples for Modelfile management and custom model creation."""

import asyncio
from ai_cli import OllamaClient
from ai_cli.types import AgentConfig
from ai_cli.prompt_manager import PromptManager


async def create_custom_models():
    """Create custom Ollama models with specific system prompts."""
    async with OllamaClient() as client:
        # Example 1: Create a Python expert model
        python_modelfile = """FROM llama3.2

SYSTEM You are a Python expert specializing in clean code, type hints, and modern Python practices.

You always:
1. Use type hints for all function signatures
2. Write comprehensive docstrings
3. Follow PEP 8 style guidelines
4. Prefer list comprehensions and generator expressions
5. Use dataclasses and Pydantic when appropriate
6. Write unit tests with pytest

PARAMETER temperature 0.5
PARAMETER top_p 0.9
PARAMETER num_predict 2000
"""

        print("Creating Python expert model...")
        async for status in await client.create_model(
            name="python-expert",
            modelfile=python_modelfile,
            stream=True
        ):
            if "status" in status:
                print(f"  {status['status']}")

        # Example 2: Create a Rust expert model
        rust_modelfile = """FROM llama3.2

SYSTEM You are a Rust expert focusing on memory safety, performance, and idiomatic Rust.

Core principles:
1. Ownership and borrowing
2. Zero-cost abstractions
3. Memory safety without garbage collection
4. Fearless concurrency
5. Type system and trait-based design

Always explain:
- Lifetime annotations when needed
- When to use Box, Rc, Arc, RefCell
- Performance implications
- Common pitfalls and how to avoid them

PARAMETER temperature 0.4
PARAMETER num_predict 3000
"""

        print("\nCreating Rust expert model...")
        async for status in await client.create_model(
            name="rust-expert",
            modelfile=rust_modelfile,
            stream=True
        ):
            if "status" in status:
                print(f"  {status['status']}")

        # Example 3: Create a security auditor model
        security_modelfile = """FROM llama3.2

SYSTEM You are a cybersecurity expert specializing in code security audits.

Your analysis covers:
1. OWASP Top 10 vulnerabilities
2. Input validation and sanitization
3. Authentication and authorization flaws
4. SQL injection, XSS, CSRF
5. Insecure dependencies
6. Data exposure and privacy issues
7. Cryptographic vulnerabilities
8. API security

For each finding, provide:
- Severity (Critical/High/Medium/Low)
- Detailed description
- Proof of concept (if applicable)
- Remediation steps with code examples
- References to security standards

PARAMETER temperature 0.3
PARAMETER top_k 20
PARAMETER num_predict 4000
"""

        print("\nCreating security auditor model...")
        async for status in await client.create_model(
            name="security-auditor",
            modelfile=security_modelfile,
            stream=True
        ):
            if "status" in status:
                print(f"  {status['status']}")


async def use_custom_models():
    """Use the custom models we created."""
    async with OllamaClient() as client:
        # Use Python expert
        print("\n" + "="*60)
        print("Testing Python expert model:")
        print("="*60)

        python_response = await client.generate(
            model="python-expert",
            prompt="Write a function to validate email addresses with proper type hints and docstring"
        )

        print(python_response.response[:500])

        # Use Rust expert
        print("\n" + "="*60)
        print("Testing Rust expert model:")
        print("="*60)

        rust_response = await client.generate(
            model="rust-expert",
            prompt="Explain the difference between Box<T> and Rc<T> with examples"
        )

        print(rust_response.response[:500])

        # Use security auditor
        print("\n" + "="*60)
        print("Testing security auditor model:")
        print("="*60)

        vulnerable_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result
"""

        security_response = await client.generate(
            model="security-auditor",
            prompt=f"Audit this code for security vulnerabilities:\n\n{vulnerable_code}"
        )

        print(security_response.response[:500])


async def show_model_info():
    """Show detailed information about models including system prompts."""
    async with OllamaClient() as client:
        models = ["python-expert", "rust-expert", "security-auditor"]

        for model_name in models:
            try:
                info = await client.show_model(model_name)

                print(f"\n{'='*60}")
                print(f"Model: {model_name}")
                print(f"{'='*60}")

                # Extract system prompt from modelfile
                if "modelfile" in info:
                    modelfile = info["modelfile"]
                    lines = modelfile.split("\n")

                    print("\nModelfile configuration:")
                    for line in lines[:10]:  # First 10 lines
                        print(f"  {line}")

                    if len(lines) > 10:
                        print(f"  ... ({len(lines) - 10} more lines)")

            except Exception as e:
                print(f"\nModel {model_name} not found: {e}")


async def agent_config_to_modelfile():
    """Convert AgentConfig to Modelfile and create model."""
    async with OllamaClient() as client:
        pm = PromptManager()

        # Create agent configuration
        config = AgentConfig(
            name="golang_expert",
            role="Go Developer",
            system_prompt="""You are a Go (Golang) expert.

Expertise areas:
1. Goroutines and channels
2. Interface design
3. Error handling patterns
4. Testing with testing package
5. Performance optimization
6. Standard library usage

Code style:
- Idiomatic Go code
- Effective Go guidelines
- Proper error handling
- Clear naming conventions
- Minimal dependencies""",
            model="llama3.2",
            temperature=0.6,
            max_tokens=2500
        )

        # Generate Modelfile from config
        modelfile = config.to_modelfile()

        print("Generated Modelfile:")
        print("="*60)
        print(modelfile)
        print("="*60)

        # Create model in Ollama
        print("\nCreating Go expert model from AgentConfig...")

        async for status in await client.create_model(
            name="golang-expert",
            modelfile=modelfile,
            stream=True
        ):
            if "status" in status:
                print(f"  {status['status']}")

        # Test the model
        print("\n" + "="*60)
        print("Testing golang-expert model:")
        print("="*60)

        response = await client.generate(
            model="golang-expert",
            prompt="Write a concurrent web scraper using goroutines and channels"
        )

        print(response.response[:500])


async def delete_custom_models():
    """Clean up custom models."""
    async with OllamaClient() as client:
        models_to_delete = [
            "python-expert",
            "rust-expert",
            "security-auditor",
            "golang-expert"
        ]

        for model in models_to_delete:
            try:
                print(f"Deleting {model}...")
                await client.delete_model(model)
                print(f"  ✓ Deleted {model}")
            except Exception as e:
                print(f"  ✗ Failed to delete {model}: {e}")


if __name__ == "__main__":
    print("=== Creating Custom Models ===")
    asyncio.run(create_custom_models())

    print("\n\n=== Using Custom Models ===")
    asyncio.run(use_custom_models())

    print("\n\n=== Show Model Info ===")
    asyncio.run(show_model_info())

    print("\n\n=== AgentConfig to Modelfile ===")
    asyncio.run(agent_config_to_modelfile())

    # Uncomment to delete custom models
    # print("\n\n=== Deleting Custom Models ===")
    # asyncio.run(delete_custom_models())
