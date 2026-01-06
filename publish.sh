#!/bin/bash

# Скрипт для публикации пакета ai-cli в PyPI

set -e

# Активация venv если он существует
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Проверка и установка зависимостей
if ! python -m pip show build > /dev/null 2>&1; then
    echo "📥 Установка build и twine..."
    python -m pip install build twine
fi

echo "🧹 Очистка старых сборок..."
rm -rf build/ dist/ *.egg-info/

echo "📦 Сборка пакета..."
python -m build

echo "✅ Проверка пакета..."
twine check dist/*

echo "📤 Публикация в PyPI..."
echo "Используйте: twine upload dist/*"
echo ""
echo "Для тестового PyPI: twine upload --repository testpypi dist/*"
echo "Для основного PyPI: twine upload dist/*"
