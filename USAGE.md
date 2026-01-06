# AI CLI - Руководство по использованию

## ✅ Ваш проект уже настроен!

Проект правильно упакован и готов к использованию как CLI-приложение.

## Быстрый старт

### 1. Установка (один раз)

```bash
# Перейдите в папку проекта
cd ~/IdeaProjects/ai-cli

# Запустите скрипт установки
./install.sh

# ИЛИ установите вручную:
source venv/bin/activate
pip install -e .
```

### 2. Запуск Ollama (каждый раз)

```bash
# В отдельном терминале
ollama serve

# В другом терминале скачайте модель (один раз)
ollama pull llama3.2
```

### 3. Использование

```bash
# Активируйте окружение
source venv/bin/activate

# Проверьте установку
which ai-cli
# Вывод: /Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli

# Справка
ai-cli --help

# Список моделей
ai-cli --models

# Быстрый запрос
ai-cli "explain python decorators"

# С выбором модели
ai-cli --model llama3.2 "write a fibonacci function"

# Интерактивный режим
ai-cli chat

# Мультиагентный режим
ai-cli team "build a REST API"
```

## Все доступные команды

### Быстрый запрос

```bash
ai-cli "произвольный текст"
```

Примеры:

```bash
ai-cli "what is async/await in python"
ai-cli "create a docker-compose for postgres"
ai-cli "explain REST API best practices"
```

### Выбор модели

```bash
ai-cli --model <model-name> "your question"
```

Примеры:

```bash
ai-cli --model llama3.2 "explain decorators"
ai-cli --model codellama "write a sorting algorithm"
ai-cli -m mistral "what is machine learning"
```

### Список моделей

```bash
ai-cli --models
```

Вывод:

```
Available models:
------------------------------------------------------------
  llama3.2                       (2.00 GB)
  codellama                      (3.80 GB)
```

### Интерактивный режим (чат)

```bash
ai-cli chat
```

ИЛИ просто:

```bash
ai-cli
```

### Мультиагентный режим

```bash
ai-cli team "your task"
```

Пример:

```bash
ai-cli team "build a REST API for todo app"
```

### Версия

```bash
ai-cli --version
# Вывод: ai-cli 0.1.0
```

### Справка

```bash
ai-cli --help
ai-cli -h
```

## Использование без активации venv

### Вариант 1: Создать алиас (рекомендуется)

Добавьте в `~/.zshrc`:

```bash
alias ai-cli='/Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli'
```

Затем:

```bash
source ~/.zshrc
ai-cli "your question"  # работает из любой папки!
```

### Вариант 2: Создать симлинк

```bash
sudo ln -s /Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli /usr/local/bin/ai-cli
```

Теперь `ai-cli` доступен глобально:

```bash
ai-cli "your question"  # работает везде!
```

## Примеры использования

### Вопросы о программировании

```bash
ai-cli "difference between list and tuple in python"
ai-cli "how does garbage collection work in python"
ai-cli "explain MVC pattern"
```

### Генерация кода

```bash
ai-cli "write a function to validate email"
ai-cli "create a REST endpoint for user login"
ai-cli "generate unit tests for a factorial function"
```

### Отладка

```bash
ai-cli "why does this raise TypeError: [код]"
ai-cli "optimize this slow query: SELECT * FROM..."
```

### Многословные запросы

```bash
ai-cli "I need to create a Python function that reads a CSV file,
filters rows where column 'age' is greater than 18,
and returns the count of unique values in the 'city' column"
```

## Ежедневный workflow

### Шаг 1: Запустите Ollama

```bash
# В отдельном терминале (оставьте его открытым)
ollama serve
```

### Шаг 2: Используйте ai-cli

**С активацией venv:**

```bash
cd ~/IdeaProjects/ai-cli
source venv/bin/activate
ai-cli "your question"
```

**С алиасом (без активации):**

```bash
# Из любой папки
ai-cli "your question"
```

### Шаг 3: Завершение работы

```bash
# Деактивируйте venv (если активировали)
deactivate

# Ollama можно оставить запущенным или остановить
# Ctrl+C в терминале где запущен ollama serve
```

## Структура команды

```
ai-cli [OPTIONS] [QUERY]
```

### OPTIONS:

- `--help`, `-h` - Показать справку
- `--version`, `-v` - Показать версию
- `--models` - Список доступных моделей
- `--model <name>`, `-m <name>` - Выбрать модель
- `--ollama-url <url>` - URL Ollama сервера (по умолчанию: http://localhost:11434)

### QUERY:

- Произвольный текст в кавычках
- Специальные команды: `chat`, `team "<task>"`

## Продвинутое использование

### Использовать другой Ollama сервер

```bash
ai-cli --ollama-url http://192.168.1.100:11434 "your question"
```

### Использовать меньшую модель для скорости

```bash
# Скачайте маленькую модель
ollama pull llama3.2:1b

# Используйте её
ai-cli --model llama3.2:1b "quick question"
```

### Использовать модель для кода

```bash
ollama pull codellama
ai-cli --model codellama "write a binary search algorithm"
```

## Возможные проблемы

### "ai-cli: command not found"

**Решение:**

```bash
# Проверьте что venv активирован
source venv/bin/activate
which ai-cli

# ИЛИ используйте полный путь
./venv/bin/ai-cli "question"

# ИЛИ создайте алиас (см. выше)
```

### "Connection refused" или "Error: ..."

**Решение:**

```bash
# Проверьте что Ollama запущен
curl http://localhost:11434/api/tags

# Если не работает, запустите:
ollama serve
```

### "Model not found"

**Решение:**

```bash
# Скачайте модель
ollama pull llama3.2

# Проверьте список
ollama list
```

### Медленная работа

**Решение:**

```bash
# Используйте меньшую модель
ollama pull llama3.2:1b
ai-cli --model llama3.2:1b "question"
```

## Как это работает

1. **setup.py** определяет entry point:
   ```python
   entry_points={
       "console_scripts": [
           "ai-cli=ai_cli.cli:main",
       ],
   }
   ```

2. **pip install -e .** создает исполняемый файл `venv/bin/ai-cli`

3. При вызове `ai-cli` запускается функция `main()` из модуля `ai_cli.cli`

4. **argparse** обрабатывает аргументы командной строки

5. CLI подключается к Ollama и отправляет запросы

## Обновление

```bash
cd ~/IdeaProjects/ai-cli
source venv/bin/activate
git pull
pip install -e . --force-reinstall
```

## Удаление

```bash
# Деактивируйте venv
deactivate

# Удалите папку проекта
rm -rf ~/IdeaProjects/ai-cli

# Удалите алиас из ~/.zshrc (если создавали)
# Удалите симлинк (если создавали)
sudo rm /usr/local/bin/ai-cli
```

## Дополнительные файлы

- `QUICKSTART_CLI.md` - Подробное руководство
- `INSTALL.md` - Инструкции по установке
- `README.md` - Общая документация
- `examples/` - Примеры использования API

---

**Готово!** Теперь вы можете использовать `ai-cli "ваш вопрос"` из командной строки.
