# Инструкция по развертыванию проекта

1. Создайте папку в которую вы хотите скачать проект. В терминале:
   ```bash
   mkdir ProjectHH
   ```

2. Перейдите в нее:
   ```bash
   cd ProjectHH
   ```

3. Склонируйте репозиторий на свой локальный компьютер:
   ```bash

   git clone https://github.com/agapoov/HandyHub.git
   ```
   
4. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

5. Активируйте виртуальное окружение:
   ```bash
   venv\Scripts\activate
   ```
   
6. Перейдите в проект:
   ```bash
   cd app
   ```

7. Установите необходимые зависимости, используя `pip`:
   ```bash
   pip install -r requirements.txt
   ```
8. Выполните миграции:
     ```bash
     python manage.py migrate
     ```

9. Запустите проект:
     ```bash
     python manage.py runserver
     ```

Проект будет доступен по адресу localhost:8000 или 127.0.0.1:8000
