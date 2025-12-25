# Решение проблем

Это руководство поможет решить наиболее частые проблемы при работе с AI CLI.

## Проблемы с Python

### ❌ "python: command not found"

**Причина:** Python не установлен или не добавлен в PATH.

**Решение:**
```bash
# Попробуйте python3 вместо python
python3 --version

# Если это работает, используйте python3 везде
python3 -m venv venv
python3 examples/basic_usage.py

# Или создайте alias (macOS/Linux)
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

Если и `python3` не работает, установите Python (см. INSTALL.md).

### ❌ Несовместимая версия Python (3.13+)

**Симптомы:**
```
ERROR: Could not find a version that satisfies the requirement pydantic>=2.0.0
```

**Решение:**
```bash
# Установите Python 3.12
# macOS:
brew install python@3.12

# Пересоздайте виртуальное окружение
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "No module named 'venv'"

**Причина:** Модуль venv не установлен (часто на Linux).

**Решение (Ubuntu/Debian):**
```bash
sudo apt install python3.12-venv
```

**Решение (CentOS/RHEL):**
```bash
sudo yum install python3-venv
```

## Проблемы с зависимостями

### ❌ "ModuleNotFoundError: No module named 'ai_cli'"

**Причина:** Пакет ai_cli не установлен.

**Решение:**
```bash
# 1. Убедитесь что видите (venv) в начале строки
# Если нет:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 2. Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 3. Установите ai_cli в режиме разработки (editable mode)
pip install -e .

# 4. Проверьте установку
python -c "import ai_cli; print('OK')"
```

### ❌ Ошибки при установке httpx или pydantic

**Симптомы:**
```
error: subprocess-exited-with-error
building wheel for httpx...
```

**Решение:**
```bash
# Обновите pip, setuptools и wheel
pip install --upgrade pip setuptools wheel

# Попробуйте установить заново
pip install -r requirements.txt
pip install -e .

# Если не помогает, установите по одной:
pip install "httpx[http2]>=0.27.0,<0.28.0"
pip install "pydantic>=2.0.0,<3.0.0"
pip install "psutil>=5.9.0,<6.0.0"
pip install -e .
```

### ❌ "ImportError: Using http2=True, but the 'h2' package is not installed"

**Причина:** HTTP/2 поддержка требует дополнительную библиотеку h2.

**Решение:**
```bash
# Переустановите httpx с поддержкой HTTP/2
pip uninstall httpx
pip install "httpx[http2]>=0.27.0"

# Или установите заново все зависимости
pip install -r requirements.txt
```

### ❌ Ошибка при установке llama-cpp-python

**Симптомы:**
```
error: Microsoft Visual C++ 14.0 or greater is required
# или
error: command 'gcc' failed
```

**Решение Windows:**
1. Установите [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Перезапустите терминал
3. `pip install llama-cpp-python`

**Решение macOS:**
```bash
# Установите Xcode Command Line Tools
xcode-select --install

# Переустановите
pip install llama-cpp-python
```

**Решение Linux:**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Переустановите
pip install llama-cpp-python
```

## Проблемы с Ollama

### ❌ Connection refused / Cannot connect to Ollama

**Симптомы:**
```
httpx.ConnectError: [Errno 61] Connection refused
```

**Решение:**
```bash
# 1. Проверьте работает ли Ollama
curl http://localhost:11434/api/tags

# Если нет ответа, запустите Ollama:
ollama serve

# 2. Проверьте в новом терминале
curl http://localhost:11434/api/tags

# Должен вернуть JSON с моделями
```

**Если используете удаленный Ollama:**
```python
# В коде укажите правильный URL
async with OllamaClient(base_url="http://your-server:11434") as client:
    ...
```

### ❌ "Model not found"

**Симптомы:**
```
Model 'llama3.2' not found
```

**Решение:**
```bash
# Проверьте доступные модели
ollama list

# Если llama3.2 нет в списке, скачайте:
ollama pull llama3.2

# Проверьте снова
ollama list
```

### ❌ Ollama зависает или работает медленно

**Решение:**
```bash
# 1. Проверьте использование ресурсов
python examples/resource_optimization.py

# 2. Используйте меньшую модель
ollama pull llama3.2:1b  # 1 billion параметров вместо 3B

# 3. Или используйте quantized модель
ollama pull llama3.2:q4_0  # 4-bit quantization

# 4. Проверьте доступную память
# macOS/Linux:
free -h
# macOS:
vm_stat
```

### ❌ Ollama использует слишком много памяти

**Решение:**
```bash
# Остановите Ollama
pkill ollama

# Запустите с ограничением контекста
OLLAMA_NUM_GPU=0 ollama serve  # Отключить GPU
# или
OLLAMA_MAX_LOADED_MODELS=1 ollama serve  # Максимум 1 модель в памяти
```

## Проблемы с виртуальным окружением

### ❌ Windows: "cannot be loaded because running scripts is disabled"

**Симптомы:**
```
venv\Scripts\activate.ps1 cannot be loaded because running scripts is disabled on this system
```

**Решение:**
```powershell
# Запустите PowerShell от администратора
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Или используйте CMD вместо PowerShell
venv\Scripts\activate.bat
```

### ❌ "Permission denied" при активации (macOS/Linux)

**Решение:**
```bash
# Дайте права на выполнение
chmod +x venv/bin/activate

# Активируйте снова
source venv/bin/activate
```

### ❌ Виртуальное окружение не активируется

**Решение:**
```bash
# Удалите и создайте заново
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Проблемы с производительностью

### ⚠️ Медленная генерация текста

**Решение:**

1. **Проверьте используется ли GPU:**
```python
# Запустите
python examples/resource_optimization.py

# Ищите секцию "GPU Detection"
```

2. **Используйте меньшую модель:**
```bash
ollama pull llama3.2:1b  # Быстрее
```

3. **Настройте параметры генерации:**
```python
response = await client.generate(
    model="llama3.2",
    prompt="...",
    options={
        "num_predict": 100,  # Меньше токенов
        "temperature": 0.3,   # Более фокусированный вывод
    }
)
```

### ⚠️ Высокое использование памяти

**Решение:**
```python
# Включите мониторинг ресурсов
async with OllamaClient(enable_resource_monitoring=True) as client:
    # Используйте throttling
    usage = client.get_resource_usage()
    if usage['memory_percent'] > 85:
        print("Память заканчивается, подождите...")
        await asyncio.sleep(5)
```

## Проблемы с GPU

### ❌ NVIDIA GPU не определяется

**Симптомы:**
```python
gpu_usage: None
```

**Решение:**
```bash
# Установите pynvml
pip install pynvml

# Проверьте драйверы NVIDIA
nvidia-smi

# Если nvidia-smi не работает, обновите драйверы:
# https://www.nvidia.com/Download/index.aspx
```

### ❌ Apple Silicon: "GPU not detected"

**Примечание:** Apple Silicon использует unified memory, GPU мониторинг ограничен.

**Решение:**
```bash
# Ollama автоматически использует Apple Neural Engine
# Проверьте что Ollama использует Metal:
ollama run llama3.2 "test"
# В логах должно быть: "loaded model ... using metal"
```

## Проблемы с кодом

### ❌ "RuntimeError: Client not initialized"

**Причина:** Забыли использовать `async with` или `await client.__aenter__()`.

**Решение:**
```python
# ❌ Неправильно:
client = OllamaClient()
await client.generate(...)

# ✅ Правильно:
async with OllamaClient() as client:
    await client.generate(...)
```

### ❌ "Task was destroyed but it is pending"

**Причина:** Асинхронные задачи не завершены при выходе.

**Решение:**
```python
# Используйте try-finally
async with OllamaClient() as client:
    try:
        result = await client.generate(...)
    finally:
        # Cleanup автоматически
        pass
```

### ❌ Streaming не работает

**Решение:**
```python
# ✅ Правильный способ стриминга:
async with OllamaClient() as client:
    stream = await client.generate(
        model="llama3.2",
        prompt="...",
        stream=True
    )

    async for chunk in stream:
        if not chunk.done:
            print(chunk.response, end="", flush=True)
```

## Диагностика

### Запуск полной диагностики

Создайте файл `diagnose.py`:

```python
"""Диагностика AI CLI."""
import asyncio
import sys
import httpx

async def diagnose():
    print("=== AI CLI Диагностика ===\n")

    # 1. Python версия
    print(f"1. Python: {sys.version}")
    if sys.version_info < (3, 11):
        print("   ⚠️ Рекомендуется Python 3.11+")
    elif sys.version_info >= (3, 13):
        print("   ⚠️ Python 3.13+ может быть несовместим")
    else:
        print("   ✅ Версия Python подходит")

    # 2. Импорты
    print("\n2. Зависимости:")
    try:
        import httpx
        print(f"   ✅ httpx {httpx.__version__}")
    except ImportError as e:
        print(f"   ❌ httpx: {e}")

    try:
        import pydantic
        print(f"   ✅ pydantic {pydantic.__version__}")
    except ImportError as e:
        print(f"   ❌ pydantic: {e}")

    try:
        import psutil
        print(f"   ✅ psutil {psutil.__version__}")
    except ImportError as e:
        print(f"   ❌ psutil: {e}")

    try:
        import ai_cli
        print(f"   ✅ ai_cli {ai_cli.__version__}")
    except ImportError as e:
        print(f"   ❌ ai_cli: {e}")

    # 3. Ollama
    print("\n3. Ollama:")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                print(f"   ✅ Ollama работает ({len(models)} моделей)")
                for model in models:
                    print(f"      - {model['name']}")
            else:
                print(f"   ⚠️ Ollama ответил с кодом {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ollama не доступен: {e}")
        print("      Запустите: ollama serve")

    # 4. GPU
    print("\n4. GPU:")
    try:
        import pynvml
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        print(f"   ✅ NVIDIA GPU: {count} устройство(а)")
        for i in range(count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            print(f"      - {name}")
        pynvml.nvmlShutdown()
    except:
        print("   ⚠️ NVIDIA GPU не обнаружен или pynvml не установлен")

    print("\n=== Диагностика завершена ===")

asyncio.run(diagnose())
```

Запустите:
```bash
python diagnose.py
```

## Получение помощи

Если проблема не решена:

1. **Соберите информацию:**
```bash
python diagnose.py > diagnostic.txt
```

2. **Создайте issue** с diagnostic.txt и описанием проблемы

3. **Включите:**
   - Версию Python
   - ОС (macOS/Windows/Linux)
   - Полный текст ошибки
   - Что вы пытались сделать

---

**Большинство проблем решаются:**
1. Переустановкой виртуального окружения
2. Обновлением pip
3. Проверкой что Ollama запущен
