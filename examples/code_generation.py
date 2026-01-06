"""Example of code generation with automatic file saving."""

import asyncio
from pathlib import Path
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator


async def basic_code_generation():
    """Generate code and automatically save to files."""
    async with OllamaClient() as client:
        # Create orchestrator with auto-save enabled
        orchestrator = AgentOrchestrator(
            client,
            output_dir=Path("./generated_code"),
            auto_save_code=True
        )

        # Create a backend agent
        team = orchestrator.create_coding_team(
            model="llama3.2",
            specializations=["backend"]
        )

        # Ask agent to write code - it will be automatically saved
        task = """
        Напиши простой REST API endpoint на Python с FastAPI для регистрации пользователя.
        Включи валидацию email и пароля.
        Сохрани в файлы с правильными именами.
        """

        print("Генерирую код...")
        results = await orchestrator.distribute_task(task)

        # Check what was saved
        print("\n✅ Код сгенерирован!")
        for result in results:
            print(f"\nАгент: {result['agent']}")

            if "saved_files" in result:
                print("Сохраненные файлы:")
                for file in result["saved_files"]:
                    print(f"  📄 {file}")
            else:
                print("  (Код не найден для сохранения)")

        # Get all saved files
        all_files = orchestrator.get_saved_files()
        print(f"\n📁 Всего сохранено файлов: {len(all_files)}")


async def multi_agent_project():
    """Generate complete project with multiple agents."""
    async with OllamaClient() as client:
        orchestrator = AgentOrchestrator(
            client,
            output_dir=Path("./user_auth_project"),
            auto_save_code=True
        )

        # Create full team
        team = orchestrator.create_coding_team(
            model="llama3.2",
            specializations=["backend", "testing"]
        )

        # Step 1: Backend creates API
        print("Шаг 1: Backend разрабатывает API...")

        backend_task = """
        Создай REST API для системы авторизации пользователей на Python с FastAPI.

        Требования:
        1. Endpoint /register для регистрации (POST)
        2. Endpoint /login для входа (POST)
        3. Pydantic модели для User
        4. Хеширование паролей
        5. JWT токены

        Каждый компонент в отдельном файле:
        - models.py - модели данных
        - auth.py - логика авторизации
        - main.py - FastAPI приложение

        Используй синтаксис ```python:filename.py для указания имен файлов.
        """

        backend_results = await orchestrator.distribute_task(
            backend_task,
            agent_names=["backend_agent"]
        )

        # Step 2: Testing creates tests
        print("\nШаг 2: Testing пишет тесты...")

        testing_task = """
        Напиши unit тесты для API авторизации используя pytest.

        Покрой тестами:
        1. Регистрацию нового пользователя
        2. Регистрацию с существующим email (ошибка)
        3. Логин с правильными credentials
        4. Логин с неправильным паролем

        Сохрани в файл ```python:test_auth.py
        """

        testing_results = await orchestrator.distribute_task(
            testing_task,
            agent_names=["testing_agent"]
        )

        # Summary
        print("\n" + "="*60)
        print("🎉 Проект создан!")
        print("="*60)

        all_files = orchestrator.get_saved_files()
        print(f"\n📁 Создано файлов: {len(all_files)}")
        for file in all_files:
            size = file.stat().st_size
            print(f"  📄 {file.name} ({size} bytes)")

        print(f"\n📂 Расположение: {orchestrator.code_parser.output_dir}")


async def manual_code_extraction():
    """Manually extract and save code from response."""
    from ai_cli.code_parser import CodeParser

    async with OllamaClient() as client:
        # Generate code without auto-save
        response = await client.generate(
            model="llama3.2",
            prompt="""
            Напиши класс User на Python с полями:
            - id: int
            - email: str
            - password_hash: str
            - created_at: datetime

            Используй dataclass и добавь методы для валидации.

            Сохрани как ```python:user.py
            """,
            system="Ты опытный Python разработчик"
        )

        print("Ответ модели:")
        print(response.response[:500])
        print("...\n")

        # Manually parse and save
        parser = CodeParser(output_dir=Path("./manual_output"))

        blocks = parser.extract_code_blocks(response.response)
        print(f"Найдено блоков кода: {len(blocks)}\n")

        for i, block in enumerate(blocks):
            print(f"Блок {i+1}:")
            print(f"  Язык: {block.language}")
            print(f"  Имя файла: {block.filename or 'не указано'}")
            print(f"  Строк кода: {len(block.code.splitlines())}")

            # Save
            saved_path = parser.save_code_block(block)
            print(f"  ✅ Сохранено: {saved_path}\n")


async def streaming_with_code_save():
    """Stream response and save code blocks."""
    async with OllamaClient() as client:
        print("Генерация кода (streaming)...\n")

        full_response = ""

        async for chunk in await client.generate(
            model="llama3.2",
            prompt="""
            Создай простой HTTP сервер на Python используя http.server.
            Добавь обработку GET и POST запросов.

            Сохрани как ```python:server.py
            """,
            stream=True
        ):
            if not chunk.done:
                print(chunk.response, end="", flush=True)
                full_response += chunk.response

        print("\n\n" + "="*60)

        # Parse and save after streaming completes
        from ai_cli.code_parser import CodeParser

        parser = CodeParser(output_dir=Path("./streaming_output"))
        saved = parser.save_all_code_blocks(full_response)

        print(f"\n✅ Сохранено файлов: {len(saved)}")
        for file in saved:
            print(f"  📄 {file}")


async def organize_project():
    """Generate and organize code into proper project structure."""
    from ai_cli.code_parser import CodeOrganizer

    async with OllamaClient() as client:
        orchestrator = AgentOrchestrator(
            client,
            output_dir=Path("./temp_output"),
            auto_save_code=True
        )

        # Generate various components
        team = orchestrator.create_coding_team(
            specializations=["backend", "testing"]
        )

        tasks = [
            "Создай User модель с Pydantic",
            "Создай UserService для CRUD операций",
            "Создай UserController для HTTP endpoints",
            "Создай тесты для User модели",
        ]

        for task in tasks:
            await orchestrator.distribute_task(task)

        # Organize into MVC structure
        organizer = CodeOrganizer(Path("./organized_project"))

        all_files = orchestrator.get_saved_files()
        organized_dir = organizer.create_structured_project(
            all_files,
            structure_type="mvc"  # or "by_language" or "flat"
        )

        print(f"✅ Проект организован в: {organized_dir}")
        print("\nСтруктура:")
        for path in organized_dir.rglob("*"):
            if path.is_file():
                relative = path.relative_to(organized_dir)
                print(f"  📄 {relative}")


if __name__ == "__main__":
    print("=== 1. Базовая генерация кода ===")
    asyncio.run(basic_code_generation())

    print("\n\n=== 2. Мультиагентный проект ===")
    asyncio.run(multi_agent_project())

    print("\n\n=== 3. Ручное извлечение кода ===")
    asyncio.run(manual_code_extraction())

    print("\n\n=== 4. Streaming с сохранением ===")
    asyncio.run(streaming_with_code_save())

    print("\n\n=== 5. Организация проекта ===")
    asyncio.run(organize_project())
