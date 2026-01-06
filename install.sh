#!/bin/bash
# Скрипт установки AI CLI для macOS/Linux

set -e  # Остановка при ошибке

echo "=================================================="
echo "  AI CLI - Установка"
echo "=================================================="
echo ""

# Проверка Python
echo "Проверка Python..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Ошибка: Python 3.11+ не найден"
    echo "Установите Python: brew install python@3.12"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Найден Python $PYTHON_VERSION"

# Проверка Ollama
echo ""
echo "Проверка Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama не найден"
    echo "Установить сейчас? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Установка Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "Пропуск установки Ollama"
    fi
else
    echo "✓ Ollama установлен"
fi

# Создание виртуального окружения
echo ""
echo "Создание виртуального окружения..."
if [ -d "venv" ]; then
    echo "⚠️  venv уже существует, пропуск"
else
    $PYTHON_CMD -m venv venv
    echo "✓ Создано виртуальное окружение"
fi

# Активация виртуального окружения
echo ""
echo "Активация виртуального окружения..."
source venv/bin/activate

# Обновление pip
echo ""
echo "Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
echo ""
echo "Установка зависимостей..."
pip install -r requirements.txt

# Установка пакета
echo ""
echo "Установка ai-cli..."
pip install -e .

# Проверка установки
echo ""
echo "Проверка установки..."
if command -v ai-cli &> /dev/null; then
    echo "✓ ai-cli установлен успешно!"
    echo ""
    echo "Путь: $(which ai-cli)"
else
    echo "❌ Ошибка: ai-cli не найден в PATH"
    echo ""
    echo "Попробуйте:"
    echo "  source venv/bin/activate"
    echo "  which ai-cli"
fi

echo ""
echo "=================================================="
echo "  Установка завершена!"
echo "=================================================="
echo ""
echo "Для использования:"
echo "  1. Активируйте окружение: source venv/bin/activate"
echo "  2. Запустите Ollama: ollama serve (в отдельном терминале)"
echo "  3. Скачайте модель: ollama pull llama3.2"
echo "  4. Используйте CLI: ai-cli --help"
echo ""
echo "Примеры использования:"
echo '  ai-cli "explain python decorators"'
echo '  ai-cli --models'
echo '  ai-cli chat'
echo ""
