# 🌍 Travel Diary (Дневник путешествий)

Учебный проект на Flask: веб-приложение для ведения личного дневника путешествий.

## 🚀 Возможности
- Регистрация и авторизация пользователей
- Добавление собственных путешествий
- Просмотр записей других пользователей
- Дополнительные атрибуты путешествия:
  - 📍 Местоположение
  - 🖼 Изображение мест
  - 💲 Стоимость поездки

## 🔧 Установка и запуск
```bash
# Клонировать репозиторий
git clone https://github.com/saida2347g/travel-diary-flask.git
cd travel-diary-flask

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate   # Windows
# или source venv/bin/activate   # Linux/Mac

# Установить зависимости
pip install flask flask_sqlalchemy werkzeug

# Запустить приложение
python app.py
