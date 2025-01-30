from datetime import datetime
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from pyshorteners import Shortener
from splatoonschedules import get_regular_schedules, get_spontaneous_schedules, get_unidentified_schedules, festival_schedules

bot = AsyncTeleBot("7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA")
commands_for_open_menu = ["/start", "/menu"]

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

changeMode1 = types.KeyboardButton("ℹ️ Бой салаг")
changeMode2 = types.KeyboardButton("ℹ️ Стихийный бой (Открытый)")
changeMode3 = types.KeyboardButton("ℹ️ Стихийный бой (Серия)")
changeMode4 = types.KeyboardButton("ℹ️ Бой X")
changeMode5 = types.KeyboardButton("ℹ️ Сплатфест")
changeMode6 = types.KeyboardButton("⚙️ Помощь")

main_menu.add(changeMode6) \
          .row(changeMode5) \
          .row(changeMode1, changeMode4) \
          .row(changeMode2, changeMode3)


sub_menu_regular = types.ReplyKeyboardMarkup()
now_rotation_regular = types.KeyboardButton("📋 Ротация сейчас (Бой салаг)")
all_list_regular = types.KeyboardButton("🕑 Полное рассписание (Бой салаг)")
back_to_main_menu_from_sub_regular = types.KeyboardButton("⏪ Назад (Из боя салаг)")
sub_menu_regular.row(now_rotation_regular, all_list_regular).add(back_to_main_menu_from_sub_regular)

sub_menu_spontaneous_open = types.ReplyKeyboardMarkup()
now_rotation_spontaneous_open = types.KeyboardButton("📋 Ротация сейчас (Стихийный, открытый)")
all_list_spontaneous_open = types.KeyboardButton("🕑 Полное рассписание (Стихийный, открытый)")
back_to_main_menu_from_sub_spontaneous_open = types.KeyboardButton("⏪ Назад (Из Cтихийный, открытый)")
sub_menu_spontaneous_open.row(now_rotation_spontaneous_open, all_list_spontaneous_open).add(
    back_to_main_menu_from_sub_spontaneous_open)

sub_menu_spontaneous_serial = types.ReplyKeyboardMarkup()
now_rotation_spontaneous_serial = types.KeyboardButton("📋 Ротация сейчас (Стихийный, серия)")
all_list_spontaneous_serial = types.KeyboardButton("🕑 Полное рассписание (Стихийный, серия)")
back_to_main_menu_from_sub_spontaneous_serial = types.KeyboardButton("⏪ Назад (Из Cтихийный, серия)")
sub_menu_spontaneous_serial.row(now_rotation_spontaneous_serial, all_list_spontaneous_serial).add(
    back_to_main_menu_from_sub_spontaneous_serial)

sub_menu_unidentified = types.ReplyKeyboardMarkup()
now_rotation_unidentified = types.KeyboardButton("📋 Ротация сейчас (Бой X)")
all_list_unidentified = types.KeyboardButton("🕑 Полное рассписание (Бой X)")
back_to_main_menu_from_sub_unidentified = types.KeyboardButton("⏪ Назад (Из боя X)")
sub_menu_unidentified.row(now_rotation_unidentified, all_list_unidentified).add(back_to_main_menu_from_sub_unidentified)

print("Working...")


@bot.message_handler(commands=["start", "menu"])
async def command_interpretation(msg):
    global commands_for_open_menu, main_menu
    if str(msg.chat.id) not in [1]:
        if msg.text in commands_for_open_menu:
            welcome_msg = f"Приветсвую, {msg.from_user.first_name} {msg.from_user.last_name}, на тестирование бота! "
            await bot.send_message(msg.chat.id, welcome_msg)
            await bot.send_message(msg.chat.id, "Выберите вариант: ", reply_markup=main_menu)
        # elif msg.text == "/help":
        #     help_text = "По всем вопросом с ботом, можете обращаться к @OtrashkevichEM или же @tanuki_fire"
        #     await bot.send_message(msg.chat.id, help_text)
    else:
        await bot.send_message(msg.chat.id, "Вы в бане")


@bot.message_handler(commands=["help"])
async def help_command(msg):
    help_text = ("Если у вас есть вопросы по работоспособности \nбота, то можете обратиться сюда.\n"
                 "Контакты:\n"
                 "- @OtrashkevichEM (горе разраб)\n"
                 "- @tanuki_fire (кто придумал)\n"
                 "- Все данные беруться с https://splatoon3.ink")
    await bot.send_message(msg.chat.id, help_text)


@bot.message_handler(commands=["cat"])
async def send_gif_with_cat(msg):
    await bot.send_animation(msg.chat.id, "https://media1.tenor.com/m/4_Lj9Mh4mPQAAAAC/hooray-yay.gif")


@bot.message_handler(content_types=["text"])
async def sub_menu(msg):
    global time_range_A, time_range_B
    if msg.text == "ℹ️ Бой салаг":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=sub_menu_regular)
    elif msg.text == "📋 Ротация сейчас (Бой салаг)":
        regular_schedules1 = get_regular_schedules().all()[0]
        regular_schedules2 = get_regular_schedules().all()[1]
        map_name = regular_schedules1["MapName"]
        game_mode = regular_schedules1["GameMode"]
        map_photo = regular_schedules1["MapPhoto"]
        map_name1 = regular_schedules2["MapName"]
        game_mode1 = regular_schedules2["GameMode"]
        map_photo1 = regular_schedules2["MapPhoto"]
        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")
        markdown_text1 = (f"***Имя карты***: {map_name}\n"
                          f"***Режим***: {game_mode}\n"
                          f"[Картинка]({map_photo})\n")
        markdown_text2 = (f"***Имя карты***: {map_name1}\n"
                          f"***Режим***: {game_mode1}\n"
                          f"[Картинка]({map_photo1})")
        await bot.send_message(msg.chat.id, markdown_text1, parse_mode='Markdown')
        await bot.send_message(msg.chat.id, markdown_text2, parse_mode='Markdown')
    elif msg.text == "⏪ Назад (Из боя салаг)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=main_menu)
    elif msg.text == "🕑 Полное рассписание (Бой салаг)":
        ull_schedules = ""
        switch_time_range = 0

        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")

        current_hour = datetime.now().hour
        time_ranges = [
            (9, 11),
            (11, 13),
            (13, 15),
            (15, 17),
            (17, 19),
            (19, 21),
            (21, 23),
            (23, 1),
            (1, 3),
            (3, 5),
            (5, 7),
            (7, 9)
        ]

        for time_range_A, time_range_B in time_ranges:
            if time_range_A <= current_hour < (time_range_B if time_range_B != 1 else 24):
                break

        schedules_on_day_regular = get_regular_schedules().all()
        full_schedules = f"[Картинка меню выбора]({temp_menu_photo})\n"

        if schedules_on_day_regular:
            for schedule in schedules_on_day_regular:
                if switch_time_range == 2:
                    time_range_A += 2
                    time_range_B += 2

                    if time_range_A >= 24:
                        time_range_A -= 24
                    if time_range_B >= 24:
                        time_range_B -= 24

                    switch_time_range = 0

                full_schedules += (f"***Имя карты***: {schedule["MapName"]}\n"
                                   f"***Режим***: {schedule["GameMode"]}\n"
                                   f"***Время***: {time_range_A}:00 - {time_range_B}:00 по МСК\n"
                                   f"===============================\n\n")
                switch_time_range += 1

            await bot.send_message(msg.chat.id, full_schedules, reply_markup=main_menu, parse_mode='Markdown')
        else:
            await bot.send_message(msg.chat.id, "Нет доступных расписаний.", reply_markup=main_menu)

    # ----------------------------------------------------------------------------------

    if msg.text == "ℹ️ Стихийный бой (Открытый)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=sub_menu_spontaneous_open)
    elif msg.text == "📋 Ротация сейчас (Стихийный, открытый)":
        spontaneous_schedules = get_spontaneous_schedules()[1]
        map_name = spontaneous_schedules[0]["MapName"]
        game_mode = spontaneous_schedules[0]["GameMode"]
        map_photo = spontaneous_schedules[0]["Photo"]["url"]
        map_name1 = spontaneous_schedules[1]["MapName"]
        game_mode1 = spontaneous_schedules[1]["GameMode"]
        map_photo1 = spontaneous_schedules[1]["Photo"]["url"]
        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6"
            "-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")
        markdown_text1 = (f"***Имя карты***: {map_name}\n"
                          f"***Режим***: {game_mode}\n"
                          f"[Картинка]({map_photo})\n")
        markdown_text2 = (f"***Имя карты***: {map_name1}\n"
                          f"***Режим***: {game_mode1}\n"
                          f"[Картинка]({map_photo1})")
        await bot.send_message(msg.chat.id, markdown_text1, parse_mode='Markdown')
        await bot.send_message(msg.chat.id, markdown_text2, parse_mode='Markdown')
    elif msg.text == "⏪ Назад (Из Cтихийный, открытый)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=main_menu)
    elif msg.text == "🕑 Полное рассписание (Стихийный, открытый)":
        full_schedules = ""
        switch_time_range = 0

        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")

        current_hour = datetime.now().hour
        time_ranges = [
            (9, 11),
            (11, 13),
            (13, 15),
            (15, 17),
            (17, 19),
            (19, 21),
            (21, 23),
            (23, 1),
            (1, 3),
            (3, 5),
            (5, 7),
            (7, 9)
        ]

        for time_range_A, time_range_B in time_ranges:
            if time_range_A <= current_hour < (time_range_B if time_range_B != 1 else 24):
                break

        schedules_on_day_regular = get_spontaneous_schedules()[1].all()
        full_schedules = f"[Картинка меню выбора]({temp_menu_photo})\n"

        if schedules_on_day_regular:
            for schedule in schedules_on_day_regular:
                if switch_time_range == 2:
                    time_range_A += 2
                    time_range_B += 2

                    if time_range_A >= 24:
                        time_range_A -= 24
                    if time_range_B >= 24:
                        time_range_B -= 24

                    switch_time_range = 0

                full_schedules += (f"***Имя карты***: {schedule["MapName"]}\n"
                                   f"***Режим***: {schedule["GameMode"]}\n"
                                   f"***Время***: {time_range_A}:00 - {time_range_B}:00 по МСК\n"
                                   f"===============================\n\n")
                switch_time_range += 1

            await bot.send_message(msg.chat.id, full_schedules, reply_markup=main_menu, parse_mode='Markdown')
        else:
            await bot.send_message(msg.chat.id, "Нет доступных расписаний.", reply_markup=main_menu)

    # ----------------------------------------------------------------------------------

    if msg.text == "ℹ️ Стихийный бой (Серия)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=sub_menu_spontaneous_serial)
    elif msg.text == "📋 Ротация сейчас (Стихийный, серия)":
        spontaneous_schedules1 = get_spontaneous_schedules()[0]
        map_name = spontaneous_schedules1[0]["MapName"]
        game_mode = spontaneous_schedules1[0]["GameMode"]
        map_photo = spontaneous_schedules1[0]["Photo"]["url"]
        map_name1 = spontaneous_schedules1[1]["MapName"]
        game_mode1 = spontaneous_schedules1[1]["GameMode"]
        map_photo1 = spontaneous_schedules1[1]["Photo"]["url"]
        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")
        markdown_text1 = (f"***Имя карты***: {map_name}\n"
                          f"***Режим***: {game_mode}\n"
                          f"[Картинка]({map_photo})\n")
        markdown_text2 = (f"***Имя карты***: {map_name1}\n"
                          f"***Режим***: {game_mode1}\n"
                          f"[Картинка]({map_photo1})")
        await bot.send_message(msg.chat.id, markdown_text1, parse_mode='Markdown')
        await bot.send_message(msg.chat.id, markdown_text2, parse_mode='Markdown')
    elif msg.text == "⏪ Назад (Из Cтихийный, серия)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=main_menu)
    elif msg.text == "🕑 Полное рассписание (Стихийный, серия)":
        full_schedules = ""
        switch_time_range = 0

        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")

        current_hour = datetime.now().hour
        time_ranges = [
            (9, 11),
            (11, 13),
            (13, 15),
            (15, 17),
            (17, 19),
            (19, 21),
            (21, 23),
            (23, 1),
            (1, 3),
            (3, 5),
            (5, 7),
            (7, 9)
        ]

        for time_range_A, time_range_B in time_ranges:
            if time_range_A <= current_hour < (time_range_B if time_range_B != 1 else 24):
                break

        schedules_on_day_regular = get_spontaneous_schedules()[0].all()
        full_schedules = f"[Картинка меню выбора]({temp_menu_photo})\n"

        if schedules_on_day_regular:
            for schedule in schedules_on_day_regular:
                if switch_time_range == 2:
                    time_range_A += 2
                    time_range_B += 2

                    if time_range_A >= 24:
                        time_range_A -= 24
                    if time_range_B >= 24:
                        time_range_B -= 24

                    switch_time_range = 0

                full_schedules += (f"***Имя карты***: {schedule["MapName"]}\n"
                                   f"***Режим***: {schedule["GameMode"]}\n"
                                   f"***Время***: {time_range_A}:00 - {time_range_B}:00 по МСК\n"
                                   f"===============================\n\n")
                switch_time_range += 1

            await bot.send_message(msg.chat.id, full_schedules, reply_markup=main_menu, parse_mode='Markdown')
        else:
            await bot.send_message(msg.chat.id, "Нет доступных расписаний.", reply_markup=main_menu)

    # -----------------------------------------------------------------------------------

    if msg.text == "ℹ️ Бой X":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=sub_menu_unidentified)
    elif msg.text == "📋 Ротация сейчас (Бой X)":
        unidentified_schedules = get_unidentified_schedules()
        map_name = unidentified_schedules[0]["MapName"]
        game_mode = unidentified_schedules[0]["GameMode"]
        map_photo = unidentified_schedules[0]["Photo"]["url"]
        map_name1 = unidentified_schedules[1]["MapName"]
        game_mode1 = unidentified_schedules[1]["GameMode"]
        map_photo1 = unidentified_schedules[1]["Photo"]["url"]
        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")
        markdown_text1 = (f"***Имя карты***: {map_name}\n"
                          f"***Режим***: {game_mode}\n"
                          f"[Картинка]({map_photo})\n")
        markdown_text2 = (f"***Имя карты***: {map_name1}\n"
                          f"***Режим***: {game_mode1}\n"
                          f"[Картинка]({map_photo1})")
        await bot.send_message(msg.chat.id, markdown_text1, parse_mode='Markdown')
        await bot.send_message(msg.chat.id, markdown_text2, parse_mode='Markdown')
    elif msg.text == "⏪ Назад (Из боя X)":
        await bot.send_message(msg.chat.id, "Выберите вариант:", reply_markup=main_menu)
    elif msg.text == "🕑 Полное рассписание (Бой X)":

        full_schedules = ""
        switch_time_range = 0

        temp_menu_photo = Shortener().clckru.short(
            "https://fotografias-neox.atresmedia.com/clipping/cmsimages02/2017/04/26/0BAF7E93-3FC3-4678-B8E6-BF21ED2C2016/69.jpg?crop=889,500,x1,y0&width=1280&height=720&optimize=low")

        current_hour = datetime.now().hour
        time_ranges = [
            (9, 11),
            (11, 13),
            (13, 15),
            (15, 17),
            (17, 19),
            (19, 21),
            (21, 23),
            (23, 1),
            (1, 3),
            (3, 5),
            (5, 7),
            (7, 9)
        ]

        for time_range_A, time_range_B in time_ranges:
            if time_range_A <= current_hour < (time_range_B if time_range_B != 1 else 24):
                break

        schedules_on_day_regular = get_unidentified_schedules().all()
        full_schedules = f"[Картинка меню выбора]({temp_menu_photo})\n"

        if schedules_on_day_regular:
            for schedule in schedules_on_day_regular:
                if switch_time_range == 2:
                    time_range_A += 2
                    time_range_B += 2

                    if time_range_A >= 24:
                        time_range_A -= 24
                    if time_range_B >= 24:
                        time_range_B -= 24

                    switch_time_range = 0

                full_schedules += (f"***Имя карты***: {schedule["MapName"]}\n"
                                   f"***Режим***: {schedule["GameMode"]}\n"
                                   f"***Время***: {time_range_A}:00 - {time_range_B}:00 по МСК\n"
                                   f"===============================\n\n")
                switch_time_range += 1

            await bot.send_message(msg.chat.id, full_schedules, reply_markup=main_menu, parse_mode='Markdown')
        else:
            await bot.send_message(msg.chat.id, "Нет доступных расписаний.", reply_markup=main_menu)

    # -----------------------------------------------------------------------------------

    if msg.text == "ℹ️ Сплатфест":
        fest_date = festival_schedules()

        fest_text = (f"**Вопрос:**\n"
                     f"{fest_date["Title"]}\n\n"
                     f"**Команды:**\n"
                     f"1.{fest_date["Teams"][0]}\n"
                     f"2.{fest_date["Teams"][1]}\n"
                     f"3.{fest_date["Teams"][2]}\n\n"
                     f"[Картинка]({fest_date["Photo"]})")

        await bot.send_message(msg.chat.id, fest_text, parse_mode='Markdown')

    # ----------------------------------------------------------------------------------

    if msg.text == "⚙️ Помощь":
        help_text = ("Если у вас есть вопросы по работоспособности \nбота, то можете обратиться сюда.\n"
                     "Контакты:\n"
                     "- @OtrashkevichEM (горе разраб)\n"
                     "- @tanuki_fire (кто придумал)")
        await bot.send_message(msg.chat.id, help_text, reply_markup=main_menu)


async def main():
    await asyncio.gather(bot.polling())


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Shutdown... ")
