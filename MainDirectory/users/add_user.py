from db import create_user, get_user_by_username


def main():
    # Додаємо тестового користувача
    print("Додаємо тестового користувача...")
    try:
        create_user("admin", "password123", "admin")
        print("Користувач 'admin' створений успішно!")

        # Перевіряємо, чи користувач додався
        user = get_user_by_username("admin")
        if user:
            print(f"Користувач знайдений: {user.username}, роль: {user.role}")
        else:
            print("Користувача не знайдено")

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()