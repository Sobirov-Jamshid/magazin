import os
import traceback
from pprint import pprint

from telegraph import Telegraph
import requests

import telebot
from telebot import types

import config
import template
from backendm.models import BotUser, Product, Category, OrderCredit, Order, ShopCard

bot = telebot.TeleBot(
    token=config.TOKEN,
    parse_mode='HTML',
)

telegraph = Telegraph()

telegraph.create_account(short_name='1337')

APP_DIR = os.path.join('..')


def language():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='Uz 🇺🇿', callback_data='uz'),
        types.InlineKeyboardButton(text='Ru 🇷🇺', callback_data='ru'),
    )
    return markup


def func(n: int) -> str:
    return '{:,}'.format(n).replace('.', ' ')


checked = 'Bo`lib to`lash'


def dic(call):
    print(call.data)
    call_data = call.data.split(CallTypes.SEP)
    call_id = call_data[1]
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    user.number1 = call_id
    user.save()
    print(user.number1)
    product_order(call)


class CallTypes():
    SEP = '|'
    NOTHING = 'Nothing'
    CATEGORY_SELECT = 'Category slect'
    PRODUCT_PAGE = 'Product page'
    ADD_TO_SHOP_CARD_CREDITS = 'Add to shop card credits'
    ADD_TO_SHOP_CARD = 'Add to shop card'
    SHOP_CARD_ONE_PAGE = 'shop card one page'
    SHOP_CARD_ONE_PLUS = 'shop card one plus'
    SHOP_CARD_ONE_MINUS = 'shop card one minus'
    SHOP_CARD_ONE_REMOVE = 'shop card one remove'
    SHOP_CARD_ONE_BUY = 'shop card one buy'
    SHOP_CARD_ALL_BUY = 'shop card all'
    SET_PROFIL = 'edit_profile'
    GET_PROFIL = 'get profile'
    KORZINA = 'Korzina'
    ORDER_CARD_ONE = 'order shop'
    BACK_OUT = 'Baack out'
    BACK_OUTS = 'Baack outs'
    SHOP_CARD_MONTH_MINUS = 'Shop card month minus'
    SHOP_CARD_MONTH_PLUS = 'Shop card month plus'
    SHOP_CARD_PROTSENT_PLUS = 'shop card protsent'
    SHOP_CARD_PROTSENT_MINUS = 'shop card protsent minus'

    @classmethod
    def sep_join(cls, *args):
        return cls.SEP.join(map(str, args))


def contact_keyboard(chat_id):
    user = BotUser.objects.get(user_id=chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(text=f"{template.SEND_CONTACT[user.language]}", request_contact=True)
    )
    return markup


def language_customer(chat_id):
    text = template.language
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=language()
    )


@bot.message_handler(commands=['start'])
def message_handler_start(message):
    chat_id = message.chat.id
    user = BotUser.objects.filter(user_id=chat_id)
    if not user.exists():
        BotUser.objects.create(
            user_id=chat_id, )
        language_customer(chat_id)
    else:
        user = BotUser.objects.get(user_id=chat_id)
        if user.bot_state == 0:
            language_customer(chat_id)
        else:
            text = template.KATEGORIYA_MESSAGE[user.language]
            bot.send_message(
                chat_id,
                text,
                reply_markup=products_keyboard(user.language)
            )
            user.number1 = 0
            user.month = 3
            user.save()


def set_name_message_handler(message):
    chat_id = message.chat.id
    name = message.text
    user = BotUser.objects.get(user_id=chat_id)
    if user.bot_state == 1:
        user.full_name = name
        user.bot_state += 1
        user.save()
        products_keyboard_handlers(message)


@bot.message_handler(content_types=['contact'])
def set_contact_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    pprint(message)
    contact = message.contact
    phone_number = contact.phone_number
    user.contact = phone_number
    user.save()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(template.CLOSE[user.language])
    msg = bot.send_message(chat_id, template.ADDRES_TO_YOU[user.language], reply_markup=markup)

    bot.register_next_step_handler(msg, addres_to_message, user)


@bot.message_handler(content_types=['contact'])
def set_contact_message_handlers(message, product_id):
    product_id = product_id
    chat_id = message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    contact = message.contact
    phone_number = contact.phone_number
    user.contact = phone_number
    user.save()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(template.CLOSE[user.language])
    msg = bot.send_message(chat_id, template.ADDRES_TO_YOU[user.language], reply_markup=markup)

    bot.register_next_step_handler(msg, address_to_message, user, product_id)


def address_to_message(message, user, product_id):
    text = message.text
    chat_id = message.chat.id
    if text in ["❌ Bekor qilish", "❌ Отменить действие"]:
        products_keyboard_handlers(message)
    else:
        shopcard = ShopCard.objects.get(id=product_id)
        print('--------------')
        print('1111111')
        print('--------------')

        if shopcard.chec == True:
            print('--------------')
            print('22222')
            print('--------------')
            order_card_one = OrderCredit.objects.create(
                user=user
            )
            order_card_one.products = shopcard.product.title
            order_card_one.count = shopcard.count
            order_card_one.protsent = shopcard.percent
            order_card_one.month = shopcard.month
            order_card_one.payments = shopcard.payments
            order_card_one.month_pay = shopcard.month_pay
            order_card_one.all_price = shopcard.payments
            order_card_one.save()
            ShopCard.objects.get(id=product_id).delete()
        else:
            order_card_one, _ = Order.objects.create(
                user=user
            )
            order_card_one.products = shopcard.product.title
            order_card_one.count = shopcard.count
            order_card_one.all_price = (shopcard.count * shopcard.product.price)
            order_card_one.save()
            ShopCard.objects.get(id=product_id).delete()

        user.address = text
        user.save()
        bot.send_message(
            chat_id=chat_id,
            text=template.ADDED_TO_SHOP_CARDS[user.language],
            reply_markup=products_keyboard(user.language)
        )


def addres_to_message(message, user):
    text = message.text
    chat_id = message.chat.id
    if text in ["❌ Bekor qilish", "❌ Отменить действие"]:
        products_keyboard_handlers(message)
    else:
        for shopcard in ShopCard.objects.filter(user=user):
            product_id = shopcard.id
            shop_card = ShopCard.objects.get(id=product_id)
            if shopcard.chec == True:

                order_card_all = OrderCredit.objects.create(
                    user=user,
                )
                order_card_all.products = shopcard.product.title
                order_card_all.count = shopcard.count
                order_card_all.protsent = shopcard.percent
                order_card_all.month = shopcard.month
                order_card_all.payments = shopcard.payments
                order_card_all.month_pay = shopcard.month_pay
                order_card_all.all_price = shopcard.payments
                order_card_all.save()
                ShopCard.objects.get(id=product_id).delete()
            else:
                order_card_all = Order.objects.create(
                    user=user,
                )
                order_card_all.products = shopcard.product.title
                order_card_all.count = shopcard.count
                order_card_all.all_price = (shop_card.count * shop_card.product.price)
                order_card_all.save()
                ShopCard.objects.get(id=product_id).delete()
        user.address = text
        user.save()
        bot.send_message(
            chat_id=chat_id,
            text=template.ADDED_TO_SHOP_CARDS[user.language],
            reply_markup=products_keyboard(user.language)
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_data_message(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data = call.data.split(CallTypes.SEP)
    call_type = call_data[0]
    print(call.data)
    if call_type == 'uz' or call_type == 'ru':
        user.language = call.data
        user.save()
        if user.bot_state == 0:
            if not user.full_name:
                text = template.NAME_MESSAGE[user.language]
                msg = bot.edit_message_text(
                    text=text,
                    chat_id=chat_id,
                    message_id=call.message.id
                )
                user.bot_state = 1
                user.save()
                bot.register_next_step_handler(msg, set_name_message_handler)
        else:
            text = template.LANGUAGE_EDIT[user.language]
            bot.delete_message(
                chat_id=chat_id,
                message_id=call.message.id
            )
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=text,
                show_alert=False,
                cache_time=7,
            )
            bot.send_message(
                chat_id=chat_id,
                text=template.START_MESSAGE[user.language],
                reply_markup=products_keyboard(user.language)
            )

    if call_type == CallTypes.NOTHING:
        return

    elif call_type == CallTypes.CATEGORY_SELECT:
        category_select_call_handler(call)

    elif call_type == CallTypes.PRODUCT_PAGE:
        product_page_call_handler(call)
    elif call_type == CallTypes.ADD_TO_SHOP_CARD:
        add_to_shop_card_call_handler(call)
    elif call_type == CallTypes.ADD_TO_SHOP_CARD_CREDITS:
        add_to_shop_card_credits_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ONE_PAGE:
        shop_cart_one_page_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ONE_PLUS:
        shop_card_one_plus_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ONE_MINUS:
        shop_card_one_minus_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ONE_REMOVE:
        shop_card_one_remove_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ONE_BUY:
        shop_card_one_buy(call)
    elif call_type == CallTypes.SET_PROFIL:
        customer_edit(call)
    elif call_type == CallTypes.GET_PROFIL:
        customer_profile(call, chat_id)
    elif call_type == CallTypes.KORZINA:
        shop_card_keyboard_handler(call)
    elif call_type == CallTypes.SHOP_CARD_ALL_BUY:
        shop_card_all_buy(call)
    elif call_type == CallTypes.BACK_OUT:
        products_keyboard_handler(call.message)
    elif call_type == CallTypes.BACK_OUTS:
        category_select_call_handler(call)
    elif call_type == 'order':
        dic(call)
    elif call_type == CallTypes.SHOP_CARD_MONTH_MINUS:
        shop_card_month_minus_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_MONTH_PLUS:
        shop_card_month_plus_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_PROTSENT_PLUS:
        shop_card_pratsent_plus_call_handler(call)
    elif call_type == CallTypes.SHOP_CARD_PROTSENT_MINUS:
        shop_card_pratsent_minus_call_handler(call)


def products_keyboard(language):
    categories = Category.objects.filter(parent=None)
    categories_keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        category_button = types.InlineKeyboardButton(
            text=category.name,
            callback_data=CallTypes.sep_join(
                CallTypes.CATEGORY_SELECT, category.id,
            )
        )
        categories_keyboard.add(category_button)

    if language == 'uz':
        categories_keyboard.add(
            types.InlineKeyboardButton(
                text='👤 Profil',
                callback_data=CallTypes.sep_join(
                    CallTypes.GET_PROFIL
                )
            ),
            types.InlineKeyboardButton(
                text='🧺 Savatcha',
                callback_data=CallTypes.sep_join(
                    CallTypes.KORZINA
                )
            )
        )
        return categories_keyboard
    else:
        categories_keyboard.add(
            types.InlineKeyboardButton(
                text='👤 Профиль',
                callback_data=CallTypes.sep_join(
                    CallTypes.GET_PROFIL
                )
            ),
            types.InlineKeyboardButton(
                text='🧺 Корзина',
                callback_data=CallTypes.sep_join(
                    CallTypes.KORZINA
                )
            )
        )
        return categories_keyboard


def products_keyboard_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    text = template.KATEGORIYA_MESSAGE[user.language]
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=message.message_id,
        reply_markup=products_keyboard(user.language)
    )


def products_keyboard_handlers(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    user.number = 1
    user.save()
    bot.send_message(
        chat_id=chat_id,
        text='.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.delete_message(chat_id=chat_id, message_id=message.id + 1)
    text = template.KATEGORIYA_MESSAGE[user.language]
    bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=products_keyboard(user.language)
    )


def category_select_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data = call.data.split(CallTypes.SEP)
        print(call_data, call.data)
        category_id = int(call_data[1])
        if category_id == 0:
            categories = Category.objects.filter(parent=None)
        else:
            main_category = Category.objects.get(id=category_id)
            categories = Category.objects.filter(parent=main_category)
            if not categories.exists():
                product = Product.objects.filter(category=main_category).first()
                send_product_page(call, chat_id, product)
                return

        categories_keyboard = types.InlineKeyboardMarkup()
        for category in categories:
            category_button = types.InlineKeyboardButton(
                text=category.name,
                callback_data=CallTypes.sep_join(
                    CallTypes.CATEGORY_SELECT, category.id,
                )
            )
            categories_keyboard.add(category_button)
        if user.language == 'uz':
            categories_keyboard.add(
                types.InlineKeyboardButton(
                    text='👤 Profil',
                    callback_data=CallTypes.sep_join(
                        CallTypes.GET_PROFIL
                    )
                ),
                types.InlineKeyboardButton(
                    text='🧺 Savatcha',
                    callback_data=CallTypes.sep_join(
                        CallTypes.KORZINA
                    )
                )
            )
        else:
            categories_keyboard.add(
                types.InlineKeyboardButton(
                    text='👤 Профиль',
                    callback_data=CallTypes.sep_join(
                        CallTypes.GET_PROFIL
                    )
                ),
                types.InlineKeyboardButton(
                    text='🧺 Корзина',
                    callback_data=CallTypes.sep_join(
                        CallTypes.KORZINA
                    )
                )
            )

        if category_id and main_category.parent:
            parent_id = main_category.parent.id
        else:
            parent_id = 0

        if category_id:
            back_button = types.InlineKeyboardButton(
                text=template.BACK[user.language],
                callback_data=CallTypes.sep_join(
                    CallTypes.CATEGORY_SELECT, parent_id,
                )
            )
            categories_keyboard.add(back_button)
        text = template.KATEGORIYA_MESSAGE[user.language]
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=categories_keyboard,
        )
    except Exception as e:
        print(e)


def make_product_page_keyboard(category, index, user):
    try:

        product = Product.objects.filter(category=category)[index]
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        print(index)
        print('######################')
        page_buttons = [
            types.InlineKeyboardButton(
                text='⬅️',
                callback_data=CallTypes.sep_join(
                    CallTypes.PRODUCT_PAGE, category.id, index, -1,
                )
            ),
            types.InlineKeyboardButton(
                text=str(index + 1),
                callback_data=CallTypes.sep_join(
                    CallTypes.NOTHING,
                )
            ),
            types.InlineKeyboardButton(
                text='➡️',
                callback_data=CallTypes.sep_join(
                    CallTypes.PRODUCT_PAGE, category.id, index, 1,
                )
            ),
        ]

        plus_minus_buttons = [
            types.InlineKeyboardButton(
                text='➖',
                callback_data=CallTypes.sep_join(
                    CallTypes.SHOP_CARD_ONE_MINUS, index, category.id,
                )
            ),
            types.InlineKeyboardButton(
                text=f'{user.number}',
                callback_data=CallTypes.NOTHING
            ),
            types.InlineKeyboardButton(
                text='➕',
                callback_data=CallTypes.sep_join(
                    CallTypes.SHOP_CARD_ONE_PLUS, index, category.id,
                )
            ),
        ]

        if user.number1 == 0:

            order = [
                types.InlineKeyboardButton(
                    text="✅ Tezkor Xarid",
                    callback_data=CallTypes.sep_join(
                        'order', 0, index, category.id,
                    )
                ),
                types.InlineKeyboardButton(
                    text="Bo`lib to`lash",
                    callback_data=CallTypes.sep_join(
                        'order', 1, index, category.id,
                    )
                )
            ]
            add_to_shop_card_button = types.InlineKeyboardButton(
                text=template.ADD_TO_SHOP_CARD[user.language],
                callback_data=CallTypes.sep_join(
                    CallTypes.ADD_TO_SHOP_CARD, product.id,
                )
            )
        else:
            order = [types.InlineKeyboardButton(
                text="Tezkor Xarid",
                callback_data=CallTypes.sep_join(
                    'order', 0, index, category.id,
                )
            ),
                types.InlineKeyboardButton(
                    text="✅ Bo`lib to`lash",
                    callback_data=CallTypes.sep_join(
                        'order', 1, index, category.id,
                    )
                )
            ]
            alifshop = [types.InlineKeyboardButton(
                text="AlifShop",
                callback_data=CallTypes.NOTHING
            ),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=CallTypes.NOTHING
                )
            ]
            # one_payments = types.InlineKeyboardButton(
            #         text=f'Birinchi to`lov: {one_pay} so`m',
            #         callback_data=CallTypes.NOTHING
            #     )
            credit_order = types.InlineKeyboardButton(
                text="Bo'lib to'lash turini tanlang",
                callback_data=CallTypes.NOTHING
            )
            kredit = [
                types.InlineKeyboardButton(
                    text='➖',
                    callback_data=CallTypes.sep_join(
                        CallTypes.SHOP_CARD_MONTH_MINUS, index, category.id,
                    )
                ),
                types.InlineKeyboardButton(
                    text=f'{user.month}',
                    callback_data=CallTypes.NOTHING
                ),
                types.InlineKeyboardButton(
                    text='➕',
                    callback_data=CallTypes.sep_join(
                        CallTypes.SHOP_CARD_MONTH_PLUS, index, category.id,
                    )
                ),
            ]
            payment_credit = [
                types.InlineKeyboardButton(
                    text='➖',
                    callback_data=CallTypes.sep_join(
                        CallTypes.SHOP_CARD_PROTSENT_MINUS, index, category.id
                    )
                ),
                types.InlineKeyboardButton(
                    text=f'Birinchi to`lov: {user.protsent} %',
                    callback_data=CallTypes.NOTHING
                ),
                types.InlineKeyboardButton(
                    text='➕',
                    callback_data=CallTypes.sep_join(
                        CallTypes.SHOP_CARD_PROTSENT_PLUS, index, category.id,
                    )
                ),
            ]
            if user.protsent == 0:
                one_pay = 0
            else:
                one_pay = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100))
            one_payments = types.InlineKeyboardButton(
                text=f'Birinchi to`lov: {one_pay} so`m',
                callback_data=CallTypes.NOTHING
            )
            add_to_shop_card_button = types.InlineKeyboardButton(
                text=template.ADD_TO_SHOP_CARD[user.language],
                callback_data=CallTypes.sep_join(
                    CallTypes.ADD_TO_SHOP_CARD_CREDITS, product.id, user.month, user.protsent, user.number
                )
            )

        keyboard.add(*page_buttons)
        keyboard.add(*plus_minus_buttons)
        keyboard.add(*order)
        if user.number1 == 1:
            keyboard.add(*alifshop)
            keyboard.add(credit_order)
            keyboard.add(*kredit)
            keyboard.add(*payment_credit)
            keyboard.add(one_payments)
            keyboard.add(add_to_shop_card_button)
        else:
            keyboard.add(add_to_shop_card_button)
        if user.language == 'uz':
            keyboard.add(
                types.InlineKeyboardButton(
                    text=template.BACK[user.language],
                    callback_data=CallTypes.sep_join(
                        CallTypes.BACK_OUTS, category.parent.id
                    )
                ),
                types.InlineKeyboardButton(
                    text='🧺 Savatcha',
                    callback_data=CallTypes.sep_join(
                        CallTypes.KORZINA
                    )
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=template.BACK[user.language],
                    callback_data=CallTypes.sep_join(
                        CallTypes.BACK_OUTS, category.parent, id
                    )
                ),
                types.InlineKeyboardButton(
                    text='🧺 Корзина',
                    callback_data=CallTypes.sep_join(
                        CallTypes.KORZINA
                    )
                )
            )

        return keyboard


    except Exception as e:
        traceback.print_exc()


def send_product_page(call, chat_id, product):
    try:
        user = BotUser.objects.get(user_id=chat_id)
        text = template.PRODUCTS_INFO[user.language]
        user.number = 1
        user.month = 3
        user.number1 = 0
        user.protsent = 0
        user.save()
        image_path = os.path.join(APP_DIR, product.image.name)
        keyboard = make_product_page_keyboard(product.category, 0, user)
        with open(image_path, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload', files={'file':
                                                        ('file', f, 'image/jpeg')}).json()[0]['src']

        response = telegraph.create_page(
            f'{product.title}',
            html_content=f"<img src='{path}'/>"
                         f"{product.description}",
        )
        text = template.PRODUCT_INFO_ONE[user.language]
        bot.edit_message_text(
            text=text.format(
                path=response['path'],
                title=product.title,
                count=user.number,
                price=product.price,
                all_price=user.number * product.price
            ),
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)


def product_page_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        user.number = 1
        user.month = 3
        user.number1 = 0
        user.protsent = 0
        user.save()
        call_data_list = call.data.split(CallTypes.SEP)
        category_id = int(call_data_list[1])
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
        index = int(call_data_list[2])
        adding = int(call_data_list[3])
        product_count = products.count()
        next_product_index = (index + adding + product_count) % product_count
        product = products[next_product_index]
        image_path = os.path.join(APP_DIR, product.image.name)
        print(image_path)
        keyboard = make_product_page_keyboard(category, next_product_index, user)
        with open(image_path, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload', files={'file':
                                                        ('file', f,
                                                         'image/jpeg')}).json()[0]['src']

        response = telegraph.create_page(
            f'{product.title}',
            html_content=f"<img src='{path}'/>",
        )
        text = template.PRODUCT_INFO_ONE[user.language]
        bot.edit_message_text(
            text=text.format(
                path=response['path'],
                title=product.title,
                count=user.number,
                price=product.price,
                all_price=user.number * product.price
            ),
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )

    except Exception as e:
        print(e)


def add_to_shop_card_call_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    product_id = call_data_list[1]
    product = Product.objects.get(id=product_id)
    print(call.data)
    shop_card_one, _ = ShopCard.objects.get_or_create(
        user=user,
        product=product
    )
    # shop_card_credits, _ = Order
    if user.number1 == 0:
        shop_card_one.count = user.number
        shop_card_one.save()
    else:
        pass
    text = template.ADDED_TO_SHOP_CARD[user.language]
    bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False,
        cache_time=7
    )


def add_to_shop_card_credits_call_handler(call):
    chat_id = call.message.chat.id

    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    product_id = call_data_list[1]
    month = int(call_data_list[2])
    protsent = int(call_data_list[3])
    number = int(call_data_list[4])
    product = Product.objects.get(id=product_id)
    shop_card_one, _ = ShopCard.objects.get_or_create(
        user=user,
        product=product
    )
    # shop_card_credits, _ = Order
    shop_card_one.count = user.number
    shop_card_one.percent = protsent
    shop_card_one.month = month
    shop_card_one.payments = number * (product.price * 0.15 + product.price)
    shop_card_one.month_pay = number * (product.price * 0.15 + product.price) / month
    if protsent > 0:
        shop_card_one.payments = number * ((product.price * 0.15 + product.price) * (protsent / 100) + product.price)
    shop_card_one.status = checked
    shop_card_one.chec = True
    shop_card_one.save()

    text = template.ADDED_TO_SHOP_CARD[user.language]
    bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False,
        cache_time=7
    )


def make_shop_card_one_keyboard(user, index, language):
    print(index)
    print('*********************')
    shop_cards = ShopCard.objects.filter(user=user)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    product = shop_cards[index].product
    back_button = [
        types.InlineKeyboardButton(
            text=template.BACK[user.language],
            callback_data=CallTypes.sep_join(
                CallTypes.BACK_OUT
            )
        ),
        types.InlineKeyboardButton(
            text='Yangilash',
            callback_data=CallTypes.sep_join(
                CallTypes.KORZINA
            )
        )
    ]
    remove_button = list()
    text = template.MESSAGE_SHOP_CARD[language]

    for shop in shop_cards:
        button = [
            types.InlineKeyboardButton(
                text='    ❌    ',
                callback_data=CallTypes.sep_join(
                    CallTypes.SHOP_CARD_ONE_REMOVE, index,
                )
            ),
            types.InlineKeyboardButton(
                text=f"{shop.product.title}",
                callback_data=CallTypes.sep_join(
                    CallTypes.NOTHING
                )
            ),
            types.InlineKeyboardButton(
                text=f"{text}",
                callback_data=CallTypes.sep_join(
                    CallTypes.SHOP_CARD_ONE_BUY, shop.id, index
                )
            )
        ]
        remove_button += button

    price_all = 0
    for shop_card_one in shop_cards:
        price_one = shop_card_one.product.price * shop_card_one.count
        price_all += price_one
    text = template.MESSAGE_SHOP_CARDS[language]
    buy_all_button = types.InlineKeyboardButton(
        text=f'{text} ({price_all})',
        callback_data=CallTypes.sep_join(
            CallTypes.SHOP_CARD_ALL_BUY,
        )
    )

    keyboard.add(*back_button)
    keyboard.add(*remove_button)
    keyboard.add(buy_all_button)
    return keyboard


def make_shop_card_one(user, index):
    shop_cards = ShopCard.objects.filter(user=user)

    a = 1
    text = template.PRODUCT_INFO_TEXT[user.language]
    product_info = template.PRODUCT_INFO_UP[user.language]
    for shop in shop_cards:
        print(shop)
        product_info += text.format(
            status=shop.status,
            title=shop.product.title,
            count=shop.count,
            price=shop.product.price,
            all_price=shop.count * shop.product.price
        )
        a += 1
    keyboard = make_shop_card_one_keyboard(user, index, user.language)
    return product_info, keyboard


def make_product_card_one(user, category_id, index):
    product = Product.objects.filter(category=category_id)[index]
    image_path = os.path.join(APP_DIR, product.image.name)
    keyboard = make_product_page_keyboard(category=product.category, index=index, user=user)
    return product, image_path, keyboard


def shop_card_keyboard_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    if not ShopCard.objects.filter(user=user).exists():
        text = template.EMPTY_SHOP_CARDS[user.language]
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=text,
            show_alert=False,
        )
        return

    product_info, keyboard = make_shop_card_one(user, 0)  # image_path,

    bot.edit_message_text(
        text=product_info,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def shop_cart_one_page_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        index = int(call_data_list[1])
        adding = int(call_data_list[2])
        shop_cards = ShopCard.objects.filter(user=user)
        shop_cards_count = shop_cards.count()
        next_shop_card_one_index = (index + adding + shop_cards_count)
        next_shop_card_one_index %= shop_cards_count

        if next_shop_card_one_index == index:
            return

        product_info, keyboard = make_shop_card_one(  # image_path,
            user,
            next_shop_card_one_index,
        )

        bot.edit_message_text(
            text=product_info,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )
    except Exception as e:
        traceback.print_exc()


def shop_card_one_plus_call_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    index = int(call_data_list[1])
    category_id = int(call_data_list[2])
    user.number += 1
    user.save()

    product, image_path, keyboard = make_product_card_one(
        user,
        category_id,
        index,
    )

    with open(image_path, 'rb') as f:
        path = requests.post(
            'https://telegra.ph/upload', files={'file':
                                                    ('file', f,
                                                     'image/jpeg')}).json()[0]['src']
    response = telegraph.create_page(
        f'{product.title}',
        html_content=f"<img src='{path}'/>"
                     f"{product.description}",
    )

    if user.number1 == 1:
        all_price = user.number * (product.price * 0.15 + product.price)
        if user.protsent > 0:
            all_price = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

        month_price = user.number * (
                (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month
        print(all_price)
        text = template.PRODUCT_INFO[user.language].format(
            path=response['path'],
            title=product.title,
            count=user.number,
            protsent=user.month,
            one_pay=round(month_price, 2),
            all_price=all_price,
        )
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )
    else:
        text = template.PRODUCT_INFO_ONE[user.language]
        bot.edit_message_text(
            text=text.format(
                path=response['path'],
                title=product.title,
                count=user.number,
                price=product.price,
                all_price=user.number * product.price
            ),
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )


def shop_card_one_minus_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        index = int(call_data_list[1])
        category_id = int(call_data_list[2])
        if user.number <= 1:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text='Boshqa o`zgarita olmaysiz',
                show_alert=False
            )
        else:
            user.number -= 1
            user.save()

        product, image_path, keyboard = make_product_card_one(
            user,
            category_id,
            index,
        )

        with open(image_path, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload', files={'file':
                                                        ('file', f,
                                                         'image/jpeg')}).json()[0]['src']

        response = telegraph.create_page(
            f'{product.title}',
            html_content=f"<img src='{path}'/>"
                         f"{product.description}",
        )
        if user.number1 == 1:
            all_price = user.number * (product.price * 0.15 + product.price)
            if user.protsent > 0:
                all_price = user.number * (
                        (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

            month_price = user.number * (
                    (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

            text = template.PRODUCT_INFO[user.language].format(
                path=response['path'],
                title=product.title,
                count=user.number,
                protsent=user.month,
                one_pay=round(month_price, 2),
                all_price=all_price,
            )
            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard
            )
        else:
            text = template.PRODUCT_INFO_ONE[user.language]
            bot.edit_message_text(
                text=text.format(
                    path=response['path'],
                    title=product.title,
                    count=user.number,
                    price=product.price,
                    all_price=user.number * product.price
                ),
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard
            )
    except Exception as e:
        traceback.print_exc()


def shop_card_pratsent_plus_call_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    index = int(call_data_list[1])
    category_id = int(call_data_list[2])
    if user.protsent == 50:
        user.protsent = 0
        user.save()
    else:
        user.protsent += 10
        user.save()

    product, image_path, keyboard = make_product_card_one(
        user,
        category_id,
        index,
    )

    with open(image_path, 'rb') as f:
        path = requests.post(
            'https://telegra.ph/upload', files={'file':
                                                    ('file', f,
                                                     'image/jpeg')}).json()[0]['src']

    response = telegraph.create_page(
        f'{product.title}',
        html_content=f"<img src='{path}'/>"
                     f"{product.description}",
    )

    all_price = user.number * (product.price * 0.15 + product.price)
    if user.protsent > 0:
        all_price = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

    month_price = user.number * (
            (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

    text = template.PRODUCT_INFO[user.language].format(
        path=response['path'],
        title=product.title,
        count=user.number,
        protsent=user.month,
        one_pay=round(month_price, 2),
        all_price=all_price,
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def shop_card_pratsent_minus_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        index = int(call_data_list[1])
        category_id = int(call_data_list[2])
        if user.protsent <= 1:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text='Boshqa o`zgarita olmaysiz',
                show_alert=False
            )
        else:
            user.protsent -= 10
            user.save()

        product, image_path, keyboard = make_product_card_one(
            user,
            category_id,
            index,
        )

        with open(image_path, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload', files={'file':
                                                        ('file', f,
                                                         'image/jpeg')}).json()[0]['src']

        response = telegraph.create_page(
            f'{product.title}',
            html_content=f"<img src='{path}'/>"
                         f"{product.description}",
        )

        all_price = user.number * (product.price * 0.15 + product.price)
        if user.protsent > 0:
            all_price = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

        month_price = user.number * (
                (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

        text = template.PRODUCT_INFO[user.language].format(
            path=response['path'],
            title=product.title,
            count=user.number,
            protsent=user.month,
            one_pay=round(month_price, 2),
            all_price=all_price,
        )
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )
    except Exception as e:
        traceback.print_exc()


def shop_card_month_plus_call_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    index = int(call_data_list[1])
    category_id = int(call_data_list[2])
    if user.month == 15:
        user.month = 3
        user.save()
    else:
        user.month += 3
        user.save()
    print('*************************')
    print(index)
    print('*************************')
    product, image_path, keyboard = make_product_card_one(
        user,
        category_id,
        index,
    )

    with open(image_path, 'rb') as f:
        path = requests.post(
            'https://telegra.ph/upload', files={'file':
                (
                    'file', f, 'image/jpeg'
                )}).json()[0]['src']

    response = telegraph.create_page(
        f'{product.title}',
        html_content=f"<img src='{path}'/>"
                     f"{product.description}",
    )
    all_price = user.number * (product.price * 0.15 + product.price)
    if user.protsent > 0:
        all_price = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

    month_price = user.number * (
            (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

    text = template.PRODUCT_INFO[user.language].format(
        path=response['path'],
        title=product.title,
        count=user.number,
        protsent=user.month,
        one_pay=round(month_price, 2),
        all_price=all_price,
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def shop_card_month_minus_call_handler(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        index = int(call_data_list[1])
        category_id = int(call_data_list[2])
        if user.month <= 3:
            user.month = 15
            user.save()
        else:
            user.month -= 3
            user.save()

        product, image_path, keyboard = make_product_card_one(
            user,
            category_id,
            index,
        )

        with open(image_path, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload', files={'file':
                                                        ('file', f,
                                                         'image/jpeg')}).json()[0]['src']

        response = telegraph.create_page(
            f'{product.title}',
            html_content=f"<img src='{path}'/>"
                         f"{product.description}",
        )
        # all_price = user.number * product.price
        all_price = user.number * (product.price * 0.15 + product.price)
        if user.protsent > 0:
            all_price = user.number * ((product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

        month_price = user.number * (
                (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

        text = template.PRODUCTS_INFO[user.language].format(
            path={response['path']},
            title=product.title,
            count=user.number,
            one_pay=round(month_price, 2),
            all_price=all_price,
        )
        bot.edit_message_text(
            # text=f"""<a href="https://telegra.ph/{response['path']}">{product.title}</a>""",
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard
        )
    except Exception as e:
        traceback.print_exc()


def product_order(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        print('***********')
        print(call_data_list)
        print('***********')
        index = int(call_data_list[2])
        category_id = int(call_data_list[3])
        product, image_path, keyboard = make_product_card_one(
            user,
            category_id,
            index,
        )
        if user.number1 == 1:
            with open(image_path, 'rb') as f:
                path = requests.post(
                    'https://telegra.ph/upload', files={'file':
                                                            ('file', f,
                                                             'image/jpeg')}).json()[0]['src']
            response = telegraph.create_page(
                f'{product.title}',
                html_content=f"<img src='{path}'/>"
                             f"{product.description}",

            )
            print(response['path'])
            all_price = user.number * (product.price * 0.15 + product.price)
            if user.protsent > 0:
                all_price = user.number * (
                        (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

            month_price = user.number * (
                    (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month
            text = template.PRODUCT_INFO[user.language].format(
                path=response['path'],
                title=product.title,
                count=user.number,
                protsent=user.month,
                one_pay=round(month_price, 2),
                all_price=all_price,
            )
            bot.edit_message_text(
                # text=f"""<a href="http://telegra.ph/{response['path']}">{product.title}</a>\nNarx: {product.price}""",
                text=text,
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard
            )
        else:
            with open(image_path, 'rb') as f:
                path = requests.post(
                    'https://telegra.ph/upload', files={'file':
                                                            ('file', f,
                                                             'image/jpeg')}).json()[0]['src']
            response = telegraph.create_page(
                f'{product.title}',
                html_content=f"<img src='{path}'/>"
                             f"{product.description}",
            )
            all_price = user.number * (product.price * 0.15 + product.price)
            if user.protsent > 0:
                all_price = user.number * (
                            (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price)

            one_pay = all_price * (user.protsent / 100)

            month_price = user.number * (
                        (product.price * 0.15 + product.price) * (user.protsent / 100) + product.price) / user.month

            bot.edit_message_text(
                text=template.PRODUCT_INFO[user.language].format(
                    path=response['path'],
                    title=product.title,
                    count=user.number,
                    protsent=user.month,
                    one_pay=round(month_price, 2),
                    all_price=all_price,
                ),
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard
            )

    except Exception as e:
        traceback.print_exc()


def shop_card_one_remove_call_handler(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(user_id=chat_id)
    call_data_list = call.data.split(CallTypes.SEP)
    index = int(call_data_list[1])
    shop_cards = ShopCard.objects.filter(user=user)
    shop_card_one = shop_cards[index]
    shop_card_one.delete()
    shop_cards = ShopCard.objects.filter(user=user)
    shop_cards_count = shop_cards.count()
    if shop_cards_count == 0:
        category_select_call_handler(call)
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=template.EMPTY_SHOP_CARDS[user.language],
            show_alert=False
        )

        return

    index %= shop_cards_count
    # shop_card_one = shop_cards[index]
    product_info, keyboard = make_shop_card_one(  # image_path,
        user,
        index,
    )
    bot.edit_message_text(
        text=product_info,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def shop_card_one_buy(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        print(call.data)
        call_data_list = call.data.split(CallTypes.SEP)
        product_id = int(call_data_list[1])
        index = int(call_data_list[2])
        msg = bot.send_message(
            chat_id=chat_id,
            text=template.SEND_CONTACTS[user.language],
            reply_markup=contact_keyboard(chat_id)
        )
        # msg=bot.edit_message_text(
        #     text=template.SEND_CONTACTS[user.language],
        #     chat_id=chat_id,
        #     message_id=call.message.id,
        #     reply_markup=contact_keyboard(chat_id)
        # )
        bot.register_next_step_handler(msg, set_contact_message_handlers, product_id)
        shop_cards = ShopCard.objects.filter(user=user)
        if shop_cards.exists():
            a = 1
            text = template.PRODUCT_INFO_TEXT[user.language]
            product_info = template.PRODUCT_INFO_UP[user.language]
            keyboard = make_shop_card_one_keyboard(user, index, user.language)

            for shop in shop_cards:
                print(shop)
                text = text.format(
                    status=shop.status,
                    title=shop.product.title,
                    count=shop.count,
                    price=shop.product.price,
                    all_price=shop.count * shop.product.price
                )
                a += 1
                product_info += text
            bot.edit_message_text(
                text=product_info,
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard
            )
        else:
            text = template.NOT_PRODUCT_MESSAGE[user.language]
            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=products_keyboard(user.language)
            )

    except Exception as e:
        traceback.print_exc()


def shop_card_all_buy(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        msg = bot.send_message(
            chat_id=chat_id,
            text=template.SEND_CONTACTS[user.language],
            reply_markup=contact_keyboard(chat_id)
        )
        bot.register_next_step_handler(msg, set_contact_message_handler)
        # text = template.ADDED_TO_SHOP_CARDS[user.language]
        # bot.edit_message_text(
        #     text=template.KATEGORIYA_MESSAGE[user.language],
        #     chat_id=chat_id,
        #     message_id=call.message.id,
        #     reply_markup=products_keyboard(user.language)
        # )
        # bot.answer_callback_query(
        #     callback_query_id=call.id,
        #     text=text,
        #     show_alert=False,
        #     cache_time=7
        # )
    except Exception as e:
        traceback.print_exc()


def user_profile_keyboard(language):
    markup = types.InlineKeyboardMarkup(row_width=1)

    text = template.CUSTOMER_PROFILE_ORDER[language]
    print(text)
    name = types.InlineKeyboardButton(text=text, callback_data=CallTypes.sep_join(CallTypes.SET_PROFIL, 1))
    text1 = template.CUSTOMER_PROFILE_LANGUAGE[language]
    name1 = types.InlineKeyboardButton(text=text1, callback_data=CallTypes.sep_join(CallTypes.SET_PROFIL, 2))
    back_button = types.InlineKeyboardButton(
        text=template.BACK[language],
        callback_data=CallTypes.sep_join(
            CallTypes.BACK_OUT))
    markup.add(name, name1, back_button)
    return markup


def customer_profile(call, chat_id):
    user = BotUser.objects.get(user_id=chat_id)
    text1 = template.CUSTOMER_PROFILE[user.language]

    bot.edit_message_text(
        text=text1,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=user_profile_keyboard(user.language)
    )


def customer_edit(call):
    try:
        chat_id = call.message.chat.id
        user = BotUser.objects.get(user_id=chat_id)
        call_data_list = call.data.split(CallTypes.SEP)
        print(call.data)
        edit_id = call_data_list[1]
        print(type(edit_id))
        if edit_id == '1':
            my_orders = Order.objects.filter(user=user)
            my_order = OrderCredit.objects.filter(user=user)
            if my_orders.exists() or my_order.exists():
                text = "<b>📦 Maxsulotlar:</b>\n"
                a = 1
                summa = 0
                for order in my_orders:
                    text += template.ORDER_TEXT['uz'].format(
                        a=a,
                        title=order.products,
                        count=order.count,
                        price=int(order.all_price / order.count),
                        all_price=order.all_price
                    )
                    summa += order.all_price
                    a += 1
                
                for order in my_orders:
                    text += template.ORDER_TEXT['uz'].format(
                        a=a,
                        title=order.products,
                        count=order.count,
                        price=int(order.all_price / order.count),
                        all_price=order.all_price
                    )
                    a += 1
                    summa += order.all_price
                bot.edit_message_text(
                    text=f"{text}\n<b>💵 Jami summa: </b><code>{summa}</code> <b>So'm</b>",
                    chat_id=chat_id,
                    message_id=call.message.id,
                    reply_markup=user_profile_keyboard(user.language)
                )

            else:
                text = template.NOT_PRODUCT_MESSAGE[user.language]
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    text=text,
                    show_alert=True,
                )
        elif edit_id == "2":
            text = template.language
            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=language())
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    bot.polling()
