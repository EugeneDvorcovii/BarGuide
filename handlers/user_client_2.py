from aiogram import types
from initial import bot, dp
import keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient


data_client = DataClient()
data_client.set_place_category("Bar", "Some interesting place.")
data_client.set_place_category("Club", "Some interesting place.")
for nn in range(5):
    data_client.set_place(category_id=nn%2,
                          title=f"Title: {nn}",
                          description=f"Description: {nn}",
                          address=f"Москва, Страстной бульвар, 4",
                          rating=5.0,)

print(data_client.get_all_data("place"))

# category_id = data_client.get_one_from_one_if("place_category", "id", "title", "Club")


class FSMUserWay(StatesGroup):
    main_menu = State()

    watch_place_categories = State()
    watch_places = State()
    choice_place = State()
    watch_reviews = State()
    watch_menu = State()
    set_review = State()
    set_reserve = State()

    set_place_title = State()

    set_location = State()

    watch_announce_categories = State()
    watch_announces = State()


class UserClient:
    async def go_to_main_menu(self, msg: types.Message) -> None:
        await msg.reply("Вы в главном меню.", reply_markup=keyboards.create_start_btn())
        await FSMUserWay.main_menu.set()

    async def start_work(self, msg: types.Message) -> None:
        await msg.reply("Привет!", reply_markup=keyboards.create_start_btn())
        await FSMUserWay.main_menu.set()

    async def watch_place_categories(self, msg: types.Message) -> None:
        categories_titles = data_client.get_one_from_one("place_category", "title")
        categories_btn = keyboards.create_keyboards(categories_titles, True)
        await msg.reply("Выберите, какого типа Вас интересует заведение:", reply_markup=categories_btn)
        await FSMUserWay.watch_place_categories.set()

    async def watch_places(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            category_id = data_client.get_one_from_one_if("place_category", "id", "title", msg.text)[0]
            data["category"] = msg.text
            data["category_id"] = category_id
        places_titles = data_client.get_one_from_one_if("place", "title", "category_id",
                                                        f"{category_id}", value_type="int")
        places_btn = keyboards.create_keyboards(places_titles, True)
        await msg.reply("Выберите заведение:", reply_markup=places_btn)

        await FSMUserWay.watch_places.set()

    async def watch_one_place(self, msg: types.Message) -> None:
        places_titles = data_client.get_places_titles()
        if msg.text in places_titles:
            place_data = data_client.get_place_data(msg.text)
            back_msg = f"{place_data['title']}\n{place_data['description']}\n\n" \
                       f"Address: {place_data['address']}\nRating: {place_data['rating']}\n" \
                       f"Position: {place_data['position']}"
            functions = ["Открыть меню", "Смотреть отзывы", "Оставить отзыв", "Забронировать"]
            function_btn = keyboards.create_keyboards(functions, True)
            await msg.reply(back_msg, reply_markup=function_btn)

            await FSMUserWay.choice_place.set()
        else:
            await msg.answer("Такого заведения не найдено.")

    async def input_place_title(self, msg: types.Message) -> None:
        await msg.answer("Введите название заведения, которое Вас интересует.")

        await FSMUserWay.set_place_title.set()

    async def input_location(self, msg: types.Message) -> None:
        place_btn = ReplyKeyboardMarkup(resize_keyboard=True)
        place_btn.add(KeyboardButton('Поделиться местоположением', request_location=True))
        await msg.answer("Отправьте свое местоположение, тогда мы найдем ближайшие к Вам заведения.",
                         reply_markup=place_btn)
        await FSMUserWay.set_location.set()

    async def watch_near_places(self, msg: types.Message) -> None:
        user_lat = msg.location.latitude
        user_long = msg.location.longitude
        places_titles = data_client.get_near_position_place(f"{user_lat}_{user_long}")
        places_btn = keyboards.create_keyboards(places_titles, True)
        await msg.reply("Выберите заведение:", reply_markup=places_btn)

        await FSMUserWay.watch_places.set()

    async def watch_announces(self, msg: types.Message) -> None:
        await msg.answer("Этот функционал будет позже.")

    async def watch_project_info(self, msg: types.Message) -> None:
        await msg.answer("Скоро напишу про нас.")

    async def get_reviews(self, msg: types.Message) -> None:
        await msg.answer("Этот функционал будет позже.")

    async def set_review(self, msg: types.Message) -> None:
        await msg.answer("Этот функционал будет позже.")

    async def watch_menu(self, msg: types.Message) -> None:
        await msg.answer("Этот функционал будет позже.")

    async def set_reserve(self, msg: types.Message) -> None:
        await msg.answer("Этот функционал будет позже.")

    async def func_3(self, msg: types.Message) -> None:
        await bot.send_message(msg.from_user.id, msg.text+"dsfa")

    def run_handle(self) -> None:
        dp.register_message_handler(self.start_work, commands=['start'],
                                    state="*")
        dp.register_message_handler(self.go_to_main_menu, Text(equals="Отмена", ignore_case=True),
                                    state="*")
        dp.register_message_handler(self.watch_place_categories,
                                    Text(equals="Смотреть заведения", ignore_case=True),
                                    state=FSMUserWay.main_menu)
        dp.register_message_handler(self.input_place_title,
                                    Text(equals="Найти заведение", ignore_case=True),
                                    state=FSMUserWay.main_menu)
        dp.register_message_handler(self.input_location,
                                    Text(equals="Заведения рядом", ignore_case=True),
                                    state=FSMUserWay.main_menu)
        dp.register_message_handler(self.watch_near_places,
                                    content_types=["location"],
                                    state=FSMUserWay.set_location)
        dp.register_message_handler(self.watch_announces,
                                    Text(equals="Смотреть анонсы", ignore_case=True),
                                    state=FSMUserWay.main_menu)
        dp.register_message_handler(self.watch_project_info,
                                    Text(equals="О проекте", ignore_case=True),
                                    state=FSMUserWay.main_menu)
        dp.register_message_handler(self.watch_places,
                                    state=FSMUserWay.watch_place_categories)
        dp.register_message_handler(self.watch_one_place,
                                    state=[FSMUserWay.watch_places,
                                           FSMUserWay.set_place_title])
        dp.register_message_handler(self.watch_menu,
                                    Text(equals="Открыть меню", ignore_case=True),
                                    state=FSMUserWay.choice_place)
        dp.register_message_handler(self.get_reviews,
                                    Text(equals="Смотреть отзывы", ignore_case=True),
                                    state=FSMUserWay.choice_place)
        dp.register_message_handler(self.set_review,
                                    Text(equals="Оставить отзыв", ignore_case=True),
                                    state=FSMUserWay.choice_place)
        dp.register_message_handler(self.set_reserve,
                                    Text(equals="Забронировать", ignore_case=True),
                                    state=FSMUserWay.choice_place)
        dp.register_message_handler(self.func_3)
