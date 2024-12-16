from pymongo import MongoClient
from data import cats

# Підключення до MongoDB
client = MongoClient(
    f"mongodb+srv://lazardmytro:ekdaHAA7gzIKWZbZ@cluster0.ouw4u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["cats_db"]
cats_collection = db["cats"]

def populate_initial_CATalogue():
    """Функція для додавання початкового набору котів до бази даних."""
    try:
        cats_collection.insert_many(cats)
        print("Коти успішно додані.")
    except Exception as e:
        print(f"Помилка при додаванні котів: {e}")


# Операції CRUD
def get_all_cats():
    """Функція для виведення всіх котів з колекції."""
    try:
        cats = cats_collection.find()
        if cats_collection.count_documents({}) == 0:
            print("Колекція пуста.")
        else:
            for cat in cats:
                print(str(cat))
    except Exception as e:
        print(f"Помилка при отриманні котів: {e}")


def get_cat_by_name(name):
    """Функція для виведення кота за іменем."""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(str(cat))
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка при отриманні кота: {e}")


def update_cat_age(name, new_age):
    """Функція для оновлення віку кота."""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота {name} змінено на {new_age}.")
        else:
            print(f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")


def add_feature_to_cat(name, new_feature):
    """Функція для додавання нової характеристики для кота."""
    try:
        result = cats_collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}},  # Додає елемент, якщо його немає
        )
        if result.modified_count > 0:
            print(f"Характеристика '{new_feature}' додана для кота {name}.")
        else:
            print(f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")


def delete_cat_by_name(name):
    """Функція для видалення кота за іменем."""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям {name} видалено.")
        else:
            print(f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")


def delete_all_cats():
    """Функція для видалення всіх котів з колекції."""
    try:
        result = cats_collection.delete_many({})
        print(f"{result.deleted_count} котів було видалено.")
    except Exception as e:
        print(f"Помилка при видаленні котів: {e}")


if __name__ == "__main__":
    # Додати початковий набір котів до бази даних перед тестуванням інших операцій
    populate_initial_CATalogue()

    # Тестування операцій
    print("Отримання всіх котів:")
    get_all_cats()

    print("\nОтримання кота за іменем 'Barsik':")
    get_cat_by_name("Barsik")

    print("\nОновлення віку кота 'Barsik' до 4 років:")
    update_cat_age("Barsik", 4)

    print("\nДодавання характеристики до кота 'Barsik':")
    add_feature_to_cat("Barsik", "любить застрибувати на ялинку")

    print("\nОтримання оновлених даних кота 'Barsik':")
    get_cat_by_name("Barsik")

    print("\nВидалення кота 'Barsik':")
    delete_cat_by_name("Barsik")

    print("\nВидалення всіх котів:")
    delete_all_cats()
    