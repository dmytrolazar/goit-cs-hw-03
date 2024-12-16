from bson import ObjectId

cats = [
    {
        "_id": ObjectId(),
        "name": "Barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    },
    {
        "_id": ObjectId(),
        "name": "Lama",
        "age": 2,
        "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
    },
    {
        "_id": ObjectId(),
        "name": "Liza",
        "age": 4,
        "features": ["ходить в лоток", "дає себе гладити", "білий"],
    },
]
