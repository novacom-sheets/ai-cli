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

# Проверка наличия токена
if [ -z "$PYPI_TOKEN" ]; then
    echo "⚠️  Переменная PYPI_TOKEN не установлена"
    echo ""
    echo "Установите токен: export PYPI_TOKEN='ваш_токен'"
    echo "Или введите токен при запросе twine"
    echo ""
    echo "Для тестового PyPI: twine upload --repository testpypi dist/*"
    echo "Для основного PyPI: twine upload dist/*"
    echo ""
    read -p "Продолжить публикацию? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    twine upload dist/*
else
    echo "✅ Токен найден, публикация..."
    twine upload --username __token__ --password "$PYPI_TOKEN" dist/*
fi
