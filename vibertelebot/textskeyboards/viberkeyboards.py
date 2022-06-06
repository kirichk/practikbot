from vibertelebot.utils.tools import keyboard_consctructor

LOGO = 'https://images.prom.ua/1630650539_w640_h640_practik-ukrainian.jpg'

menu_keyboard = keyboard_consctructor([
            ('Створити замовлення', 'order', ''),
            ("ЄПитання", 'question', ''),
            ("Потрібна консультація експерта з харчування", 'consult', ''),
            ("Перейти на сайт", 'website', ''),
            ("Назад", 'back', ''),
            ])


greeting_keyboard = keyboard_consctructor([
            ('Так', 'yes', ''),
            ('Ні', 'no', ''),
            ])


pet_keyboard = keyboard_consctructor([
            ('Собака 🐕', 'pet_dog', ''),
            ('Котик 🐈', 'pet_cat', ''),
            ('Собака та котик 🐾', 'pet_cat_dog', ''),
            ])
