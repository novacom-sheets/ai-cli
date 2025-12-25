# Быстрый старт (5 минут)

Минимальная инструкция для тех, кто хочет быстро начать работу.

## Предварительные требования

- Python 3.11 или 3.12 установлен
- Ollama установлен и запущен

## Быстрая установка

```bash
# 1. Создайте и активируйте виртуальное окружение
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
# или venv\Scripts\activate на Windows

# 2. Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 3. Установите ai_cli в режиме разработки
pip install -e .

# 4. Проверьте что Ollama работает и скачайте модель
ollama pull llama3.2

# 5. Запустите диагностику
python diagnose.py

# 6. Попробуйте первый пример
python examples/basic_usage.py
```

## Первый код (с автосохранением в файлы!)

Создайте `test.py`:

```python
import asyncio
from pathlib import Path
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator

async def main():
    async with OllamaClient() as client:
        # Создаем оркестратор с автосохранением
        orch = AgentOrchestrator(
            client,
            output_dir=Path("./my_code"),
            auto_save_code=True  # Код автоматически сохраняется!
        )

        # Создаем агента
        team = orch.create_coding_team(specializations=["backend"])

        # Агент напишет код И сохранит в файлы
        results = await orch.distribute_task(
            "Напиши функцию для проверки email на Python с валидацией. "
            "Сохрани как ```python:validate_email.py"
        )

        # Проверяем что сохранилось
        for result in results:
            print(f"\n{result['agent']}:")
            if "saved_files" in result:
                print("✅ Сохранено:")
                for f in result["saved_files"]:
                    print(f"  📄 {f}")

asyncio.run(main())
```

Запустите:
```bash
python test.py
```

**Результат:** Код будет автоматически сохранен в `./my_code/validate_email.py`!

## Мультиагентная система (автоматически создает проект!)

Создайте `team.py`:

```python
import asyncio
from pathlib import Path
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator

async def main():
    async with OllamaClient() as client:
        # Создаем команду агентов с автосохранением
        orch = AgentOrchestrator(
            client,
            output_dir=Path("./user_api"),
            auto_save_code=True
        )

        team = orch.create_coding_team(
            specializations=["backend", "testing"]
        )

        # Даем задачу - код будет сохранен автоматически!
        results = await orch.distribute_task(
            """Создай REST API для регистрации пользователя на FastAPI.

            Нужно:
            1. models.py - Pydantic модель User
            2. api.py - endpoint /register
            3. test_api.py - тесты

            Используй ```python:filename.py для указания имен файлов.
            """
        )

        # Смотрим что создалось
        print("\n📁 Созданные файлы:")
        for f in orch.get_saved_files():
            print(f"  📄 {f}")

asyncio.run(main())
```

**Результат:** Полный проект создается в `./user_api/` с правильной структурой файлов!

## CLI режим

```bash
# Интерактивный чат
python -m ai_cli.cli chat

# Мультиагентная команда
python -m ai_cli.cli team "Разработай систему авторизации"

# Список моделей
python -m ai_cli.cli models
```

## Что дальше?

- **Больше примеров**: смотрите папку `examples/`
- **Детальная установка**: [INSTALL.md](INSTALL.md)
- **Проблемы**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Полная документация**: [README.md](README.md)

## Проблемы?

Запустите диагностику:
```bash
python diagnose.py
```

Она покажет все проблемы и как их исправить.

---

**Готово!** Начните с простых примеров и постепенно изучайте возможности системы.
