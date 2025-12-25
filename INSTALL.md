# Пошаговая инструкция по установке AI CLI

Это руководство для тех, кто впервые работает с Python проектами.

## 1. Проверка и установка Python

### Шаг 1.1: Проверьте текущую версию Python

Откройте терминал (командную строку) и выполните:

```bash
python --version
```

Если команда не найдена, попробуйте:

```bash
python3 --version
```

**Что вы должны увидеть:**
- ✅ `Python 3.11.x` или `Python 3.12.x` - отлично, переходите к шагу 2
- ⚠️ `Python 3.13.x` или выше - нужно установить Python 3.12
- ❌ `Python 3.10.x` или ниже - нужно обновить до Python 3.11 или 3.12
- ❌ Команда не найдена - нужно установить Python

### Шаг 1.2: Установка рекомендованной версии Python (если нужно)

**macOS:**
```bash
# Установите Homebrew (если еще не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установите Python 3.12
brew install python@3.12

# Проверьте установку
python3.12 --version
```

**Windows:**
1. Перейдите на [python.org/downloads](https://www.python.org/downloads/)
2. Скачайте **Python 3.12.x** (не последнюю версию!)
3. При установке **обязательно отметьте** "Add Python to PATH"
4. Нажмите "Install Now"
5. После установки откройте новый терминал и проверьте: `python --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
python3.12 --version
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install python3.12
python3.12 --version
```

## 2. Установка и запуск Ollama

Ollama - это сервер для запуска локальных AI моделей.

### Шаг 2.1: Установка Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
1. Скачайте установщик с [ollama.ai/download](https://ollama.ai/download)
2. Запустите установщик
3. Ollama автоматически запустится как сервис

**Альтернативный способ (Docker):**
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Шаг 2.2: Запуск Ollama

**macOS/Linux:**
```bash
# Запустите Ollama сервер
ollama serve
```

Откроется сервер на `http://localhost:11434`

**Windows:**
Ollama запускается автоматически после установки. Проверьте иконку в системном трее.

### Шаг 2.3: Скачивание модели

Откройте **новый терминал** (не закрывая тот где запущен `ollama serve`) и выполните:

```bash
# Скачайте модель llama3.2 (около 2GB)
ollama pull llama3.2

# Проверьте что модель скачалась
ollama list
```

Вы должны увидеть `llama3.2` в списке.

### Шаг 2.4: Проверка что Ollama работает

```bash
# Проверьте что API работает
curl http://localhost:11434/api/tags

# Должен вернуть JSON список моделей
```

Или откройте в браузере: `http://localhost:11434`

## 3. Установка AI CLI

### Шаг 3.1: Скачивание проекта

**Если у вас уже есть папка проекта:**
```bash
cd /путь/к/ai-cli
```

**Если нужно клонировать из Git:**
```bash
git clone <url-репозитория>
cd ai-cli
```

### Шаг 3.2: Создание виртуального окружения

**Что такое виртуальное окружение?**
Это отдельная папка для Python библиотек вашего проекта. Зачем нужно:
- Не засоряет систему
- Избегает конфликтов версий с другими проектами
- Легко удалить все зависимости (просто удалить папку `venv`)

```bash
# Создайте виртуальное окружение с именем "venv"
python3.12 -m venv venv

# Если python3.12 не найден, используйте python3 или python
python3 -m venv venv
```

Вы увидите новую папку `venv/` в вашем проекте.

### Шаг 3.3: Активация виртуального окружения

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Как понять что окружение активировано?**
В начале строки терминала появится `(venv)`:
```
(venv) user@computer:~/ai-cli$
```

### Шаг 3.4: Обновление pip

```bash
# Обязательно обновите pip до последней версии
pip install --upgrade pip
```

### Шаг 3.5: Установка зависимостей

```bash
# Установите основные зависимости
pip install -r requirements.txt

# Установите сам пакет ai_cli
pip install -e .

# Дождитесь завершения (может занять 1-2 минуты)
```

**Опциональные зависимости:**

Для работы с GGUF моделями напрямую (llama.cpp):
```bash
pip install llama-cpp-python
```

Для мониторинга NVIDIA GPU:
```bash
pip install pynvml
```

### Шаг 3.6: Проверка установки

```bash
# Проверьте что все установлено
python -c "import ai_cli; print('✓ AI CLI готов к работе!')"
```

Если увидели "✓ AI CLI готов к работе!" - все отлично!

## 4. Первый запуск

### Тест 1: Базовый пример

```bash
python examples/basic_usage.py
```

Вы должны увидеть ответы от AI модели.

### Тест 2: Интерактивный режим

```bash
python -m ai_cli.cli chat
```

Теперь можете общаться с AI в терминале! Введите вопрос и нажмите Enter.

### Тест 3: Мультиагентная система

```bash
python examples/multi_agent.py
```

Увидите как несколько AI агентов работают над одной задачей.

## 5. Ежедневное использование

### Как начать работу каждый раз:

```bash
# 1. Убедитесь что Ollama запущен
curl http://localhost:11434/api/tags

# Если не работает, запустите:
ollama serve  # macOS/Linux
# Windows: проверьте иконку в трее

# 2. Перейдите в папку проекта
cd /путь/к/ai-cli

# 3. Активируйте виртуальное окружение
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 4. Запускайте примеры или свой код
python examples/basic_usage.py
```

### Как закончить работу:

```bash
# Деактивируйте виртуальное окружение
deactivate
```

## Возможные проблемы и решения

### Проблема: "ModuleNotFoundError: No module named 'ai_cli'"

**Решение:**
1. Убедитесь что виртуальное окружение активировано (видите `(venv)`)
2. Переустановите зависимости: `pip install -r requirements.txt`

### Проблема: "Connection refused" при запросе к Ollama

**Решение:**
1. Проверьте что Ollama запущен: `ollama serve`
2. Проверьте порт: `curl http://localhost:11434/api/tags`
3. Если используете Docker, проверьте контейнер: `docker ps`

### Проблема: "python: command not found"

**Решение:**
1. Попробуйте `python3` вместо `python`
2. Установите Python (см. Шаг 1.2)

### Проблема: Медленная работа

**Решение:**
1. Убедитесь что используете GPU если доступен
2. Используйте меньшую модель: `ollama pull llama3.2:1b`
3. Проверьте доступную память: `python examples/resource_optimization.py`

### Проблема: "Permission denied" на macOS/Linux

**Решение:**
```bash
# Дайте права на выполнение
chmod +x venv/bin/activate
```

### Проблема: Windows блокирует выполнение скриптов

**Решение:**
```powershell
# Запустите PowerShell от администратора
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Дополнительная помощь

- **Документация Ollama**: https://ollama.ai/docs
- **Python виртуальные окружения**: https://docs.python.org/3/tutorial/venv.html
- **Issues проекта**: https://github.com/your-repo/ai-cli/issues

## Обновление проекта

```bash
# Активируйте окружение
source venv/bin/activate

# Получите последние изменения (если используете Git)
git pull

# Обновите зависимости
pip install --upgrade -r requirements.txt

# Проверьте что все работает
python examples/basic_usage.py
```

## Удаление

Если хотите полностью удалить AI CLI:

```bash
# Деактивируйте окружение
deactivate

# Удалите папку проекта
rm -rf /путь/к/ai-cli

# Удалите Ollama (опционально)
# macOS:
brew uninstall ollama

# Linux:
sudo rm -rf /usr/local/bin/ollama ~/.ollama
```

---

**Готово!** Теперь вы можете начать работу с AI CLI. Начните с `examples/basic_usage.py` и изучайте другие примеры.
