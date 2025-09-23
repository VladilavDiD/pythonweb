#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Тест запуску...")

try:
    from db import init_db

    print("Імпорт db успішний")

    init_db()
    print("БД створена успішно!")

except ImportError as e:
    print(f"Помилка імпорту: {e}")
except Exception as e:
    print(f"Інша помилка: {e}")

print("Завершено.")