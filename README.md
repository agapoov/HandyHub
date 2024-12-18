# Инструкция по развертыванию проекта


1. Склонируйте репозиторий на свой локальный компьютер:
   ```bash
   git clone https://github.com/agapoov/HandyHub.git
   ```
   
2. Перейдите в нее:
```bash
cd HandyHub
```

3. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

4. Активируйте виртуальное окружение:
   ```bash
   venv\Scripts\activate
   ```
   
5. Перейдите в проект:
   ```bash
   cd app
   ```

6. Установите необходимые зависимости, используя `pip`:
   ```bash
   pip install -r requirements.txt
   ```
7. Выполните миграции:
     ```bash
     python manage.py migrate
     ```

8. Запустите проект:
     ```bash
     python manage.py runserver
     ```

Проект будет доступен по адресу localhost:8000 или 127.0.0.1:8000
