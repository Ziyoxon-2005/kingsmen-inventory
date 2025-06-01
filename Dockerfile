# Python 3.11 rasmiy image dan foydalanamiz
FROM python:3.11-slim

# Ishchi katalogni yaratamiz
WORKDIR /app

# Dependensiyalarni konteynerga nusxalash
COPY requirements.txt /app/

# Dependensiyalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . /app/

# Django serverini 0.0.0.0:8000 da ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]