from django.core.management.base import BaseCommand
from bot_app.models import TelegramUser, UserLog
import telebot
from telebot import types

TOKEN = "8783428083:AAEck0uVydX4aUMTtTOLtP7o79g56PLGiqY"
bot = telebot.TeleBot(TOKEN)

EXERCISES_DB = {
    "treadmill": {"title": "🏃‍♂️ Беговая дорожка (РАЗМИНКА)", "reps": "15 мин"},
    "velo": {"title": "🚴‍♂️ Велотренажер (РАЗМИНКА)", "reps": "12 мин"},
    "decline_press": {
        "title": "📉 Жим головой вниз (НИЗ груди)", 
        "reps": "3х12", 
        "video": "https://youtu.be/zG3aQQior4w"
    },
    "db_fly": {
        "title": "🦋 Разводка гантелей (ФОРМА груди)", 
        "reps": "3х12", 
        "video": "https://youtu.be/fWfTbyXe7Ds"
    },
    "lat_pull_front": {
        "title": "👐 Тяга к груди (ШИРИНА спины)", 
        "reps": "4х10", 
        "video": "https://youtu.be/GTs3xqB_ZgQ"
    },
    "bent_over_row": {
        "title": "🚣‍♂️ Тяга штанги в наклоне (ТОЛЩИНА спины)", 
        "reps": "3х10", 
        "video": "https://youtu.be/D3E6BEuROfM"
    },
    "seated_row": {
        "title": "⚓️ Тяга горизонтального блока к поясу", 
        "reps": "3х12", 
        "video": "https://youtu.be/hUV6XDtNTLU"
    },
    "smith_press": {
        "title": "🛡 Жим в Смите (ПЕРЕДНИЕ дельты)", 
        "reps": "3х10", 
        "video": "https://youtu.be/wfyrf8ZfiAw"
    },
    "barbell_curl": {
        "title": "💪 Подъем штанги на бицепс", 
        "reps": "3х12", 
        "video": "https://youtu.be/tj2KdcsSsE0"
    },
    "reverse_grip_row": {
        "title": "🔄 Тяга штанги обратным хватом (НИЗ спины)", 
        "reps": "3х10", 
        "video": "https://youtu.be/xUtQU3Kcv50"
    },
    "triceps_pushdown": {
        "title": "⚡️ Жим книзу на блоке (ТРИЦЕПС)", 
        "reps": "3х12", 
        "video": "https://youtu.be/lklND7Vmy4I"
    },
    "french_press": {
        "title": "🧠 Французский жим (ТРИЦЕПС)", 
        "reps": "3х12", 
        "video": "https://youtu.be/OmJsmWQiEo4"
    },
    "leg_press": {
        "title": "🦵 Жим ногами (КВАДРИЦЕПС)", 
        "reps": "3х15", 
        "video": "https://youtu.be/LVoAjCkJNyY"
    },
    "leg_extension": {
        "title": "🦵 Разгибание ног (КВАДРИЦЕПС)", 
        "reps": "3х12", 
        "video": "https://youtu.be/1n1iyWDb7ds"
    },
    "calf_raise": {
        "title": "🦶 Подъем на носки (ИКРЫ)", 
        "reps": "3х15", 
        "video": "https://youtu.be/xslOYVtPpU8"
    },
    "hyperextension": {
        "title": "🧘‍♂️ Гиперэкстензия (СПИНА)", 
        "reps": "3х15", 
        "video": "https://youtu.be/iep-2kTrOAg"
    },
    "crunches": {
        "title": "🔥 Скручивания (ПРЕСС)", 
        "reps": "3х20", 
        "video": "https://youtu.be/H8xSHCAjM-I"
    },
    "reverse_crunches": {
        "title": "↩️ Обратные скручивания (НИЖНИЙ пресс)", 
        "reps": "3х15", 
        "video": "https://youtu.be/suAHzBGQ3g0"
    }
}

WORKOUT_PLANS = {
    "full_body": {
        "title": "Full Body (Все пучки)",
        "novice": {
            "ПОНЕДЕЛЬНИК": ["treadmill", "smith_press", "lat_pull_front", "barbell_curl", "crunches"],
            "СРЕДА": ["treadmill", "smith_press", "lat_pull_front", "triceps_pushdown", "reverse_crunches"],
            "ПЯТНИЦА": ["treadmill", "smith_press", "lat_pull_front", "barbell_curl", "hyperextension"]
        },
        "expert": {
            "ПОНЕДЕЛЬНИК": ["treadmill", "decline_press", "lat_pull_front", "barbell_curl", "triceps_pushdown", "crunches"],
            "СРЕДА": ["velo", "leg_extension", "decline_press", "seated_row", "smith_press", "french_press", "reverse_crunches"],
            "ПЯТНИЦА": ["treadmill", "db_fly", "calf_raise", "barbell_curl", "triceps_pushdown", "hyperextension"]
        }
    },
    "split": {
        "title": "Split (Детальная проработка)",
        "novice": {
            "ПН (Грудь/Спина)": ["treadmill", "lat_pull_front", "hyperextension"],
            "СР (Ноги/Плечи)": ["velo", "smith_press", "calf_raise"],
            "ПТ (Руки/Пресс)": ["treadmill", "barbell_curl", "triceps_pushdown", "crunches"]
        },
        "expert": {
            "ПН (Грудь)": ["treadmill", "decline_press", "db_fly", "crunches"],
            "СР (Спина/Ноги)": ["velo", "lat_pull_front", "seated_row", "leg_extension", "hyperextension"],
            "ПТ (Руки/Плечи)": ["treadmill", "smith_press", "barbell_curl", "triceps_pushdown", "french_press", "reverse_crunches"]
        }
    },
    "push_pull": {
        "title": "Push/Pull",
        "novice": {
            "ПН (Push)": ["treadmill", "smith_press", "triceps_pushdown"],
            "СР (Pull)": ["velo", "lat_pull_front", "barbell_curl", "hyperextension"],
            "ПТ (Legs)": ["treadmill", "calf_raise", "crunches"]
        },
        "expert": {
            "ПН (Push)": ["treadmill", "smith_press", "french_press", "triceps_pushdown", "db_fly"],
            "СР (Pull)": ["velo", "lat_pull_front", "seated_row", "barbell_curl", "hyperextension"],
            "ПТ (Legs)": ["treadmill", "leg_extension", "calf_raise", "reverse_crunches", "crunches"]
        }
    },
    "upper_lower": {
        "title": "Upper/Lower",
        "novice": {
            "ПН (Upper)": ["treadmill", "lat_pull_front", "smith_press"],
            "СР (Lower)": ["velo", "leg_extension", "crunches"],
            "ПТ (Upper)": ["treadmill", "barbell_curl", "triceps_pushdown", "hyperextension"]
        },
        "expert": {
            "ПН (Upper)": ["treadmill", "lat_pull_front", "seated_row", "barbell_curl", "triceps_pushdown"],
            "СР (Lower)": ["velo", "leg_extension", "calf_raise", "reverse_crunches", "crunches", "hyperextension"],
            "ПТ (Upper)": ["treadmill", "decline_press", "db_fly", "smith_press", "french_press"]
        }
    }
}

user_experience = {}

def show_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Мужчина 🚹", "Женщина 🚺")
    bot.send_message(message.chat.id, "Выбери пол:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user, _ = TelegramUser.objects.get_or_create(chat_id=message.chat.id)
    UserLog.objects.create(user=user, action="Запуск /start")
    show_start(message)

@bot.message_handler(func=lambda message: message.text in ["Мужчина 🚹", "Женщина 🚺"])
def get_gender(message):
    user = TelegramUser.objects.get(chat_id=message.chat.id)
    UserLog.objects.create(user=user, action=f"Выбрал пол: {message.text}")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Новичок (0-6 мес)", "Опытный (1-2 года)", "Эксперт (2+ года)")
    bot.send_message(message.chat.id, "Твой стаж тренировок:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Новичок (0-6 мес)", "Опытный (1-2 года)", "Эксперт (2+ года)"])
def get_experience(message):
    user = TelegramUser.objects.get(chat_id=message.chat.id)
    UserLog.objects.create(user=user, action=f"Выбрал стаж: {message.text}")
    
    user_experience[message.chat.id] = 'expert' if ("Эксперт" in message.text or "Опытный" in message.text) else 'novice'
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("Full Body", "Split", "Push/Pull", "Upper/Lower")
    bot.send_message(message.chat.id, "Выбери программу:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Full Body", "Split", "Push/Pull", "Upper/Lower", "🔄 Сбросить", "🔙 Назад"])
def finalize(message):
    if message.text == "🔄 Сбросить":
        return show_start(message)
    
    if message.text == "🔙 Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("Full Body", "Split", "Push/Pull", "Upper/Lower")
        return bot.send_message(message.chat.id, "Выбери программу:", reply_markup=markup)

    user = TelegramUser.objects.get(chat_id=message.chat.id)
    UserLog.objects.create(user=user, action=f"Выбрал план: {message.text}")
    
    exp = user_experience.get(message.chat.id, 'novice')
    key = message.text.lower().replace("/", "_").replace(" ", "_")
    plan = WORKOUT_PLANS.get(key)
    
    res = f"📅 ПЛАН ({exp.upper()})\n🏆 {plan['title']}\n------------------------------------\n\n"
    for day, ex_keys in plan[exp].items():
        res += f"--- {day} ---\n"
        for ex_key in ex_keys:
            ex = EXERCISES_DB.get(ex_key)
            if ex:
                if "video" in ex and ex["video"]:
                    res += f"  - [{ex['title']}]({ex['video']}) ({ex['reps']})\n"
                else:
                    res += f"  - {ex['title']} ({ex['reps']})\n"
        res += "\n"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔙 Назад", "🔄 Сбросить")
    res += "------------------------------------"
    
    bot.send_message(message.chat.id, res, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "❌ Некорректный ввод. Используй кнопки меню или /start")

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.polling(none_stop=True)