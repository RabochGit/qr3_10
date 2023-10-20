import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6421628134:AAFM5AD-vxQ454WkKV8XJ2X_ChbVQB5Qz9s",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Категории"  
text_button_1 = "История"  
text_button_2 = "Игроки"  
text_button_3 = "Достижения" 


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Вас приветствует любительский футбольный клуб `*Феникс*` г. Вязники. Предлагаем ознакомиться с фактами небольшой, но уже довольно насыщенной истории нашей команды!',  
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Какой _факт_ о нашей команде Вас заинтересовал?')  
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, "[Замечательно!За свежими новостями и событиями нашей команды Вы можете наблюдать в сообществе вконтакте](https://vk.com/club210591959)")
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Благодарим за интерес к нашей команде!', reply_markup=menu_keyboard)  
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Многим известно, что истоки наш футбольный клуб берет из _пожарно-спасательной части_ города *Вязники*, где работают и проходят службу большинство игроков нашей молодой команды.Идея организовать свою команду пришла к нам довольно-таки давно, но всерьёз реализовать её мы решились в сентябре 2020 года, после успешного выступления на Спартакиаде среди рабочих и служащих предприятий, учреждений и управлений всех форм собственности Вязниковского района.Именно тогда, инициативной группой нашего коллектива было принято решение о названии команды, вымпеле и комплектовании молодыми перспективными игроками!", reply_markup=menu_keyboard)  


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[В состав *ФК Феникс* входит 18 человек.С каждым сезоном популярность команды растет, и становиться частью молодой и перспективной команды желает все большее количество спортсменов.Поэтому,численность и масштаб команды прогрессируют достаточно быстро, не смотря на то, что клуб существует всего 3 года!Более подробную информацию об игроках *ФК Феникс* Вы можете наблюдать в нашем сообществе вконтакте](https://vk.com/club210591959)", reply_markup=menu_keyboard) 


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "1.*ФК Феникс* победитель чемпионата и первенства Вязниковского района по мини-футболу среди мужских команд 3-ей лиги сезона 2019-2020. 2.*ФК Феникс* бронзовый призёр чемпионата и первенства Вязниковского района по мини-футболу среди мужских команд 2-ой лиги сезона 2021-2022. 3.*ФК Феникс* серебрянный призёр Первенства по мини-футболу среди команд Главного управления МЧС России по Владимирской области 2022 года. 4.*ФК Феникс* серебрянный призёр турнира по мини-футболу Возрождение в поселке Никологоры в 2022 году. 5.*ФК Феникс* серебрянный призёр Первенства по мини-футболу среди команд Главного управления МЧС России по Владимирской области 2023 года.  Вот такие немаленькие достижения совсем молодой команды! В ноябре 2023 года *ФК Феникс* ожидает новый вызов, а именно участие в кубке Вязниковского района по мини-футболу среди мужских команд! Болейте за нашу дружную команду, мы очень ценим вашу поддержку!", reply_markup=menu_keyboard)  


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()