from aiogram.dispatcher.filters.state import StatesGroup, State


MAIN_TOKEN = "MAIN_TOKEN"

host = "host"
user = "user"
password = "password"


class FSMWorkProgram(StatesGroup):
    # Status for main menu
    main_menu = State()

    # 1-st variation work - get all places for category
    get_place_category = State()

    # 2-nd variation work - find place for it`s title
    set_title_place = State()

    # 3-rd variation work - find place for location
    set_self_location = State()

    # 4-st variation work - get all announces for category
    get_announce_category = State()
    get_announce = State()

    # Base states 1. For work with places info
    get_place = State()
    choice_place = State()
    # get_reviews = State()
    get_menu = State()
    get_meal = State()
    get_announces = State()
    set_review = State()
    set_review_rating = State()
    set_review_text = State()
    save_new_review = State()
    set_name_reservist = State()
    set_phone_reservist = State()
    set_date_reserve = State()
    set_time_reserve = State()
    set_count_visitors = State()
    save_reserve = State()
    save_new_reserve = State()


