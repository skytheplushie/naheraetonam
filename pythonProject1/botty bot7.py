from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
import asyncio

initiate_db()


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State('1000')


menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                     KeyboardButton(text='Купить'),
                                      KeyboardButton(text='Регистрация'),
                                      KeyboardButton(text='Что я умею?')]],
                           resize_keyboard=True)

inline_choices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
        ]
    ]
)

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Product1', callback_data='product1_buying'),
            InlineKeyboardButton('Product2', callback_data='product2_buying'),
            InlineKeyboardButton('Product3', callback_data='product3_buying'),
            InlineKeyboardButton('Product4', callback_data='product4_buying'),
            InlineKeyboardButton('Product5', callback_data='product5_buying'),
            InlineKeyboardButton('Product6', callback_data='product6_buying')
        ]
    ]
)


@dp.message_handler(text='Что я умею?')
async def tell_about_itself(message):
    await message.answer('Я могу подсчитать вашу норму калорий в день! Для этого нажмите на инлайн-кнопку'
                         '"Рассчитать"! Если хотите купить какой-нибудь товар, то нажмите на инлайн-кнопку "Купить".'
                         'Если хотите зарегистрироваться как постоянный клиент, '
                         'то нажмите на инлайн-кнопку "Регистрация". '
                         'Это пока что всё что я могу! Надеюсь вам понравится общение со мной!')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for index, product in enumerate(get_all_products()):
        await message.answer(f"Название:{product[1]} | Описание:{product[2]} | Цена: {product[3]}")
        with open(f'images/image{index + 1}.jpg', 'rb') as photo:
            await message.answer_photo(photo)


@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Как мне вас называть?')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите вашу електронную почту, пожалуйста! На неё будут приходить уведомления '
                             'о прогрессе доставки вашего заказа!')
        await RegistrationState.email.set()
    else:
        await message.answer('Имя, похоже, у кого-то у же есть. Можете ли вы его слегка изменить?')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Пожалуйста, скажите мне ваш возраст! '
                         'Это последнее о чём мне надо знать перед окончанием регистрации!')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    if 120 >= int(message.text) >= 0:
        await state.update_data(age=message.text)
        data = await state.get_data()
        add_user(data['username'], data['email'], data['age'])
        await message.answer('Регистрация успешно завершена! Спасибо, что используете нашу продукцию!')
    else:
        await message.answer('Возраст не совсем верный... Возможно вы переборщили с нулями?')
        await RegistrationState.age.set()


@dp.callback_query_handler(lambda call: call.data.endswith('_buying'))
async def send_confirm_message(call):
    product_name = call.data.split('_')[0]
    await call.message.answer(f'Вы успешно приобрели {product_name}! Спасибо за покупку!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию для дальнейшей работы:', reply_markup=inline_choices)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('Расчётная формула, которой я пользуюсь: '
                              '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; '
                              'Возможно, вам она поможет рассчитать для себя или для ваших близких!')


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Для расчёта калорий мне нужны три величины: возраст, рост и вес. "
                              "Для начала, скажите свой возраст, пожалуйста!")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Теперь назовите свой рост!")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("И на последок, назовите свой вес!")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {result} в день! Пожалуйста, соблюдайте её, чтобы быть здоровым(ой)!')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Здравствуйте! Я бот помогающий вашему здоровью. Надеюсь, вам понравится общаться со мной!',
                         reply_markup=menu)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
