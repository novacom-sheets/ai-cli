# AI CLI - Шпаргалка

## Быстрый старт

```bash
# Активируйте окружение (если нужно)
source ~/IdeaProjects/ai-cli/venv/bin/activate

# ИЛИ используйте алиас (уже настроен)
ai-cli --help
```

## Основные команды

### Быстрые запросы

```bash
ai-cli "explain python decorators"
ai-cli "what is the difference between list and tuple"
ai-cli "how to handle async errors in python"
```

### Генерация кода (в консоль)

```bash
ai-cli "write fibonacci function"
ai-cli "create REST API endpoint"
ai-cli "explain this code: [вставить код]"
```

### Генерация файлов ⭐ НОВОЕ

```bash
# Автосохранение (определяет имя файла из запроса)
ai-cli -s "Напиши HELLO-WORLD.md"
ai-cli -s "create config.py"
ai-cli -s "write README.md"

# Явное имя файла
ai-cli -o result.md "explain decorators"
ai-cli -o script.py "write web scraper"

# Только код (без пояснений)
ai-cli -s -c "create fibonacci.py"
ai-cli -o app.py -c "write flask server"
```

### Выполнение команд 🔥 НОВОЕ

```bash
# С подтверждением (безопасно)
ai-cli -x "как показать все файлы"
ai-cli -x "покажи свободное место на диске"
ai-cli -x "найди все Python файлы"

# С автоподтверждением (осторожно!)
ai-cli -x -y "create backup directory"
ai-cli -xy "show system info"

# Комбинирование с другими опциями
ai-cli -x -o howto.md "docker debugging commands"
```

### Выбор модели

```bash
ai-cli --models                           # Список моделей
ai-cli -m llama3.2 "simple question"      # Быстрая модель
ai-cli -m deepseek-r1:8b "complex task"   # Мощная модель
```

### Интерактивный режим

```bash
ai-cli chat    # Чат-режим
ai-cli         # То же самое (по умолчанию)
```

### Мультиагентный режим

```bash
ai-cli team "build REST API for todo app"
```

## Опции

| Опция | Короткая | Описание |
|-------|----------|----------|
| `--help` | `-h` | Показать справку |
| `--version` | `-v` | Показать версию |
| `--models` | - | Список моделей |
| `--model NAME` | `-m` | Выбрать модель |
| `--output FILE` | `-o` | Сохранить в файл |
| `--auto-save` | `-s` | Автоопределение имени файла |
| `--extract-code` | `-c` | Извлечь только код |
| `--execute` | `-x` | 🔥 Выполнить команды с подтверждением |
| `--yes` | `-y` | ⚠️ Автоподтверждение команд |
| `--ollama-url URL` | - | URL Ollama сервера |

## Примеры по категориям

### Python разработка

```bash
# Генерация кода
ai-cli -s -c "create main.py with argparse"
ai-cli -s -c "write utils.py with helper functions"

# Тесты
ai-cli -o test_app.py -c "write pytest for calculator"

# Конфиг
ai-cli -s "create setup.py for package"
ai-cli -s "write requirements.txt"
```

### Web разработка

```bash
ai-cli -s -c "create index.html with bootstrap"
ai-cli -s -c "write app.js with API calls"
ai-cli -s -c "create style.css"
```

### DevOps

```bash
ai-cli -s "create Dockerfile for python app"
ai-cli -s "write docker-compose.yml"
ai-cli -s "create deploy.sh script"
```

### Документация

```bash
ai-cli -s "write README.md for CLI tool"
ai-cli -s "create API.md with endpoints"
ai-cli -s "write CONTRIBUTING.md"
```

## Полезные комбинации

```bash
# Быстрая генерация + форматирование
ai-cli -s -c "create app.py" && black app.py

# Генерация + проверка
ai-cli -s -c "create script.py" && python -m py_compile script.py

# Генерация + git add
ai-cli -s "create README.md" && git add README.md

# Множественная генерация
ai-cli -s -c "create main.py" && \
ai-cli -s "create README.md" && \
ai-cli -s "create requirements.txt"
```

## Запуск Ollama

```bash
# Проверить статус
curl -s http://localhost:11434/api/tags | head -5

# Запустить вручную
ollama serve

# Автозапуск (один раз)
brew services start ollama

# Список моделей
ollama list

# Скачать модель
ollama pull llama3.2
```

## Управление моделями

```bash
# Список доступных
ai-cli --models

# Установить по умолчанию
ai-cli -m llama3.2 "query"

# Скачать новую
ollama pull codellama
ai-cli -m codellama "write algorithm"
```

## Частые задачи

### Создать новый проект

```bash
mkdir my-project && cd my-project
ai-cli -s "create README.md for python CLI tool"
ai-cli -s -c "create main.py with argparse"
ai-cli -s "write requirements.txt"
ai-cli -s "create .gitignore for python"
```

### Генерация тестов

```bash
# Создать код
ai-cli -o calculator.py -c "write calculator class"

# Создать тесты
ai-cli -o test_calculator.py -c "write pytest tests"

# Запустить
pytest
```

### Быстрое прототипирование

```bash
ai-cli -s -c "create prototype.py with basic structure"
python prototype.py
```

## Решение проблем

```bash
# ai-cli не найден?
source ~/.zshrc
which ai-cli

# Ollama не доступен?
ollama serve

# Модель не найдена?
ollama pull llama3.2
ollama list

# Медленно?
ai-cli -m llama3.2:1b "query"  # используйте меньшую модель
```

## Горячие клавиши в chat режиме

```
exit / quit    - Выход
help           - Справка
Ctrl+C         - Прервать
```

## Алиас настроен

```bash
# Работает из любой папки
cd ~/Documents
ai-cli "your question"

# Алиас указывает на:
/Users/alexyakovlev919gmail.com/IdeaProjects/ai-cli/venv/bin/ai-cli
```

## Ресурсы

- `USAGE.md` - Полное руководство
- `FILE_GENERATION.md` - Генерация файлов
- `QUICKSTART_CLI.md` - Быстрый старт
- `INSTALL.md` - Установка
- `examples/` - Примеры кода

---

**Совет дня**: Используйте `-s -c` для быстрой генерации исполняемого кода:
```bash
ai-cli -s -c "create your_script.py with functionality"
```
