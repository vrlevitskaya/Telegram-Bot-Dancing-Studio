import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
import datetime

from payments import add_payment_to_csv, get_users

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

user_data = {}  # словарь для хранения данных пользователей
selected_users = {}
month = None
date = None

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я бот танцевальной студии "Искра"',
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def send_contacts(message):
    bot.send_message(message.chat.id, 'По вопросам или ошибкам: https://t.me/vlone_l', parse_mode=ParseMode.HTML)


@bot.message_handler(commands=['set_month'])
def set_month(message):
    global month
    month = datetime.datetime.now().strftime("%B")
    bot.send_message(message.chat.id, f'Текущий месяц установлен: <b>{month}</b>', parse_mode=ParseMode.HTML)


@bot.message_handler(commands=['add_payment'])
def add_payment_start(message):
    msg = bot.send_message(message.chat.id, "Введите имя танцора")
    bot.register_next_step_handler(msg, add_surname_name)


def add_surname_name(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        surname_name = message.text
        user_data["Имя_Фамилия"] = surname_name
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Имя_Фамилия: <b>{surname_name}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите группу танцора", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_group)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_group(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        group = message.text
        user_data["Группа"] = group
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Группа: <b>{group}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите вид абонемента", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_abonement)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_abonement(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        abonement = message.text
        user_data["Вид_абонемента"] = abonement
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Абонемент: <b>{abonement}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите стоимость абонемента", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_abonement_cost)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_abonement_cost(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        abonement_cost = message.text
        user_data["Стоимость"] = abonement_cost
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Стоимость абонемента: <b>{abonement_cost}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите способ оплаты", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_payment_method)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_payment_method(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        payment_method = message.text
        user_data["Способ_оплаты"] = payment_method
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Способ оплаты: <b>{payment_method}</b>\n"
                                                f"Если данные неверны, введите /cancel.\n"
                                                "Введите дату покупки абонемента", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_purchase_date)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_purchase_date(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        date_of_purchase = message.text
        user_data["Дата_покупки"] = date_of_purchase
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Дата покупки: <b>{date_of_purchase}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите дату окончания абонемента", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_ending_date)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_ending_date(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        ending_date = message.text
        user_data["Дата_окончания"] = ending_date
        msg = bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                                f"Дата окончания: <b>{ending_date}</b>\n"
                                                "Если данные неверны, введите /cancel.\n"
                                                "Введите комментарий, номер телефона и имя родителя, если необходимо.",
                               parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(msg, add_comments)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def add_comments(message):
    try:
        if message.text == '/cancel':
            cancel_payment(message)
            return
        comments = message.text
        user_data["Комментарий"] = comments
        bot.send_message(message.chat.id, f"Вы ввели следующие данные для платежа:\n"
                                          f"Комментарий, номер телефона и имя родителя: <b>{comments}</b>\n"
                                          f"Вы ввели все данные.\n"
                                          "Если данные неверны, введите /cancel.\n"
                                          "Если верны, введите /confirm ", parse_mode=ParseMode.HTML)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке данных платежа: {e}")


def confirm_payment(message, month):
    if len(user_data) != 8:
        bot.send_message(message.chat.id, "Данных для добавления платежа недостаточно")
        return

    try:
        add_payment_to_csv(user_data, month=month)
        user_data.clear()
        bot.send_message(message.chat.id, "Платеж успешно добавлен.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при добавлении платежа: {e}")


@bot.message_handler(commands=['confirm'])
def confirm_payment_wrapper(message):
    global month
    if month is None:
        bot.send_message(message.chat.id, "Месяц не был установлен. Установите месяц с помощью команды /set_month.")
        return

    confirm_payment(message, month)


@bot.message_handler(commands=['cancel'])
def cancel_payment(message):
    if user_data:
        user_data.clear()
        bot.send_message(message.chat.id, "Добавление платежа отменено.")
    else:
        bot.send_message(message.chat.id, "В данный момент нет активного процесса добавления платежа.")


@bot.message_handler(commands=['mark_visits'])
def start_mark_visits(message):
    global selected_users
    global month
    if month is None:
        bot.send_message(message.chat.id, "Месяц не был установлен. Установите месяц с помощью команды /set_month.")
        return

    selected_users = {}
    users = get_users(month=month)
    markup = ReplyKeyboardMarkup(row_width=2)
    for user in users:
        markup.add(KeyboardButton(user))
    bot.send_message(message.chat.id, 'Выберите пользователей (можно выбрать несколько):', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global selected_users
    global month
    if month is None:
        bot.send_message(message.chat.id, "Месяц не был установлен. Установите месяц с помощью команды /set_month.")
        return
    if message.text in get_users(month):
        if message.text in selected_users:
            del selected_users[message.text]
        else:
            selected_users[message.text] = True
    elif message.text == 'Готово':
        selected_users_list = list(selected_users.keys())
        if selected_users_list:
            bot.send_message(message.chat.id, f'Вы выбрали следующих пользователей: {", ".join(selected_users_list)}')
        else:
            bot.send_message(message.chat.id, 'Вы не выбрали ни одного пользователя :(.')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте кнопки для выбора пользователей.')


bot.polling(none_stop=True)
