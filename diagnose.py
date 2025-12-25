#!/usr/bin/env python3
"""Диагностика AI CLI для решения проблем."""

import asyncio
import sys
import platform

async def diagnose():
    """Запуск полной диагностики системы."""
    print("=" * 60)
    print("AI CLI - Диагностика системы")
    print("=" * 60)

    # 1. Информация о системе
    print("\n1. Система:")
    print(f"   ОС: {platform.system()} {platform.release()}")
    print(f"   Архитектура: {platform.machine()}")
    print(f"   Python: {sys.version}")

    python_version = sys.version_info
    if python_version < (3, 11):
        print("   ⚠️  ВНИМАНИЕ: Рекомендуется Python 3.11 или 3.12")
    elif python_version >= (3, 13):
        print("   ⚠️  ВНИМАНИЕ: Python 3.13+ может быть несовместим с некоторыми зависимостями")
    else:
        print(f"   ✅ Версия Python подходит ({python_version.major}.{python_version.minor})")

    # 2. Проверка зависимостей
    print("\n2. Зависимости:")

    dependencies = {
        "httpx": "httpx",
        "pydantic": "pydantic",
        "psutil": "psutil",
        "ai_cli": "ai_cli"
    }

    for name, module in dependencies.items():
        try:
            mod = __import__(module)
            version = getattr(mod, "__version__", "unknown")
            print(f"   ✅ {name}: {version}")
        except ImportError as e:
            print(f"   ❌ {name}: не установлен ({e})")

    # 3. Опциональные зависимости
    print("\n3. Опциональные зависимости:")

    try:
        import pynvml
        print(f"   ✅ pynvml: установлен (мониторинг NVIDIA GPU)")
    except ImportError:
        print(f"   ⚠️  pynvml: не установлен (мониторинг NVIDIA GPU недоступен)")

    try:
        import llama_cpp
        print(f"   ✅ llama-cpp-python: установлен (поддержка GGUF)")
    except ImportError:
        print(f"   ⚠️  llama-cpp-python: не установлен (GGUF модели недоступны)")

    # 4. Проверка Ollama
    print("\n4. Ollama сервер:")

    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    models = data.get("models", [])
                    print(f"   ✅ Ollama работает (порт 11434)")
                    print(f"   ✅ Доступно моделей: {len(models)}")

                    if models:
                        print("\n   Установленные модели:")
                        for model in models[:5]:  # Показываем первые 5
                            name = model.get("name", "unknown")
                            size = model.get("size", 0)
                            size_gb = size / (1024**3) if size else 0
                            print(f"      - {name} ({size_gb:.2f} GB)")

                        if len(models) > 5:
                            print(f"      ... и еще {len(models) - 5} модель(ей)")
                    else:
                        print("   ⚠️  Нет установленных моделей")
                        print("      Установите модель: ollama pull llama3.2")
                else:
                    print(f"   ⚠️  Ollama ответил с кодом {response.status_code}")

            except httpx.ConnectError:
                print("   ❌ Не удалось подключиться к Ollama")
                print("      Запустите Ollama: ollama serve")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

    except ImportError:
        print("   ❌ httpx не установлен, невозможно проверить Ollama")

    # 5. Проверка GPU
    print("\n5. GPU:")

    gpu_found = False

    # NVIDIA GPU
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()

        if device_count > 0:
            gpu_found = True
            print(f"   ✅ NVIDIA GPU: {device_count} устройство(а)")

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                memory_total_gb = memory.total / (1024**3)

                print(f"\n      GPU {i}: {name}")
                print(f"         Память: {memory_total_gb:.2f} GB")

                try:
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    print(f"         Использование GPU: {util.gpu}%")
                    print(f"         Использование памяти: {util.memory}%")
                except:
                    pass

        pynvml.nvmlShutdown()

    except ImportError:
        print("   ⚠️  pynvml не установлен - мониторинг NVIDIA GPU недоступен")
    except Exception as e:
        print(f"   ⚠️  Ошибка при проверке NVIDIA GPU: {e}")

    # Apple Silicon
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        gpu_found = True
        print("   ✅ Apple Silicon (M1/M2/M3) обнаружен")
        print("      GPU встроен (unified memory)")

    if not gpu_found:
        print("   ⚠️  GPU не обнаружен - будет использован CPU")

    # 6. Проверка ресурсов
    print("\n6. Системные ресурсы:")

    try:
        import psutil

        # Память
        memory = psutil.virtual_memory()
        memory_total_gb = memory.total / (1024**3)
        memory_available_gb = memory.available / (1024**3)
        memory_percent = memory.percent

        print(f"   Память:")
        print(f"      Всего: {memory_total_gb:.2f} GB")
        print(f"      Доступно: {memory_available_gb:.2f} GB")
        print(f"      Использовано: {memory_percent:.1f}%")

        if memory_available_gb < 4:
            print("      ⚠️  Мало доступной памяти (<4GB)")
        elif memory_available_gb < 8:
            print("      ⚠️  Рекомендуется 8GB+ для комфортной работы")
        else:
            print("      ✅ Достаточно памяти")

        # CPU
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)

        print(f"\n   CPU:")
        print(f"      Ядер: {cpu_count}")
        print(f"      Использование: {cpu_percent:.1f}%")

    except ImportError:
        print("   ❌ psutil не установлен")

    # 7. Виртуальное окружение
    print("\n7. Виртуальное окружение:")

    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Виртуальное окружение активировано")
        print(f"      Путь: {sys.prefix}")
    else:
        print("   ⚠️  Виртуальное окружение НЕ активировано")
        print("      Рекомендуется использовать venv")

    # Итоги
    print("\n" + "=" * 60)
    print("Диагностика завершена")
    print("=" * 60)

    print("\nСледующие шаги:")

    # Проверяем что нужно исправить
    issues = []

    if python_version < (3, 11) or python_version >= (3, 13):
        issues.append("• Установите Python 3.11 или 3.12")

    try:
        import ai_cli
    except ImportError:
        issues.append("• Установите зависимости: pip install -r requirements.txt")

    try:
        import httpx
        async with httpx.AsyncClient(timeout=3.0) as client:
            await client.get("http://localhost:11434/api/tags")
    except:
        issues.append("• Запустите Ollama: ollama serve")

    if issues:
        print("\n⚠️  Обнаружены проблемы:")
        for issue in issues:
            print(f"   {issue}")
        print("\nПодробнее: см. TROUBLESHOOTING.md")
    else:
        print("\n✅ Все проверки пройдены! Система готова к работе.")
        print("\nПопробуйте:")
        print("   python examples/basic_usage.py")

    print("\nДля получения помощи:")
    print("   - README.md - обзор проекта")
    print("   - INSTALL.md - детальная установка")
    print("   - TROUBLESHOOTING.md - решение проблем")


if __name__ == "__main__":
    try:
        asyncio.run(diagnose())
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем")
    except Exception as e:
        print(f"\n\nОшибка при диагностике: {e}")
        import traceback
        traceback.print_exc()
