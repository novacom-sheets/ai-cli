# AI CLI - Low-Level Multi-Agent Development System

Низкоуровневый Python клиент для работы с Ollama и другими оффлайн моделями с поддержкой мультиагентных систем для collaborative разработки.

## Основные возможности

- **Низкоуровневый HTTP клиент** для Ollama с полным контролем над запросами
- **Управление ресурсами ПК** - мониторинг CPU, RAM, GPU
- **Контроль system prompts** (`application/vnd.ollama.image.system`) для создания агентов
- **Мультиагентная система** для совместной работы при написании кода
- **Абстракция провайдеров** - легкое подключение других оффлайн моделей (llama.cpp, GGUF и др.)
- **Async/await** архитектура для эффективной работы
- **HTTP/2** поддержка для оптимальной производительности

## Архитектура

```
ai_cli/
├── client.py              # Низкоуровневый Ollama HTTP клиент
├── agent.py               # Мультиагентная система
├── prompt_manager.py      # Управление system prompts
├── models.py              # Абстракция провайдеров моделей
├── resource_monitor.py    # Мониторинг ресурсов системы
├── types.py               # Типы данных
└── cli.py                 # CLI интерфейс
```

## 📋 Документация

- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Начните работу за 5 минут
- 📦 **[INSTALL.md](INSTALL.md)** - Подробная инструкция по установке для начинающих
- 🔧 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Решение частых проблем
- 💡 **Примеры** - см. папку `examples/`
- 🩺 **`python diagnose.py`** - Автоматическая диагностика системы

## Системные требования

**Рекомендованная версия Python: 3.11 или 3.12**

⚠️ **ВАЖНО**: Не используйте Python 3.13+ - некоторые зависимости еще не полностью совместимы.

Проверьте вашу версию Python:
```bash
python --version
```
```bash
# или
python3 --version
```

Если у вас Python 3.13+, установите Python 3.12:
- **macOS**: `brew install python@3.12`
- **Windows**: Скачайте с [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3.12` или `sudo yum install python3.12`

## Установка

### Шаг 1: Убедитесь что Ollama запущен

```bash
# Проверьте что Ollama работает
curl http://localhost:11434/api/tags

# Если не работает, установите Ollama:
# macOS/Linux: https://ollama.ai/download
# Или запустите: ollama serve
```

### Шаг 2: Создайте виртуальное окружение

**Что такое виртуальное окружение?**
Это изолированная папка для Python пакетов вашего проекта, чтобы не было конфликтов с другими проектами.

```bash
# Перейдите в папку проекта
cd /path/to/ai-cli
```
```bash
# Создайте виртуальное окружение (делается один раз)
python3.12 -m venv venv
```
```bash
# или если python3.12 не найден:
python3 -m venv venv
```
* Активируйте окружение
* На macOS/Linux:
```bash
source venv/bin/activate
```
```bash
# На Windows:
venv\Scripts\activate

# После активации вы увидите (venv) в начале строки терминала
```

### Шаг 3: Установите зависимости

```bash
# Убедитесь что виртуальное окружение активно (видите (venv) в терминале)

# Обновите pip до последней версии
pip3 install --upgrade pip
```
```bash
# Установите основные зависимости
pip3 install -r requirements.txt
```
```bash
# Установите ai_cli в режиме разработки
pip3 install -e .
```
```bash
# Опционально: для llama.cpp поддержки (GGUF модели)
pip3 install llama-cpp-python
```
```bash
# Опционально: для мониторинга NVIDIA GPU
pip3 install pynvml
```

### Шаг 4: Проверьте установку

```bash
# Должно работать без ошибок
python -c "import ai_cli; print('✓ AI CLI installed successfully')"
```
```bash
# Запустите простой пример
python examples/basic_usage.py
```

**Проблемы с установкой?** См. **[INSTALL.md](INSTALL.md)** для детальной инструкции или **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** для решения проблем.

### Как выключить виртуальное окружение

```bash
# Когда закончите работу
deactivate
```

### Как активировать снова

```bash
# В следующий раз просто активируйте окружение заново
cd /path/to/ai-cli
source venv/bin/activate  # macOS/Linux
```
```bash
# или
venv\Scripts\activate     # Windows
```

## Быстрый старт

### 1. Автоматическое сохранение кода в файлы

```python
import asyncio
from pathlib import Path
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator

async def main():
    async with OllamaClient() as client:
        # Создаем оркестратор с автосохранением кода
        orch = AgentOrchestrator(
            client,
            output_dir=Path("./my_project"),
            auto_save_code=True  # Код автоматически сохраняется в файлы!
        )

        team = orch.create_coding_team(specializations=["backend"])

        # Агент напишет код и сохранит в файлы
        results = await orch.distribute_task(
            "Создай FastAPI endpoint для регистрации пользователя"
        )

        # Проверяем что было сохранено
        for result in results:
            if "saved_files" in result:
                print("Сохраненные файлы:", result["saved_files"])

asyncio.run(main())
```

### 2. Базовое использование

```python
import asyncio
from ai_cli import OllamaClient

async def main():
    async with OllamaClient() as client:
        response = await client.generate(
            model="llama3.2",
            prompt="Write a Python function to calculate fibonacci",
            system="You are a helpful coding assistant"
        )
        print(response.response)

asyncio.run(main())
```

### 2. Мультиагентная разработка

```python
import asyncio
from ai_cli import OllamaClient
from ai_cli.agent import AgentOrchestrator

async def main():
    async with OllamaClient() as client:
        # Создаем оркестратор
        orchestrator = AgentOrchestrator(client)

        # Создаем команду специализированных агентов
        team = orchestrator.create_coding_team(
            model="llama3.2",
            specializations=["backend", "frontend", "testing", "review"]
        )

        # Распределяем задачу между агентами
        task = "Design a REST API for user authentication"
        results = await orchestrator.distribute_task(task)

        # Каждый агент даст свое видение задачи
        for result in results:
            print(f"{result['agent']}: {result['response'][:200]}...")

asyncio.run(main())
```

### 3. Workflow с несколькими агентами

```python
# Создаем последовательный workflow
workflow = [
    {
        "agent": "backend_agent",
        "task": "Write a user registration endpoint"
    },
    {
        "agent": "testing_agent",
        "task": "Write tests for the registration endpoint",
        "use_context": True  # Использовать результат предыдущего агента
    },
    {
        "agent": "review_agent",
        "task": "Review code and suggest improvements",
        "use_context": True
    }
]

results = await orchestrator.coordinate_workflow(workflow)
```

### 4. Управление System Prompts

```python
from ai_cli.prompt_manager import PromptManager

# Создаем менеджер промптов
pm = PromptManager()

# Регистрируем кастомный system prompt
pm.register_prompt(
    "security_expert",
    "You are a cybersecurity expert specializing in code security audits."
)

# Создаем агента с этим промптом
config = pm.create_agent_config(
    name="security_agent",
    role="Security Auditor",
    prompt_template=pm.get_prompt("security_expert"),
    model="llama3.2",
    temperature=0.3
)

# Используем агента
agent = orchestrator.register_agent(config)
result = await agent.execute_task("Review this code for vulnerabilities: ...")
```

### 5. Работа с разными моделями

```python
from ai_cli.models import create_standard_registry

# Создаем registry с поддержкой разных провайдеров
registry = await create_standard_registry(
    ollama_url="http://localhost:11434",
    llama_cpp_model="/path/to/model.gguf"  # Опционально
)

# Используем активный провайдер
provider = registry.get_active_provider()
response = await provider.generate(
    prompt="Explain Python decorators",
    model="llama3.2"
)

# Переключаемся на другой провайдер
registry.set_active_provider("llama_cpp")
provider = registry.get_active_provider()
```

### 6. Мониторинг ресурсов

```python
async with OllamaClient(enable_resource_monitoring=True) as client:
    # Клиент автоматически мониторит ресурсы
    response = await client.generate(
        model="llama3.2",
        prompt="Complex task..."
    )

    # Получаем текущее использование ресурсов
    usage = client.get_resource_usage()
    print(f"CPU: {usage['cpu_percent']}%")
    print(f"Memory: {usage['memory_percent']}%")
    print(f"Available RAM: {usage['memory_available_gb']} GB")
```

## CLI Интерфейс

```bash
# Интерактивный режим
python -m ai_cli.cli chat

# Запустить мультиагентную команду
python -m ai_cli.cli team "Create a user authentication system"

# Список доступных моделей
python -m ai_cli.cli models
```

## Примеры

Смотрите директорию `examples/`:
- `basic_usage.py` - базовые примеры работы с клиентом
- `multi_agent.py` - мультиагентные системы
- `model_providers.py` - работа с разными провайдерами моделей

## Конфигурация агентов

### Создание кастомного агента

```python
from ai_cli.types import AgentConfig

config = AgentConfig(
    name="rust_expert",
    role="Rust Developer",
    system_prompt="""You are an expert Rust developer.
    Focus on memory safety, performance, and idiomatic Rust code.
    Always explain ownership and borrowing when relevant.""",
    model="llama3.2",
    temperature=0.7,
    max_tokens=2000
)

# Регистрируем агента
agent = orchestrator.register_agent(config)
```

### Генерация Modelfile

```python
# AgentConfig может создать Modelfile для Ollama
modelfile = config.to_modelfile()
print(modelfile)
# Выведет:
# FROM llama3.2
# SYSTEM You are an expert Rust developer...
# PARAMETER temperature 0.7
# PARAMETER num_predict 2000

# Создаем кастомную модель в Ollama
await client.create_model(
    name="rust-expert",
    modelfile=modelfile
)
```

## Продвинутые возможности

### Streaming ответов

```python
# Потоковая генерация
async for chunk in await client.generate(
    model="llama3.2",
    prompt="Explain async programming",
    stream=True
):
    print(chunk.response, end="", flush=True)
```

### Контроль контекста

```python
# Генерируем с сохранением контекста
response1 = await client.generate(
    model="llama3.2",
    prompt="Start a story about a programmer"
)

# Продолжаем с тем же контекстом
response2 = await client.generate(
    model="llama3.2",
    prompt="Continue the story",
    context=response1.context  # Передаем контекст
)
```

### Ограничение ресурсов

```python
from ai_cli.resource_monitor import ResourceMonitor

monitor = ResourceMonitor(check_interval=0.5)
await monitor.start()

# Проверяем нужно ли ограничить запросы
if monitor.should_throttle(cpu_threshold=80, memory_threshold=85):
    print("System under load, throttling requests...")
    await asyncio.sleep(1)
```

## Подключение других моделей

### llama.cpp

```python
from ai_cli.models import LlamaCppProvider

provider = LlamaCppProvider(model_path="/path/to/model.gguf")
await provider.initialize(
    n_ctx=4096,
    n_gpu_layers=-1  # Использовать GPU
)

response = await provider.generate(
    prompt="Hello!",
    system="You are helpful"
)
```

### Кастомный провайдер

```python
from ai_cli.models import ModelProvider, ModelType

class CustomProvider(ModelProvider):
    def __init__(self):
        super().__init__(ModelType.CUSTOM)

    async def initialize(self, **kwargs):
        # Инициализация вашей модели
        pass

    async def generate(self, prompt, system=None, **kwargs):
        # Ваша логика генерации
        pass

    async def chat(self, messages, **kwargs):
        # Ваша логика чата
        pass

# Регистрируем в registry
registry.register_provider("my_model", CustomProvider())
```

## Преимущества архитектуры

1. **Низкоуровневый контроль**: Прямой доступ к HTTP API Ollama
2. **Эффективность**: HTTP/2, connection pooling, async/await
3. **Мониторинг**: Отслеживание CPU, RAM, GPU в реальном времени
4. **Гибкость**: Легко подключить любую оффлайн модель
5. **Масштабируемость**: Мультиагентная система для больших проектов
6. **Управление промптами**: Централизованный контроль system prompts

## Требования

- **Python 3.11 или 3.12** (рекомендовано, НЕ 3.13+)
- **Ollama** запущенный локально (`http://localhost:11434`) или на удаленном сервере
- Зависимости: httpx, pydantic, psutil (устанавливаются автоматически)

## Лицензия

MIT

## Разработка

```bash
# Установка для разработки
pip install -e .

# Запуск примеров
python examples/basic_usage.py
python examples/multi_agent.py
python examples/model_providers.py
```

## Roadmap

- [ ] Поддержка Hugging Face Transformers
- [ ] Веб-интерфейс для управления агентами
- [ ] Персистентность истории разговоров
- [ ] Интеграция с VS Code
- [ ] Distributed multi-agent systems (работа через сеть)
- [ ] Benchmark разных моделей
- [ ] Автоматическое тестирование кода агентами
