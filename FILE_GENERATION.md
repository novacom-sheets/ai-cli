# Генерация файлов с AI CLI

AI CLI теперь может автоматически сохранять результаты в файлы!

## Три способа сохранения

### 1. Автоматическое сохранение (--auto-save / -s)

CLI автоматически определит имя файла из вашего запроса:

```bash
ai-cli --auto-save "Напиши HELLO-WORLD.md"
ai-cli -s "create config.json"
ai-cli -s "write README.md"
```

**Результат:**
- ✓ Автоматически создаст файл `HELLO-WORLD.md`
- ✓ Покажет путь к созданному файлу
- ✓ Выведет превью содержимого

### 2. Явное указание файла (--output / -o)

Укажите точное имя выходного файла:

```bash
ai-cli --output result.md "explain python decorators"
ai-cli -o script.py "write a web scraper"
ai-cli -o config.yaml "create kubernetes deployment config"
```

**Результат:**
- ✓ Сохранит ответ в указанный файл
- ✓ Можно указать путь: `ai-cli -o ~/Documents/result.md "..."`

### 3. Извлечение только кода (--extract-code / -c)

Сохраняет только код, без пояснительного текста:

```bash
ai-cli -o fibonacci.py -c "напиши функцию fibonacci"
ai-cli -s -c "create app.py with flask server"
ai-cli --auto-save --extract-code "write sort.py"
```

**Результат:**
- ✓ Извлекает только блоки кода из ответа
- ✓ Убирает markdown форматирование
- ✓ Сохраняет чистый исполняемый код

## Примеры использования

### Python скрипты

```bash
# С пояснениями
ai-cli -o calculator.py "create calculator with add/subtract/multiply"

# Только код
ai-cli -o calculator.py -c "create calculator with add/subtract/multiply"
```

### Конфигурационные файлы

```bash
ai-cli -s "write docker-compose.yml for postgres and redis"
ai-cli -s "create .gitignore for python project"
ai-cli -s "write package.json for express app"
```

### Документация

```bash
ai-cli -s "Напиши README.md для CLI проекта"
ai-cli -o CONTRIBUTING.md "write contributing guidelines"
ai-cli -s "create API-DOCS.md with REST endpoints"
```

### Множественная генерация

```bash
# Создать несколько файлов последовательно
ai-cli -s "write Dockerfile for python app"
ai-cli -s "create docker-compose.yml"
ai-cli -s "write .dockerignore"
```

## Как это работает

### Автоопределение имени файла

CLI ищет паттерны в вашем запросе:

- `"Напиши HELLO-WORLD.md"` → `HELLO-WORLD.md`
- `"create config.py"` → `config.py`
- `"write app.js"` → `app.js`
- `"файл setup.sh"` → `setup.sh`

Поддерживаемые паттерны:
- Имена файлов с расширениями: `filename.ext`
- Слова: "create", "write", "файл"
- Кавычки: `"config.py"`, `'config.py'`

### Извлечение кода

Опция `--extract-code` ищет markdown блоки кода:

````markdown
Вот функция:

```python
def hello():
    print("Hello World")
```

Используйте её так...
````

Результат в файле:
```python
def hello():
    print("Hello World")
```

## Комбинации опций

### Быстрая генерация кода

```bash
# Автосохранение + только код
ai-cli -s -c "create server.py with flask REST API"
```

### С выбором модели

```bash
# Использовать другую модель
ai-cli --model deepseek-r1:8b -s "write complex algorithm.py"
```

### Полный контроль

```bash
# Явный файл + извлечение кода + модель
ai-cli -m llama3.2 -o app.py -c "write flask app with routes"
```

## Практические примеры

### 1. Создание проекта Python

```bash
ai-cli -s -c "create main.py with argparse CLI"
ai-cli -s -c "write setup.py for package named myapp"
ai-cli -s "create README.md for python CLI tool"
ai-cli -s "write requirements.txt with flask and requests"
ai-cli -s "create .gitignore for python"
```

### 2. Web проект

```bash
ai-cli -s -c "create index.html with bootstrap"
ai-cli -s -c "write style.css with modern design"
ai-cli -s -c "create app.js with fetch API examples"
ai-cli -s "write README.md for web app"
```

### 3. DevOps конфигурация

```bash
ai-cli -s "create Dockerfile for node.js app"
ai-cli -s "write docker-compose.yml with postgres and redis"
ai-cli -s "create .env.example with config variables"
ai-cli -s "write deploy.sh script"
```

### 4. Документация

```bash
ai-cli -s "create API.md with REST endpoints documentation"
ai-cli -s "write CONTRIBUTING.md with guidelines"
ai-cli -s "create CHANGELOG.md template"
```

## Проверка результатов

После генерации файла:

```bash
# Проверьте содержимое
cat HELLO-WORLD.md

# Для кода - запустите
python fibonacci.py

# Для скриптов - дайте права
chmod +x script.sh
./script.sh
```

## Советы

### 1. Будьте конкретны в запросе

❌ Плохо:
```bash
ai-cli -s "напиши код"
```

✅ Хорошо:
```bash
ai-cli -s -c "create fibonacci.py with recursive implementation"
```

### 2. Используйте -c для исполняемого кода

❌ Без -c (с пояснениями):
```python
# Вот функция fibonacci:

def fib(n):
    ...

# Используйте её так: fib(10)
```

✅ С -c (чистый код):
```python
def fib(n):
    ...
```

### 3. Проверяйте файлы перед использованием

```bash
# Сохраните
ai-cli -s -c "create deploy.sh"

# Проверьте
cat deploy.sh

# Дайте права и запустите
chmod +x deploy.sh
./deploy.sh
```

### 4. Комбинируйте с другими инструментами

```bash
# Генерируйте и сразу форматируйте
ai-cli -s -c "create app.py" && black app.py

# Генерируйте и проверяйте синтаксис
ai-cli -s -c "create script.py" && python -m py_compile script.py

# Генерируйте и добавляйте в git
ai-cli -s "create README.md" && git add README.md
```

## Частые вопросы

### Файл не создается?

Проверьте:
1. Используете ли опцию `-s` или `-o`
2. Есть ли имя файла с расширением в запросе
3. Есть ли права на запись в текущей папке

```bash
# Правильно:
ai-cli -s "create file.md"

# Неправильно (нет -s или -o):
ai-cli "create file.md"
```

### Файл содержит пояснения вместо кода?

Используйте `-c`:

```bash
# Добавьте флаг --extract-code
ai-cli -s -c "create script.py"
```

### Как указать путь к файлу?

```bash
# Абсолютный путь
ai-cli -o /Users/name/Documents/result.md "..."

# Относительный путь
ai-cli -o ../output/file.py "..."

# Текущая папка (по умолчанию)
ai-cli -s "create file.md"
```

### Можно ли перезаписать существующий файл?

Да, файл будет перезаписан без предупреждения. Будьте осторожны!

```bash
# Сохраните бэкап перед перезаписью
cp important.py important.py.backup
ai-cli -o important.py "improve the code"
```

## Интеграция в workflow

### Быстрое прототипирование

```bash
# Создайте структуру проекта
ai-cli -s "create project_structure.md"
cat project_structure.md

# Генерируйте файлы
ai-cli -s -c "create main.py"
ai-cli -s -c "create utils.py"
ai-cli -s "create README.md"
```

### Генерация тестов

```bash
# Создайте основной код
ai-cli -o calculator.py -c "write calculator class"

# Сгенерируйте тесты
ai-cli -o test_calculator.py -c "write pytest tests for calculator"

# Запустите
pytest test_calculator.py
```

### Документация на лету

```bash
# Генерируйте документацию для существующего кода
ai-cli -s "create ARCHITECTURE.md explaining project structure"
ai-cli -s "write SETUP.md with installation steps"
```

---

**Готово!** Теперь вы можете генерировать файлы напрямую из AI CLI.

**Основные команды:**
- `ai-cli -s "create file.ext"` - автосохранение
- `ai-cli -o file.ext "..."` - явный файл
- `ai-cli -s -c "..."` - только код
