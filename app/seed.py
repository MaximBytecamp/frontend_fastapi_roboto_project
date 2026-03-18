from sqlmodel import Session, select
from app.core.database import engine
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.product import Product


def seed_data():
    with Session(engine) as session:
        existing_users = session.exec(select(User)).first()
        if existing_users:
            print("База данных уже содержит данные. Пропуск заполнения.")
            return

        # ====== Пользователи ======
        admin = User(
            name="Администратор",
            email="admin@robomarket.ru",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        user = User(
            name="Иван Петров",
            email="user@robomarket.ru",
            hashed_password=hash_password("user123"),
            role="user"
        )
        session.add(admin)
        session.add(user)
        session.commit()

        # ====== Категории ======
        categories_data = [
            {"name": "Робототехнические наборы", "description": "Полные наборы для сборки и программирования роботов"},
            {"name": "Контроллеры", "description": "Arduino, ESP32, Raspberry Pi и другие платы управления"},
            {"name": "Датчики", "description": "Ультразвуковые, инфракрасные, температурные и другие датчики"},
            {"name": "Сервоприводы и моторы", "description": "Сервоприводы, шаговые и DC-моторы для робототехники"},
            {"name": "Питание", "description": "Аккумуляторы, блоки питания и модули зарядки"},
            {"name": "Колёса и шасси", "description": "Колёса, гусеницы, рамы и шасси для мобильных роботов"},
            {"name": "Камеры и модули", "description": "Камеры, дисплеи и коммуникационные модули"},
            {"name": "Аксессуары", "description": "Провода, макетные платы, крепёж и другие аксессуары"},
        ]
        categories = []
        for cat_data in categories_data:
            cat = Category(**cat_data)
            session.add(cat)
            categories.append(cat)
        session.commit()
        for cat in categories:
            session.refresh(cat)

        # ====== Товары ======
        products_data = [
            # Робототехнические наборы
            {
                "name": "Arduino Starter Kit",
                "short_description": "Полный набор для начинающих с Arduino Uno",
                "full_description": "Набор включает плату Arduino Uno R3, макетную плату, набор резисторов, светодиодов, кнопок, потенциометров, сервопривод, LCD-дисплей, датчики температуры и освещённости. Идеально подходит для первого знакомства с робототехникой и программированием микроконтроллеров. В комплекте книга с 15 проектами.",
                "price": 4500.00,
                "image_url": "https://images.unsplash.com/photo-1553406830-ef2513450d76?w=400",
                "stock": 25,
                "category_id": 1
            },
            {
                "name": "Робот-манипулятор 4DOF",
                "short_description": "Роботизированная рука с 4 степенями свободы",
                "full_description": "Роботизированная рука с 4 степенями свободы на базе сервоприводов MG996R. Корпус из акрила, управление через Arduino. Поддерживает захват объектов весом до 200 граммов. Включает инструкцию по сборке и примеры программ.",
                "price": 7800.00,
                "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400",
                "stock": 10,
                "category_id": 1
            },
            {
                "name": "Набор STEM Робот-танк",
                "short_description": "Гусеничный робот с камерой и WiFi-управлением",
                "full_description": "Гусеничный робот-танк с камерой для FPV, управление через WiFi с помощью смартфона или компьютера. На базе ESP32, встроенный датчик ультразвукового дальномера, инфракрасные датчики для следования по линии. Поддерживает автономный режим.",
                "price": 12500.00,
                "image_url": "https://images.unsplash.com/photo-1561557944-6e7860d1a7eb?w=400",
                "stock": 8,
                "category_id": 1
            },
            # Контроллеры
            {
                "name": "Arduino Uno R3",
                "short_description": "Классический микроконтроллер для обучения",
                "full_description": "Arduino Uno R3 — самая популярная плата для обучения программированию и электронике. Микроконтроллер ATmega328P, 14 цифровых пинов, 6 аналоговых входов, USB-подключение, питание 7-12В. Совместима с тысячами библиотек и проектов.",
                "price": 1200.00,
                "image_url": "https://images.unsplash.com/photo-1608564697071-ddf911d81370?w=400",
                "stock": 50,
                "category_id": 2
            },
            {
                "name": "ESP32 DevKit V1",
                "short_description": "Модуль WiFi + Bluetooth для IoT-проектов",
                "full_description": "ESP32 DevKit V1 — мощный микроконтроллер с встроенным WiFi и Bluetooth. Двухъядерный процессор 240 МГц, 520 КБ SRAM, 34 GPIO-пина. Идеален для проектов Интернета вещей, умного дома и робототехники с беспроводным управлением.",
                "price": 850.00,
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400",
                "stock": 40,
                "category_id": 2
            },
            {
                "name": "Raspberry Pi 4 Model B 4GB",
                "short_description": "Мини-компьютер для сложных робототехнических проектов",
                "full_description": "Raspberry Pi 4 Model B с 4 ГБ оперативной памяти. Четырёхъядерный процессор ARM Cortex-A72 1.5 ГГц, поддержка двух мониторов 4K, USB 3.0, Gigabit Ethernet, WiFi 5 ГГц, Bluetooth 5.0. Идеален для проектов с компьютерным зрением и машинным обучением.",
                "price": 6500.00,
                "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=400",
                "stock": 15,
                "category_id": 2
            },
            # Датчики
            {
                "name": "Ультразвуковой датчик HC-SR04",
                "short_description": "Датчик расстояния от 2 до 400 см",
                "full_description": "Ультразвуковой датчик расстояния HC-SR04. Диапазон измерения: 2-400 см, точность: ±3 мм, рабочая частота: 40 кГц. Простое подключение: VCC, Trig, Echo, GND. Широко используется в робототехнике для обнаружения препятствий.",
                "price": 180.00,
                "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400",
                "stock": 100,
                "category_id": 3
            },
            {
                "name": "Набор датчиков 37-в-1",
                "short_description": "Комплект из 37 различных датчиков для Arduino",
                "full_description": "Универсальный набор из 37 датчиков: температуры, влажности, давления, света, звука, движения, газа, магнитного поля, пульса и многих других. Совместим с Arduino и ESP32. Включает документацию и примеры кода для каждого датчика.",
                "price": 3200.00,
                "image_url": "https://images.unsplash.com/photo-1580584126903-c17d41830450?w=400",
                "stock": 20,
                "category_id": 3
            },
            {
                "name": "ИК-датчик препятствий",
                "short_description": "Инфракрасный датчик для обнаружения препятствий",
                "full_description": "Инфракрасный датчик для обнаружения препятствий на расстоянии 2-30 см. Регулируемый потенциометр чувствительности, цифровой выход. Идеален для роботов-следопытов и проектов автоматического объезда препятствий.",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400",
                "stock": 80,
                "category_id": 3
            },
            # Сервоприводы и моторы
            {
                "name": "Сервопривод MG996R",
                "short_description": "Мощный сервопривод с металлическими шестернями",
                "full_description": "Сервопривод MG996R с металлическими шестернями. Крутящий момент: 11 кг·см при 6В, скорость: 0.17 сек/60°. Угол поворота: 180°. Идеален для роботизированных рук, поворотных платформ и тяжёлых нагрузок.",
                "price": 450.00,
                "image_url": "https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=400",
                "stock": 60,
                "category_id": 4
            },
            {
                "name": "Шаговый двигатель NEMA 17",
                "short_description": "Точный шаговый мотор для ЧПУ и 3D-принтеров",
                "full_description": "Биполярный шаговый двигатель NEMA 17 с углом шага 1.8° (200 шагов на оборот). Ток: 1.5А, удерживающий момент: 4.2 кг·см. Применяется в 3D-принтерах, станках с ЧПУ и точных робототехнических системах.",
                "price": 780.00,
                "image_url": "https://images.unsplash.com/photo-1537151608828-ea2b11305ee2?w=400",
                "stock": 30,
                "category_id": 4
            },
            # Питание
            {
                "name": "Аккумулятор Li-Po 7.4V 2200mAh",
                "short_description": "Литий-полимерный аккумулятор для роботов",
                "full_description": "Литий-полимерный аккумулятор 7.4В 2200мАч (2S). Разрядный ток: до 25C. Разъём XT60. Идеален для мобильных роботов, дронов и проектов, требующих автономного питания. В комплекте балансировочный кабель.",
                "price": 1500.00,
                "image_url": "https://images.unsplash.com/photo-1619953942547-233eab5a70d6?w=400",
                "stock": 35,
                "category_id": 5
            },
            # Колёса и шасси
            {
                "name": "Шасси для робота 4WD",
                "short_description": "Платформа с 4 моторами для мобильного робота",
                "full_description": "Универсальная платформа для мобильного робота с 4 DC-моторами и колёсами. Размер: 25×15 см, материал: акрил. Включает 4 мотора с редуктором, 4 колеса, крепёж, отсек для батареек. Идеальная основа для первого робота.",
                "price": 2200.00,
                "image_url": "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=400",
                "stock": 18,
                "category_id": 6
            },
            # Камеры и модули
            {
                "name": "Камера OV7670 для Arduino",
                "short_description": "Компактная камера 640×480 для обработки изображений",
                "full_description": "Камера-модуль OV7670 с разрешением 640×480 пикселей. Поддержка форматов YUV, RGB. Низкое энергопотребление, встроенная обработка изображений. Используется для проектов компьютерного зрения с Arduino и ESP32.",
                "price": 350.00,
                "image_url": "https://images.unsplash.com/photo-1526406915894-7bcd65f60845?w=400",
                "stock": 25,
                "category_id": 7
            },
            # Аксессуары
            {
                "name": "Макетная плата 830 точек",
                "short_description": "Беспаечная макетная плата для прототипирования",
                "full_description": "Беспаечная макетная плата (breadboard) на 830 контактных точек. Центральная область 630 точек + 2 шины питания по 100 точек. Совместима со стандартными компонентами DIP. Незаменимый инструмент для прототипирования электронных схем.",
                "price": 250.00,
                "image_url": "https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=400",
                "stock": 100,
                "category_id": 8
            },
            {
                "name": "Набор проводов Dupont 120 шт",
                "short_description": "Набор соединительных проводов M-M, M-F, F-F",
                "full_description": "Набор из 120 соединительных проводов Dupont длиной 20 см: 40 шт. папа-папа (M-M), 40 шт. папа-мама (M-F), 40 шт. мама-мама (F-F). Универсальные провода для подключения Arduino, датчиков и модулей к макетной плате.",
                "price": 280.00,
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400",
                "stock": 150,
                "category_id": 8
            },
        ]

        for prod_data in products_data:
            product = Product(**prod_data)
            session.add(product)

        session.commit()
        print("Тестовые данные успешно добавлены!")
        print(f"  - Пользователей: 2 (admin@robomarket.ru / admin123, user@robomarket.ru / user123)")
        print(f"  - Категорий: {len(categories_data)}")
        print(f"  - Товаров: {len(products_data)}")
