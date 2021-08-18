
language = """<b>O'zingizga qulay tilni tanlang!
-----
Выберите удобный Вам язык!.</b>"""

ADDRES_TO_YOU = {
    'uz':"<b>Manzilingizni kiriting 📌</b>",
    'ru':"<b>Введите свой адрес 📌</b>"
}

NAME_MESSAGE = {
   "uz": "<b>Ismingizni kiriting</b>",
   "ru": "<b>Введите ваше имя</b>"
}

ECHO_ALL = {
    "uz": """
Agar sizda biron bir savol bo‘lsa, murojaatingizni shu erda yozishingiz mumkin: LICHKA
Yoki bizga bog'laning:  TEL_RAQAM
Yoki /start tugmasini bosing
    """,
    "ru":"""
При возникновении каких-либо вопросов, вы можете написать своё обращение сюда: LICHKA
Или позвоните по номеру:  TEL_RAQAM
Или нажмите /start
    """
}

SEND_CONTACTS = {
    'uz': "<b>Telefon raqamni jo'nating</b>",
    'ru': "<b>Отправить номер телефона</b>"
}
SEND_CONTACT = {
    'uz': "📱 Telefon raqamni jo'natish",
    'ru': "📱 Отправить номер телефона"
}

START_MESSAGE = {
    'uz': '<b>Kerakli tugmani bosing 🗂</b>',
    'ru': '<b>Нажмите желаемую кнопку 🗂</b>'
}

KATEGORIYA_MESSAGE = {
    'uz': "<b>🗂 Kategoriyani tanlang:</b>",
    'ru': "<b>🗂 Выбрать категорию:</b>"
}

BACK = {
    'uz': "🔙 Orqaga",
    'ru': "🔙 Назад"
}

PRODUCT_INFO = {
    "uz": """
<code>* * * * * * *</code>
    <b>📝 Nomi:</b><a href="https://telegra.ph/{path}"> <i>{title}</i></a>
    <b>🧮 Miqdori: <i>{count} ta</i></b>
<code>* * * * * * *</code>

<b>Bo`lib to`lash narxi:</b>
<i>Tarif:</i> {protsent} oy
<i>Birinchi to`lov:</i> {one_pay} so`m
<i>Umumiy:</i> {all_price}

    """,
    "ru": """
<code>* * * * * * *</code>
    <b> 📝 Имя:</b> <a href="https://telegra.ph/{path}"><i>{title}</i>
    <b>🧮 Количество: <i>{count} ta</i></b>
<code>* * * * * * *</code>

<b>Цена для рассрочки:</b>
<i>Кредитный план::</i> {protsent} месяцев
<i>Первоначальный взнос:</i> {one_pay} сум
    """,
}

PRODUCTS_INFO = {
    "uz": "<b>📌 Maxsulotlar ro'yhati</b>",
    "ru": "<b>📌 Список продуктов</b>"
    }

ADD_TO_SHOP_CARD = {
    'uz': "🧺 Savatga joylash",
    'ru': "🧺 покупка товаров"
}

ADDED_TO_SHOP_CARD = {
    'uz': "Savatga joylandi ✅",
    'ru': "Добавлено в корзину ✅"
}

ADDED_TO_SHOP_CARDS = {
    'uz': "<b>Sotib olish uchun yuborildi ✅</b>",
    'ru': "<b>Отправлено на покупку ✅</b>"
}

EMPTY_SHOP_CARD = {
    'uz': "<b>Savatcha bo'sh 🗑</b>",
    'ru': "<b>Корзина пуста 🗑</b>"
}

EMPTY_SHOP_CARDS = {
    'uz': "Savatcha bo'sh 🗑",
    'ru': "Корзина пуста 🗑"
}

MESSAGE_SHOP_CARD = {
    'uz': "💰 Sotib olish",
    'ru': "💰 Покупка"
}

MESSAGE_SHOP_CARDS = {
    'uz': "💰 Sotib olish hammasini",
    'ru': "💰 Купи их все"
}

NOT_PRODUCT_MESSAGE = {
    'uz': "Maxsulot mavjud emas ❌",
    'ru': "Товар нет ❌"
}

CUSTOMER_PROFILE = {
    'uz': "<b>👤 Mening sahifam:</b>",
    'ru': "<b>👤 Моя страница:</b>"
}

CUSTOMER_PROFILE_ORDER = {
    'uz': "✴️ Mening buyurtmalarim",
    'ru': "✴️ Мои заказы"
}
CUSTOMER_PROFILE_LANGUAGE = {
    'uz': "🌍 Tilni o'zgartirish",
    'ru': "🌍 Сменить язык"
}

LANGUAGE_EDIT = {
    'uz': "Saqlandi ✅",
    'ru': "Сохранено ✅"
}
PRODUCT_INFO_UP = {
    'uz': """<b>🛍 Maxsulotlar</b>
<code>* * * * *</code>""",
    'ru': """<b>🛍 Продукты</b>
<code>* * * * *</code>"""
}
PRODUCT_INFO_TEXT = {
    'uz': """
<b>Xarid:</b> <code>{status}</code>
<b>Nomi:</b> <i>{title}</i>
<b>Narxi</b>: <i>{count} x {price} = {all_price}</i>
<code>* * * * *</code>
        """,
    'ru': """
<b>Имени:</b> <i>{title}</i>
<b>Цена:</b> <i>{count} x {price} = {all_price}</i>
<code>* * * * *</code>"""
}
ORDER_TEXT = {
    'uz': """<b>{a}.</b> <i>{title}
        <code>{count}x{price}={all_price}</code></i>\n""",
}

PRODUCT_INFO_ONE = {
    'uz': """
<b>Nomi:</b><a href="http://telegra.ph/{path}"> {title}</a>
<b>Narxi</b>: <i>{count} x {price} = {all_price}</i>

        """,
    'ru': """
<b>Имени:</b><a href="http://telegra.ph/{path}"> {title}</a>
<b>Цена:</b> <i>{count} x {price} = {all_price}</i>
"""
}

CLOSE = {
    'uz':"❌ Bekor qilish",
    'ru':"❌ Отменить действие"
}