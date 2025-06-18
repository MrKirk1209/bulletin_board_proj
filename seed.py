from database import SessionLocal, Base, engine
from models import Role, User, Category, Advertisement, Response, Favourite
from datetime import datetime, timedelta
import bcrypt 
import random

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:


        roles = [
            Role(name="admin"),
            Role(name="user"),
            Role(name="moderator")
        ]
        db.add_all(roles)
        db.commit()
        

        users = [
            User(username="Admin", email="admin@example.com", password=hash_password("admin12345"), role_id=1),
            User(username="Moderator1", email="mod1@example.com", password=hash_password("modPass1"), role_id=3),
            User(username="Moderator2", email="mod2@example.com", password=hash_password("modPass2"), role_id=3),
            User(username="User1", email="user1@example.com", password=hash_password("password1"), role_id=2),
            User(username="User2", email="user2@example.com", password=hash_password("password2"), role_id=2),
            User(username="User3", email="user3@example.com", password=hash_password("password3"), role_id=2)
        ]
        db.add_all(users)
        db.commit()
        

        categories = [
            Category(name="cars"),
            Category(name="electronics"),
            Category(name="clothes"),
            Category(name="books"),
            Category(name="furniture"),
            Category(name="sport")
        ]
        db.add_all(categories)
        db.commit()

        category_data = {
            "cars": {
                "brands": ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi"],
                "models": ["Camry", "Civic", "Focus", "X5", "C-Class", "A4"],
                "templates": [
                    ("{brand} {model} {year} года", "Пробег: {mileage} км, {condition}. {details}"),
                    ("Продам {brand} {model}", "Год выпуска: {year}, двигатель {engine} л.с. {details}"),
                    ("{brand} {model} в {condition} состоянии", "Комплектация: {trim}, {features}")
                ],
                "engines": ["1.6", "2.0", "2.5", "3.0", "электрический"],
                "trims": ["стандарт", "комфорт", "люкс", "премиум"]
            },
            "electronics": {
                "brands": ["Samsung", "Apple", "Sony", "LG", "Xiaomi", "Asus"],
                "models": ["Galaxy S24", "iPhone 15", "Bravia", "OLED", "Redmi", "Zenbook"],
                "templates": [
                    ("{brand} {model}", "Характеристики: {specs}, {condition}. {details}"),
                    ("Новый {product} {brand}", "Гарантия: {warranty}, {details}"),
                    ("{product} {brand} {model}", "Состояние: {condition}, {features}")
                ],
                "products": ["смартфон", "ноутбук", "телевизор", "планшет", "фотоаппарат"]
            },
            "clothes": {
                "brands": ["Nike", "Zara", "Adidas", "H&M", "Gucci", "Levi's"],
                "models": ["Air Max", "Basic", "Ultraboost", "Trend", "Classic", "501"],
                "templates": [
                    ("{type} {brand} размер {size}", "Состояние: {condition}, материал: {material}"),
                    ("{brand} {item}", "Новый с биркой, размер {size}, цвет {color}"),
                    ("{style} {item} {brand}", "Цвет: {color}, размер {size}, {material}")
                ],
                "types": ["Куртка", "Платье", "Рубашка", "Джинсы", "Футболка", "Костюм"]
            },
            "books": {
                "brands": ["Эксмо", "АСТ", "Манн, Иванов и Фербер", "Питер", "Росмэн"],
                "models": ["", "", "", "", ""],  # Не используется для книг
                "templates": [
                    ("{title} - {author}", "Жанр: {genre}, {condition}. {details}"),
                    ("Книга '{title}'", "Год издания: {year}, {details}"),
                    ("{author}: {title}", "Состояние: {condition}, {pages} стр. {genre}")
                ],
                "titles": ["Властелин Колец", "Гарри Поттер", "1984", "Мастер и Маргарита", "Преступление и наказание"]
            },
            "furniture": {
                "brands": ["IKEA", "Hoff", "Шатура", "Ангстрем", "Stolplit"],
                "models": ["EKTORP", "Domenico", "Милан", "Флоренция", "Классик"],
                "templates": [
                    ("{type} {brand} {material}", "Стиль: {style}, {condition}. Размеры: {dimensions}"),
                    ("{room} {item} {brand}", "Цвет: {color}, материал: {material}"),
                    ("{item} для {room} {brand}", "Материал: {material}, сборка: {assembly}")
                ],
                "items": ["диван", "кресло", "стол", "шкаф", "кровать"]
            },
            "sport": {
                "brands": ["Adidas", "Nike", "Puma", "Reebok", "Under Armour"],
                "models": ["Predator", "Air Max", "Ultra", "Classic", "Charged"],
                "templates": [
                    ("{brand} {equipment}", "Для {sport}, {condition}. {details}"),
                    ("{equipment} {brand} {model}", "Размер: {size}, цвет: {color}"),
                    ("{sport} {item} {brand}", "{features}, {material}")
                ],
                "equipment": ["велосипед", "кроссовки", "мяч", "гиря", "ракетка"]
            }
        }


        conditions = ["отличное", "хорошее", "новое", "как новое", "требует ремонта"]
        details_list = ["с документами", "с гарантией", "с аксессуарами", "оригинальная упаковка"]
        colors = ["черный", "белый", "синий", "красный", "зеленый", "серый"]
        

        ads = []
        start_date = datetime(2025, 5, 1)
        regular_users = [4, 5, 6]  
        

        db_categories = db.query(Category).all()
        
        for category in db_categories:
            cat_name = category.name
            cat_id = category.id
            data = category_data[cat_name]
            
            for i in range(20):

                title_template, desc_template = random.choice(data["templates"])

                template_data = {
                    "brand": random.choice(data["brands"]),
                    "model": random.choice(data["models"]),
                    "year": random.randint(2015, 2025),
                    "mileage": random.randint(5000, 100000) if cat_name == "cars" else "",
                    "condition": random.choice(conditions),
                    "details": random.choice(details_list),
                    "product": random.choice(data.get("products", [""])),
                    "warranty": random.choice(["6 месяцев", "1 год", "2 года"]),
                    "specs": f"{random.randint(2, 12)}ГБ RAM, {random.randint(128, 1000)}ГБ SSD" if cat_name == "electronics" else "",
                    "type": random.choice(data.get("types", [""])),
                    "size": random.choice(["S", "M", "L", "XL"]),
                    "material": random.choice(["кожа", "хлопок", "полиэстер", "дерево", "металл"]),
                    "item": random.choice(data.get("items", [""])),
                    "style": random.choice(["Классический", "Современный", "Минимализм"]),
                    "color": random.choice(colors),
                    "title": random.choice(data.get("titles", [""])),
                    "author": random.choice(["Толкин", "Роулинг", "Оруэлл", "Достоевский", "Булгаков"]),
                    "genre": random.choice(["Фэнтези", "Научная литература", "Детектив", "Роман", "Исторический"]),
                    "pages": random.randint(100, 800),
                    "room": random.choice(["гостиная", "кухня", "спальня", "офис", "детская"]),
                    "dimensions": f"{random.randint(50, 200)}x{random.randint(50, 200)} см",
                    "assembly": random.choice(["требуется сборка", "готовая"]),
                    "equipment": random.choice(data.get("equipment", [""])),
                    "sport": random.choice(["футбол", "бег", "йога", "теннис", "велоспорт"]),
                    "features": f"{random.randint(1, 30)} функций",
                    "trim": random.choice(data.get("trims", [""])),
                    "engine": random.choice(data.get("engines", [""])),
                }
                
                title = title_template.format(**template_data).strip()
                description = desc_template.format(**template_data).strip()
                

                if cat_name == "cars":
                    price = round(random.uniform(5000, 50000), 2)
                elif cat_name in ["electronics", "furniture"]:
                    price = round(random.uniform(200, 5000), 2)
                else:
                    price = round(random.uniform(10, 1000), 2)
                
                ads.append(
                    Advertisement(
                        title=title,
                        description=description,
                        price=price,
                        creator_id=random.choice(regular_users),
                        category_id=cat_id,
                        date=start_date + timedelta(days=random.randint(0, 45))
                ))
        
        db.add_all(ads)
        db.commit()
        

        responses = []
        ad_ids = [ad.id for ad in ads] 
        
        for _ in range(30):
            responses.append(
                Response(
                    message=random.choice([
                        "Интересует этот товар, возможен торг?",
                        "Есть ли дополнительные фото?",
                        "Могу забрать сегодня, какой адрес?",
                        "Какие есть способы оплаты?",
                        f"Предлагаю свою цену: ${random.randint(50, 500)}",
                        "Есть ли гарантия на товар?",
                        "Интересует обмен?",
                        "Состояние соответствует описанию?",
                        "Когда можно посмотреть товар?"
                    ]),
                    user_id=random.choice(regular_users),
                    advertisement_id=random.choice(ad_ids)
                )
            )
        
        db.add_all(responses)
        db.commit()
        

        favorites = []
        favorite_pairs = set()
        
        while len(favorites) < 40:
            user_id = random.choice(regular_users)
            ad_id = random.choice(ad_ids)
            
            if (user_id, ad_id) not in favorite_pairs:
                favorite_pairs.add((user_id, ad_id))
                favorites.append(
                    Favourite(user_id=user_id, advertisement_id=ad_id)
                )
        
        db.add_all(favorites)
        db.commit()
        
        print("Данные успешно заполнены!")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()