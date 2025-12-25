"""Examples of resource monitoring and optimization."""

import asyncio
from ai_cli import OllamaClient
from ai_cli.resource_monitor import ResourceMonitor
from ai_cli.agent import AgentOrchestrator


async def basic_monitoring():
    """Basic resource monitoring example."""
    async with OllamaClient(enable_resource_monitoring=True) as client:
        print("Starting resource monitoring...")

        # Generate something
        print("\nGenerating response...")
        await client.generate(
            model="llama3.2",
            prompt="Write a detailed explanation of Docker containers and how they work"
        )

        # Check resources
        usage = client.get_resource_usage()

        print("\nResource Usage:")
        print(f"  CPU: {usage['cpu_percent']:.1f}%")
        print(f"  Memory: {usage['memory_percent']:.1f}%")
        print(f"  Available RAM: {usage['memory_available_gb']:.2f} GB")

        if usage.get('gpu_usage'):
            print(f"\n  GPU Info:")
            gpu = usage['gpu_usage']
            if gpu['type'] == 'nvidia':
                for device in gpu['devices']:
                    print(f"    GPU {device['id']} ({device['name']}):")
                    print(f"      Memory: {device['memory_percent']:.1f}%")
                    print(f"      Utilization: {device['gpu_percent']:.1f}%")


async def throttling_example():
    """Example of request throttling based on resource usage."""
    monitor = ResourceMonitor(check_interval=0.5)
    await monitor.start()

    try:
        async with OllamaClient() as client:
            tasks = [
                "Explain Python async/await",
                "Write a REST API in FastAPI",
                "Explain Docker networking",
                "Create a database schema for e-commerce",
                "Implement JWT authentication"
            ]

            for i, task in enumerate(tasks):
                # Check if we should throttle
                if monitor.should_throttle(cpu_threshold=80, memory_threshold=85):
                    usage = await monitor.get_current_usage()
                    print(f"\n⚠️  System under load!")
                    print(f"    CPU: {usage.cpu_percent:.1f}%")
                    print(f"    Memory: {usage.memory_percent:.1f}%")
                    print(f"    Waiting 3 seconds before next request...")
                    await asyncio.sleep(3)

                print(f"\n[Task {i+1}/{len(tasks)}] {task}")

                response = await client.generate(
                    model="llama3.2",
                    prompt=task
                )

                print(f"  ✓ Completed ({len(response.response)} chars)")

                # Brief pause between requests
                await asyncio.sleep(0.5)

    finally:
        await monitor.stop()


async def concurrent_with_monitoring():
    """Run multiple agents concurrently while monitoring resources."""
    monitor = ResourceMonitor(check_interval=1.0)
    await monitor.start()

    try:
        async with OllamaClient(enable_resource_monitoring=True) as client:
            orchestrator = AgentOrchestrator(client)

            # Create team
            team = orchestrator.create_coding_team(
                model="llama3.2",
                specializations=["backend", "frontend", "testing"]
            )

            print(f"Created team with {len(team)} agents")

            # Monitor resources while running tasks
            async def monitor_task():
                """Background task to monitor resources."""
                while True:
                    usage = await monitor.get_current_usage()
                    print(f"\n[Monitor] CPU: {usage.cpu_percent:.1f}% | "
                          f"Memory: {usage.memory_percent:.1f}% | "
                          f"Available: {usage.memory_available_gb:.2f} GB")

                    if usage.memory_percent > 90:
                        print("  ⚠️  WARNING: High memory usage!")

                    await asyncio.sleep(2)

            # Start monitoring in background
            monitor_task_handle = asyncio.create_task(monitor_task())

            # Run the actual work
            task = "Design a microservices architecture for an e-commerce platform"

            print(f"\nExecuting task: {task}")
            print("="*60)

            results = await orchestrator.distribute_task(task)

            # Cancel monitoring
            monitor_task_handle.cancel()

            # Show results
            print("\n" + "="*60)
            print("Results:")
            print("="*60)

            for result in results:
                print(f"\n{result['agent']}:")
                print(f"  {result['response'][:200]}...")

    finally:
        await monitor.stop()


async def adaptive_batch_size():
    """Adapt batch size based on available resources."""
    monitor = ResourceMonitor()
    await monitor.start()

    try:
        async with OllamaClient() as client:
            prompts = [
                f"Generate code example #{i}"
                for i in range(20)
            ]

            async def process_batch(batch, batch_num):
                """Process a batch of prompts."""
                print(f"\nProcessing batch {batch_num} ({len(batch)} items)...")

                tasks = [
                    client.generate(model="llama3.2", prompt=p)
                    for p in batch
                ]

                results = await asyncio.gather(*tasks)
                print(f"  ✓ Completed batch {batch_num}")
                return results

            # Determine batch size based on resources
            usage = await monitor.get_current_usage()

            if usage.memory_available_gb > 8:
                batch_size = 5
            elif usage.memory_available_gb > 4:
                batch_size = 3
            else:
                batch_size = 1

            print(f"Available memory: {usage.memory_available_gb:.2f} GB")
            print(f"Selected batch size: {batch_size}")

            # Process in batches
            all_results = []
            for i in range(0, len(prompts), batch_size):
                batch = prompts[i:i + batch_size]
                results = await process_batch(batch, i // batch_size + 1)
                all_results.extend(results)

                # Re-check resources and adjust if needed
                usage = await monitor.get_current_usage()
                if usage.memory_percent > 85:
                    print("  ⚠️  High memory, reducing batch size")
                    batch_size = max(1, batch_size - 1)

            print(f"\n✓ Processed all {len(all_results)} prompts")

    finally:
        await monitor.stop()


async def gpu_detection():
    """Detect and display GPU information."""
    monitor = ResourceMonitor()
    await monitor.start()

    try:
        usage = await monitor.get_current_usage()

        print("GPU Detection:")
        print("="*60)

        if usage.gpu_usage:
            gpu_info = usage.gpu_usage

            if gpu_info['type'] == 'nvidia':
                print("✓ NVIDIA GPU detected")
                for device in gpu_info['devices']:
                    print(f"\n  GPU {device['id']}: {device['name']}")
                    print(f"    Memory: {device['memory_used_gb']:.2f} GB / "
                          f"{device['memory_total_gb']:.2f} GB "
                          f"({device['memory_percent']:.1f}%)")
                    print(f"    Utilization: {device['gpu_percent']:.1f}%")

            elif gpu_info['type'] == 'apple_silicon':
                print("✓ Apple Silicon detected")
                print("  Unified memory architecture")

            else:
                print(f"✓ GPU type: {gpu_info['type']}")

        else:
            print("✗ No GPU detected or GPU monitoring not available")
            print("\nTo enable NVIDIA GPU monitoring:")
            print("  pip install pynvml")

    finally:
        await monitor.stop()


if __name__ == "__main__":
    print("=== Basic Monitoring ===")
    asyncio.run(basic_monitoring())

    print("\n\n=== GPU Detection ===")
    asyncio.run(gpu_detection())

    print("\n\n=== Throttling Example ===")
    asyncio.run(throttling_example())

    print("\n\n=== Adaptive Batch Size ===")
    asyncio.run(adaptive_batch_size())

    # Note: This one is more resource intensive
    # print("\n\n=== Concurrent with Monitoring ===")
    # asyncio.run(concurrent_with_monitoring())
