import psycopg2
from contextlib import contextmanager
import faker
from random import randint
from config import DB_CONFIG, NUMBER_OF_USERS, NUMBER_OF_TASKS, STATUSES


@contextmanager
def create_connection():
    """Створення з'єднання з PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Помилка підключення: {e}")
    finally:
        if conn:
            conn.close()


def generate_fake_data(NUMBER_OF_USERS, NUMBER_OF_TASKS):
    """Генерація даних для заповнення таблиць."""
    fake = faker.Faker()
    fake_users = [
        {"fullname": fake.name(), "email": fake.email()} for _ in range(NUMBER_OF_USERS)
    ]
    fake_tasks = [
        {
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": randint(1, len(STATUSES)),
            "user_id": randint(1, NUMBER_OF_USERS),
        }
        for _ in range(NUMBER_OF_TASKS)
    ]

    return fake_users, fake_tasks


def prepare_data(users, statuses, tasks):
    """Підготовка даних до вставки в таблиці."""
    for_users = [(user["fullname"], user["email"]) for user in users]
    for_statuses = [(status,) for status in statuses]
    for_tasks = [
        (task["title"], task["description"], task["status_id"], task["user_id"])
        for task in tasks
    ]
    return for_users, for_statuses, for_tasks


def insert_data_into_db(users, statuses, tasks):
    """Вставка даних у таблиці."""
    with create_connection() as conn:
        try:
            cur = conn.cursor()

            # Вставка користувачів
            sql_users = """
            INSERT INTO users (fullname, email)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
            """
            cur.executemany(sql_users, users)
            print(f"Користувачі успішно додані.")

            # Вставка статусів
            sql_statuses = """
            INSERT INTO statuses (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """
            cur.executemany(sql_statuses, statuses)
            print(f"Статуси успішно додані.")

            # Вставка завдань
            sql_tasks = """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
            """
            cur.executemany(sql_tasks, tasks)
            print(f"Завдання успішно додані.")

        except Exception as e:
            print(f"Помилка вставки даних: {e}")


if __name__ == "__main__":
    print(f"Генеруються дані...")
    users, tasks = generate_fake_data(NUMBER_OF_USERS, NUMBER_OF_TASKS)
    users, statuses, tasks = prepare_data(users, STATUSES, tasks)

    print(f"Заповнюється база даних...")
    insert_data_into_db(users, statuses, tasks)
    print(f"База даних заповнена!")
    