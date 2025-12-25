"""Multi-agent collaborative coding example."""

import asyncio
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator
from ai_cli.prompt_manager import PromptManager


async def create_coding_team_example():
    """Create a team of specialized coding agents."""
    async with OllamaClient() as client:
        orchestrator = AgentOrchestrator(client)

        # Create a coding team with different specializations
        team = orchestrator.create_coding_team(
            model="llama3.2",
            specializations=["backend", "frontend", "testing"]
        )

        print(f"Created team with {len(team)} agents:")
        for name in team.keys():
            print(f"  - {name}")

        # Assign a task to all agents
        task = "Design a REST API for a user authentication system"

        print(f"\nTask: {task}\n")

        results = await orchestrator.distribute_task(task)

        # Show each agent's response
        for result in results:
            print(f"\n{'='*60}")
            print(f"Agent: {result['agent']}")
            print(f"Role: {result['role']}")
            print(f"\nResponse:\n{result['response'][:500]}...")


async def workflow_example():
    """Coordinate a multi-step workflow with different agents."""
    async with OllamaClient() as client:
        orchestrator = AgentOrchestrator(client)

        # Create specialized agents
        team = orchestrator.create_coding_team(
            model="llama3.2",
            specializations=["backend", "testing", "review"]
        )

        # Define workflow
        workflow = [
            {
                "agent": "backend_agent",
                "task": "Write a Python function to validate email addresses using regex"
            },
            {
                "agent": "testing_agent",
                "task": "Write unit tests for the email validation function",
                "use_context": True
            },
            {
                "agent": "review_agent",
                "task": "Review the code and tests, suggest improvements",
                "use_context": True
            }
        ]

        print("Executing workflow...\n")

        # Execute workflow with callback
        async def on_step_complete(step, result):
            print(f"\n{'='*60}")
            print(f"Completed: {step['task'][:50]}...")
            print(f"Agent: {result['agent']}")

        results = await orchestrator.coordinate_workflow(
            workflow,
            on_step_complete=on_step_complete
        )

        # Final summary
        print("\n" + "="*60)
        print("WORKFLOW COMPLETE")
        print("="*60)

        for i, result in enumerate(results):
            print(f"\nStep {i+1}: {result['agent']}")
            print(f"Response preview: {result['response'][:200]}...")


async def custom_agent_example():
    """Create a custom agent with specific system prompt."""
    async with OllamaClient() as client:
        orchestrator = AgentOrchestrator(client)
        prompt_manager = PromptManager()

        # Create custom agent configuration
        custom_prompt = """You are a security-focused code reviewer.

Your role: Analyze code for security vulnerabilities and best practices.

Focus areas:
1. Input validation and sanitization
2. SQL injection prevention
3. XSS prevention
4. Authentication and authorization
5. Secure data handling
6. Dependency vulnerabilities

Always provide:
- Specific vulnerability descriptions
- Severity levels (Critical, High, Medium, Low)
- Remediation recommendations
- Code examples of fixes
"""

        config = prompt_manager.create_agent_config(
            name="security_reviewer",
            role="Security Code Reviewer",
            prompt_template=custom_prompt,
            model="llama3.2",
            temperature=0.3  # Lower temperature for more focused output
        )

        # Register custom agent
        agent = orchestrator.register_agent(config)

        # Test the agent
        code_to_review = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result
"""

        result = await agent.execute_task(
            f"Review this code for security issues:\n\n{code_to_review}"
        )

        print("Security Review:")
        print("="*60)
        print(result['response'])


async def prompt_management_example():
    """Demonstrate system prompt management."""
    prompt_manager = PromptManager()

    # Register custom prompts
    prompt_manager.register_prompt(
        "python_expert",
        "You are a Python expert specializing in performance optimization and clean code."
    )

    prompt_manager.register_prompt(
        "rust_expert",
        "You are a Rust expert specializing in systems programming and memory safety."
    )

    # List registered prompts
    print("Registered prompts:")
    for name in prompt_manager.list_prompts():
        print(f"  - {name}")

    # Retrieve a prompt
    python_prompt = prompt_manager.get_prompt("python_expert")
    print(f"\nPython expert prompt:\n{python_prompt}")


if __name__ == "__main__":
    print("=== Coding Team Example ===")
    asyncio.run(create_coding_team_example())

    print("\n\n=== Workflow Example ===")
    asyncio.run(workflow_example())

    print("\n\n=== Custom Agent Example ===")
    asyncio.run(custom_agent_example())

    print("\n\n=== Prompt Management Example ===")
    asyncio.run(prompt_management_example())
