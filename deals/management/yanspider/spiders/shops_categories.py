shops = {
    'связной': {'id': 3828, 'categories':
        ['смартфоны', 'умные часы и браслеты', 'телевизоры']},
    '123.ru': {'id': 5570, 'categories':
        ['телевизоры', 'смартфоны', 'умные часы и браслеты',
         'конструкторы', 'настольные игры',
         'блендеры', 'кофеварки и кофемашины', 'мультиварки']},
    'TechPort.ru': {'id': 1672, 'categories':
        ['телевизоры', 'смартфоны', 'умные часы и браслеты',
         'конструкторы', 'настольные игры',
         'блендеры', 'кофеварки и кофемашины', 'мультиварки']}
}

vendor = '&fesh={}'
promo = 'onstock=1&local-offers-first=0&promo-type=discount&viewtype=grid'

categories_urls = {
    # Электроника
    'смартфоны': f'https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?{promo}{vendor}',
    'умные часы и браслеты': f'https://market.yandex.ru/catalog--umnye-chasy-i-braslety/56034/list?{promo}{vendor}',
    'телевизоры': f'https://market.yandex.ru/catalog--televizory/59601/list?{promo}{vendor}',
    # Бытовая техника
    'блендеры': f'https://market.yandex.ru/catalog--blendery/16673559/list?{promo}{vendor}',
    'кофеварки и кофемашины': f'https://market.yandex.ru/catalog--kofevarki-i-kofemashiny/54942/list?{promo}{vendor}',
    'мультиварки': f'https://market.yandex.ru/catalog--multivarki/54951/list?{promo}{vendor}',
    # Для детей
    'настольные игры': f'https://market.yandex.ru/catalog--nastolnye-igry/17348362/list?{promo}{vendor}',
    'конструкторы': f'https://market.yandex.ru/catalog--konstruktory-dlia-detei-do-3-let/17310967/list?{promo}{vendor}',
}
