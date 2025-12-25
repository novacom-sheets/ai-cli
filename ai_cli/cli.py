"""Command-line interface for AI CLI."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from .client import OllamaClient
from .agent import AgentOrchestrator
from .prompt_manager import PromptManager
from .models import create_standard_registry


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


async def main():
    """Main CLI entry point."""
    cli = CLI()

    try:
        await cli.initialize()

        if len(sys.argv) > 1:
            # Command mode
            command = sys.argv[1]

            if command == "chat":
                await cli.interactive_mode()

            elif command == "team":
                if len(sys.argv) < 3:
                    print("Usage: ai-cli team <task>")
                    return

                task = " ".join(sys.argv[2:])
                await cli.run_workflow(
                    task=task,
                    specializations=["backend", "frontend", "testing"]
                )

            elif command == "models":
                models = await cli.client.list_models()
                print("Available models:")
                for model in models.get("models", []):
                    print(f"  - {model['name']}")

            else:
                print(f"Unknown command: {command}")
                print("Available commands: chat, team, models")

        else:
            # Default to interactive mode
            await cli.interactive_mode()

    finally:
        await cli.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
