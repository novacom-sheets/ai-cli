"""Command-line interface for AI CLI."""

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

from .client import OllamaClient
from .agent import AgentOrchestrator
from .prompt_manager import PromptManager
from .models import create_standard_registry


def extract_filename_from_query(query: str) -> Optional[str]:
    """Extract filename from query like 'Напиши HELLO-WORLD.md' or 'create config.py'."""
    # Patterns to match filenames with extensions
    patterns = [
        r'["\']?([a-zA-Z0-9_-]+\.[a-zA-Z0-9]+)["\']?',  # filename.ext
        r'файл\s+([a-zA-Z0-9_-]+\.[a-zA-Z0-9]+)',       # файл filename.ext
        r'create\s+([a-zA-Z0-9_-]+\.[a-zA-Z0-9]+)',     # create filename.ext
        r'write\s+([a-zA-Z0-9_-]+\.[a-zA-Z0-9]+)',      # write filename.ext
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1)

    return None


def extract_code_blocks(text: str) -> str:
    """Extract code blocks from markdown-formatted text."""
    # Remove markdown code fences and keep only content
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)

    if code_blocks:
        # If there are code blocks, join them
        return '\n\n'.join(code_blocks)

    # If no code blocks, return original text
    return text


class CLI:
    """Simple CLI for interacting with the AI system."""

    def __init__(self):
        self.client: Optional[OllamaClient] = None
        self.orchestrator: Optional[AgentOrchestrator] = None
        self.prompt_manager = PromptManager()

    async def initialize(self, ollama_url: str = "http://localhost:11434"):
        """Initialize the CLI."""
        self.client = OllamaClient(base_url=ollama_url)
        await self.client.__aenter__()
        self.orchestrator = AgentOrchestrator(self.client, self.prompt_manager)

    async def shutdown(self):
        """Shutdown the CLI."""
        if self.client:
            await self.client.__aexit__(None, None, None)

    async def interactive_mode(self):
        """Run interactive chat mode."""
        print("AI CLI - Interactive Mode")
        print("Type 'exit' to quit, 'help' for commands")
        print("-" * 60)

        from .types import Message

        messages = [
            Message(role="system", content="You are a helpful AI assistant for software development.")
        ]

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                if user_input.lower() == "help":
                    self.print_help()
                    continue

                if not user_input:
                    continue

                # Add user message
                messages.append(Message(role="user", content=user_input))

                # Get response
                response = await self.client.chat(
                    model="llama3.2",
                    messages=messages,
                    stream=False
                )

                assistant_message = response["message"]["content"]

                # Add assistant message
                messages.append(Message(role="assistant", content=assistant_message))

                print(f"\nAssistant: {assistant_message}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

    def print_help(self):
        """Print help message."""
        help_text = """
Available commands:
  exit, quit     - Exit the program
  help           - Show this help message

Usage examples:
  - Ask questions about coding
  - Request code generation
  - Get explanations of concepts
        """
        print(help_text)

    async def create_agent_team(self, specializations: list[str], model: str = "llama3.2"):
        """Create a team of coding agents."""
        if not self.orchestrator:
            print("Error: CLI not initialized")
            return

        team = self.orchestrator.create_coding_team(
            model=model,
            specializations=specializations
        )

        print(f"Created team with {len(team)} agents:")
        for name, agent in team.items():
            print(f"  - {name}: {agent.config.role}")

        return team

    async def run_workflow(self, task: str, specializations: list[str]):
        """Run a collaborative workflow."""
        if not self.orchestrator:
            print("Error: CLI not initialized")
            return

        # Create team
        await self.create_agent_team(specializations)

        print(f"\nTask: {task}")
        print("=" * 60)

        # Distribute task
        results = await self.orchestrator.distribute_task(task)

        # Print results
        for result in results:
            print(f"\n{result['agent']} ({result['role']}):")
            print("-" * 60)
            print(result['response'][:500])
            if len(result['response']) > 500:
                print("...")

    async def quick_query(self, query: str, model: str = "llama3.2",
                         output_file: Optional[str] = None,
                         auto_save: bool = False,
                         extract_code: bool = False):
        """Quick single query without conversation history."""
        from .types import Message

        messages = [
            Message(role="system", content="You are a helpful AI assistant."),
            Message(role="user", content=query)
        ]

        print(f"Query: {query}")
        print("-" * 60)

        response = await self.client.chat(
            model=model,
            messages=messages,
            stream=False
        )

        assistant_message = response["message"]["content"]

        # Determine output filename
        filename = output_file
        if auto_save and not filename:
            filename = extract_filename_from_query(query)

        # Save to file if filename is specified
        if filename:
            content_to_save = assistant_message

            # Extract code blocks if requested
            if extract_code:
                content_to_save = extract_code_blocks(assistant_message)

            output_path = Path(filename)
            output_path.write_text(content_to_save, encoding='utf-8')

            print(f"\n✓ Saved to: {output_path.absolute()}")
            print(f"  Size: {len(content_to_save)} bytes")
            print(f"\nContent preview:")
            print("-" * 60)
            print(f"\n{assistant_message[:500]}")
            if len(assistant_message) > 500:
                print("...")
        else:
            # Just print to console
            print(f"\n{assistant_message}")

        return assistant_message

    async def list_models(self):
        """List available models."""
        models = await self.client.list_models()
        print("\nAvailable models:")
        print("-" * 60)
        for model in models.get("models", []):
            name = model.get('name', 'unknown')
            size = model.get('size', 0)
            size_gb = size / (1024**3) if size > 0 else 0
            print(f"  {name:<30} ({size_gb:.2f} GB)")
        print()


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='ai-cli',
        description='AI CLI - Multi-agent development system for Ollama',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-cli "explain python decorators"                    # Quick query
  ai-cli --model llama3.2 "write a function"            # Query with specific model
  ai-cli --auto-save "Напиши HELLO-WORLD.md"            # Auto-save to file
  ai-cli --output result.py "write fibonacci function"  # Save to specific file
  ai-cli -s -c "create config.py"                       # Auto-save, extract code only
  ai-cli chat                                            # Interactive chat mode
  ai-cli --models                                        # List available models
  ai-cli team "build a REST API"                         # Multi-agent workflow

For more information, visit: https://github.com/your-repo/ai-cli
        """
    )

    # Positional argument for quick queries
    parser.add_argument(
        'query',
        nargs='*',
        help='Quick query text (e.g., "explain python decorators")'
    )

    # Optional arguments
    parser.add_argument(
        '--model', '-m',
        default='llama3.2',
        help='Model to use (default: llama3.2)'
    )

    parser.add_argument(
        '--models',
        action='store_true',
        help='List available models'
    )

    parser.add_argument(
        '--ollama-url',
        default='http://localhost:11434',
        help='Ollama server URL (default: http://localhost:11434)'
    )

    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help='Save output to file (e.g., --output result.md)'
    )

    parser.add_argument(
        '--auto-save', '-s',
        action='store_true',
        help='Automatically save to file if filename detected in query'
    )

    parser.add_argument(
        '--extract-code', '-c',
        action='store_true',
        help='Extract only code blocks from response (use with --output or --auto-save)'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 0.1.0'
    )

    return parser


async def async_main():
    """Async main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    cli = CLI()

    try:
        await cli.initialize(ollama_url=args.ollama_url)

        # List models
        if args.models:
            await cli.list_models()
            return

        # Check if query is a command
        if args.query:
            query_text = ' '.join(args.query)

            # Special commands
            if query_text == 'chat':
                await cli.interactive_mode()
                return

            elif query_text.startswith('team '):
                task = query_text[5:]  # Remove 'team ' prefix
                await cli.run_workflow(
                    task=task,
                    specializations=["backend", "frontend", "testing"]
                )
                return

            # Regular quick query
            else:
                await cli.quick_query(
                    query_text,
                    model=args.model,
                    output_file=args.output,
                    auto_save=args.auto_save,
                    extract_code=args.extract_code
                )
                return

        # No query provided - show help or start interactive mode
        else:
            parser.print_help()
            print("\nStarting interactive mode...\n")
            await cli.interactive_mode()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await cli.shutdown()


def main():
    """Synchronous entry point for console_scripts."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
