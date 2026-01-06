# AI CLI - Быстрый старт

## Установка (macOS)

### 1. Автоматическая установка

```bash
# Клонируйте репозиторий (если еще не сделано)
git clone <url-репозитория>
cd ai-cli

# Запустите скрипт установки
./install.sh
```

### 2. Ручная установка

```bash
# Создайте виртуальное окружение
python3.12 -m venv venv

# Активируйте окружение
source venv/bin/activate

# Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Установите ai-cli
pip install -e .

# Проверьте установку
which ai-cli
ai-cli --version
```

## Проверка установки

```bash
# Активируйте окружение (если не активировано)
source venv/bin/activate

# Проверьте что команда доступна
which ai-cli
# Должен вывести: /Users/.../ai-cli/venv/bin/ai-cli

# Посмотрите справку
ai-cli --help
```

## Запуск Ollama

```bash
# В отдельном терминале запустите Ollama
ollama serve

# В другом терминале скачайте модель
ollama pull llama3.2

# Проверьте доступные модели
ollama list
```

## Использование

### 1. Быстрый запрос (рекомендуется)

```bash
# Активируйте окружение
source venv/bin/activate

# Задайте вопрос
ai-cli "explain python decorators"

# С выбором модели
ai-cli --model llama3.2 "write a function to calculate fibonacci"

# Генерация кода
ai-cli "create a REST API endpoint for user registration"
```

### 2. Список доступных моделей

```bash
ai-cli --models
```

Вывод:
```
Available models:
------------------------------------------------------------
  llama3.2                       (2.00 GB)
  codellama                      (3.80 GB)
  mistral                        (4.10 GB)
```

### 3. Интерактивный режим (чат)

```bash
ai-cli chat
```

Или просто:

```bash
ai-cli
```

Вы войдете в режим чата:

```
AI CLI - Interactive Mode
Type 'exit' to quit, 'help' for commands
------------------------------------------------------------

You: explain async/await in python
Assistant: [ответ AI]

You: exit
Goodbye!
```

### 4. Мультиагентный режим

```bash
ai-cli team "build a REST API for a todo application"
```

Несколько AI-агентов будут работать над задачей вместе.

## Опции командной строки

```bash
ai-cli --help              # Показать справку
ai-cli --version           # Показать версию
ai-cli --models            # Список моделей
ai-cli --model <name>      # Выбрать модель
ai-cli --ollama-url <url>  # Указать URL Ollama (по умолчанию: http://localhost:11434)
```

## Примеры использования

### Вопросы о программировании

```bash
ai-cli "what is the difference between list and tuple in python"
ai-cli "explain REST API best practices"
ai-cli "how to handle errors in async python"
```

### Генерация кода

```bash
ai-cli "write a python function to validate email addresses"
ai-cli "create a docker-compose file for postgres and redis"
ai-cli "generate unit tests for a factorial function"
```

### Отладка кода

```bash
ai-cli "why does this code raise AttributeError: [вставить код]"
ai-cli "optimize this slow database query: [вставить код]"
```

### Использование другой модели

```bash
# Используйте более быструю модель
ai-cli --model llama3.2:1b "simple question"

# Используйте модель для кода
ai-cli --model codellama "write a sorting algorithm"
```

## Ежедневный workflow

### Начало работы

```bash
# 1. Перейдите в папку проекта
cd ~/IdeaProjects/ai-cli

# 2. Активируйте виртуальное окружение
source venv/bin/activate

# Теперь команда ai-cli доступна
ai-cli "your question here"
```

### Завершение работы

```bash
# Деактивируйте окружение
deactivate
```

## Установка глобально (опционально)

Если хотите использовать `ai-cli` без активации окружения:

### Вариант 1: Создать алиас

Добавьте в `~/.zshrc` или `~/.bashrc`:

```bash
alias ai-cli='/Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli'
```

Перезагрузите терминал:

```bash
source ~/.zshrc  # или source ~/.bashrc
```

Теперь можете использовать `ai-cli` из любой папки:

```bash
ai-cli "your question"
```

### Вариант 2: Симлинк в PATH

```bash
# Создайте симлинк (замените путь на свой)
sudo ln -s /Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli /usr/local/bin/ai-cli

# Проверьте
which ai-cli
ai-cli --version
```

### Вариант 3: Установить в системный Python (не рекомендуется)

```bash
# Деактивируйте venv
deactivate

# Установите глобально
pip3 install -e .

# Теперь ai-cli доступен везде
ai-cli "test query"
```

**⚠️ Внимание**: Установка в системный Python может привести к конфликтам зависимостей.

## Конфигурация

Создайте файл `~/.ai-cli.conf` для настроек по умолчанию:

```ini
[default]
model = llama3.2
ollama_url = http://localhost:11434
```

## Возможные проблемы

### Проблема: "ai-cli: command not found"

**Решение 1**: Активируйте окружение
```bash
source venv/bin/activate
which ai-cli
```

**Решение 2**: Используйте полный путь
```bash
./venv/bin/ai-cli "your question"
```

**Решение 3**: Создайте алиас (см. выше)

### Проблема: "Connection refused"

**Решение**: Убедитесь что Ollama запущен
```bash
# Проверьте статус
curl http://localhost:11434/api/tags

# Если не работает, запустите
ollama serve
```

### Проблема: "Model not found"

**Решение**: Скачайте модель
```bash
ollama pull llama3.2
ollama list
```

### Проблема: Медленная работа

**Решение**: Используйте меньшую модель
```bash
ollama pull llama3.2:1b
ai-cli --model llama3.2:1b "your question"
```

## Обновление

```bash
# Активируйте окружение
source venv/bin/activate

# Получите последние изменения
git pull

# Обновите зависимости
pip install --upgrade -r requirements.txt

# Переустановите пакет
pip install -e .
```

## Удаление

```bash
# Деактивируйте окружение
deactivate

# Удалите папку проекта
rm -rf ~/IdeaProjects/ai-cli

# Удалите алиас из ~/.zshrc (если создавали)
# Удалите симлинк (если создавали)
sudo rm /usr/local/bin/ai-cli
```

## Дополнительные ресурсы

- Полная документация: [README.md](README.md)
- Подробная установка: [INSTALL.md](INSTALL.md)
- Примеры использования: папка `examples/`
- Решение проблем: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Поддержка

Если возникли проблемы:

1. Проверьте что Ollama запущен: `curl http://localhost:11434/api/tags`
2. Проверьте что окружение активировано: `which ai-cli`
3. Проверьте логи: `ai-cli --help`
4. Создайте issue на GitHub

---

**Готово!** Теперь вы можете использовать `ai-cli` из командной строки.
