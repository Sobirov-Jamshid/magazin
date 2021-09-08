
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

<b>👉 Bo`lib to`lash narxi:</b>
<i>📆 Tarif:</i> {protsent} oy
<i>💳 Birinchi to`lov:</i> {one_pay} {price_choice}
<i>💰 Umumiy:</i> {all_price} {price_choice}

    """,
    "ru": """
<code>* * * * * * *</code>
<b> 📝 Имя:</b> <a href="https://telegra.ph/{path}"><i>{title}</i></a>
<b>🧮 Количество: <i>{count} ta</i></b>
<code>* * * * * * *</code>

<b>👉 Цена для рассрочки:</b>
<i>📆 Кредитный план::</i> {protsent} месяцев
<i>💳 Первоначальный взнос:</i> {one_pay} {price_choice}
<i>💰 Итого:</i> {all_price} {price_choice}
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
    'uz': "<b>Sizning №{id} raqamli buyurtmangiz qabul qilindi. Tasdiqlashlarini kuting ✅</b>",
    'ru': "<b>Ваш заказ №{id} принят. Ждите подтверждения ✅</b>"
}

NEW_ORDER = {
    'uz': """
<b>🎊 Yangi №{id} raqamli buyurtma</b>
👤 User: <a href="tg://user?id={chat_id}">{name}</a>
📞 Telefon raqami: {phone}
📍 Manzil: {adress}
""",
    'ru': """
<b>🎊 Новый цифровой заказ № {id}</b>
<b>👤 Пользователь:</b> <a href="tg://user?id={chat_id}">{name}</a>
<b>📞 Номер телефона:</b> {phone}
<b>📍 Адрес:</b> {adress}
"""
}

NEW_ORDER_SEND_GROUPS = {
    'uz': """
<b>To`lov turi Tezkor xarid 💳</b>
♻️Status: <code>{status}</code>
<i>🔖 Nomi:</i> {title}
<i>🔢 Soni:</i> {count}
<i>💰 Puli:</i> {payments} {currency}  
    
    """,
    'ru': """
<b> Тип оплаты Быстрая покупка 💳 </b>
♻️Status: <code>{status}</code>
<i> 🔖 Имя: </i> {title}
<i> 🔢 Сони: </i> {count}
<i> 💰 Деньги: </i> {payments} {currency}

    """

}

NEW_ORDER_SEND_GROUP = {
    'uz':"""

<b>To`lov turi Bo`lib to`lash 💳</b>
♻️Status: <code>{status}</code>
<i>🔖 Nomi:</i> {title}
<i>🔢 Soni:</i> {count}
<i>🧮 Foizi:</i> {percent}
<i>📆 Oy:</i> {month}
<i>💰 Puli:</i> {payments} {currency}
<i>💸 Oyiga tolov:</i> {one_month} {currency}

    """,
    'ru': """
    
<b> Тип платежа Рассрочка 💳 </b>
♻️Status: <code>{status}</code>
<i> 🔖 Имя: </i> {title}
<i> 🔢 Сони: </i> {count}
<i> 🧮 Процент: </i> {percent}
<i> 📆 Месяцев: </i> {month}
<i> 💰 Деньги: </i> {payments} {currency}
<i> 💸 Оплата в месяц: </i> {one_month} {currency}

    """
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
<b>Narxi</b>: <i>{count} x {price} = {all_price} {price_choice}</i>
<code>* * * * *</code>
        """,
    'ru': """
<b>Покупка:</b> <code>{status}</code>
<b>Имени:</b> <i>{title}</i>
<b>Цена:</b> <i>{count} x {price} = {all_price} {price_choice}</i>
<code>* * * * *</code>"""
}

ORDER_TEXT = {
    'uz': """<b>{a}.</b> <i>{title}
        <code>{count}x{price}={all_price} {currency} </code> {status}</i>\n""",
}

PRODUCT_INFO_ONE = {
    'uz': """
<b>Nomi:</b><a href="http://telegra.ph/{path}"> {title}</a>
<b>Narxi</b>: <i>{count} x {price} = {all_price} {price_choice}</i>

        """,
    'ru': """
<b>Имени:</b><a href="http://telegra.ph/{path}"> {title}</a>
<b>Цена:</b> <i>{count} x {price} = {all_price} {price_choice}</i>
"""
}

CLOSE = {
    'uz':"❌ Bekor qilish",
    'ru':"❌ Отменить действие"
}

KUPIT_SRAZU = {
    'uz': '✅ Tezkor Xarid',
    'ru': '✅ Купить сразу'
}

KUPIT_SRAZUS = {
    'uz': "Tezkor Xarid",
    'ru': "Купить сразу"
}


KUPIT_V_RASSROCHKU = {
    'uz': "✅ Bo`lib to`lash",
    'ru': "✅ Купить в рассрочку"
}

KUPIT_V_RASSROCHKUS = {
    'uz': "Bo`lib to`lash",
    'ru': "Купить в рассрочку"
}

KUPIT = {
    'uz': "Bo'lib to'lash turini tanlang",
    'ru': 'Выберите условия Рассрочки'
}

OTKAZAT =  {
    'uz': 'Rad qilish ❌',
    'ru': 'Отказать ❌'
}
ACCEPT ={
    'uz': 'Tasdiqlash ✅',
    'ru': 'Принятие ✅'
}

CANCELLED_ORDER = {
    'uz': """
<i>{title}
        <code>{count}x{price}={all_price} {currency} </code> {status}</i>\n""",
}

SEND_USER_CANCELLED_ORDER = {
    'uz': "Sizning №{id} raqamli buyurtmangiz qabul qilinmadi.",
    'ru': "Ваш заказ №{id} не принят."
}

ADMIN_CANCELLED_ORDER = {
    'uz': "<b>№{id} raqamli buyurtma Bekor qilindi</b>",
    'ru': "<b>№{id} цифровой заказ Отменен</b>"
}