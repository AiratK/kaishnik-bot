# Official emoji list of the Unicode Consortium: http://unicode.org/emoji/charts/full-emoji-list.html
emoji = {
    "smirking":    "\U0001F60F", # 😏
    "upside-down": "\U0001F643", # 🙃
    "kissing":     "\U0001F61A", # 😚
    "crying":      "\U0001F622", # 😢
    "no-woman":    "\U0001F645"  # 🙅‍♀️
}

# Replies to unknow stuff
replies_to_unknown_command = [
    "Список команд можно увидеть, введя * / * (но не отправляя!).",
    "Введи * / *, но не отправляй, и ты увидишь поддерживаемые команды. А твою я не знаю" + emoji["no-woman"],
    "Я понимаю лишь несколько команд. Они доступны после ввода * / * (не отправлять, только ввести).",
    "_\"Не любая команда - команда\"_ - [Создатель](https://telegram.me/airatk)."
]

replies_to_unknown_message = [
    "Не понимаю!",
    "Не делай так, я отвечаю лишь на определённые команды.",
    "Если ты думаешь, что это весело - писать мне непонятные сообщения, то нет.",
    "Ўт тЅЁЅ! тЎЁы Ј тЅЁЅ ЁыЋЎ ­ЅЏЎ­ят­Ў!",
    "А может, ты лучше команду введёшь?",
    "О, ты, как моя девушка! Я тебя тоже не понял.",
    "Я не умею отвечать на естественные сообщения - я же всего лишь глупый алгоритм, а не ИИ.",
    emoji["upside-down"],
    "Есть вещи, которые я понимаю (кстати, они начинаются с * / *), а есть вещи, которых я не понимаю. Вторых, конечно же, больше." + emoji["crying"],
    "К чёрту всё! Я люблю тебя!" + emoji["kissing"],
    "Нет, это не по мне... По мне - это простые запросы, которые начинаются с * / *.",
    "Целовались студееенты, распускались тюльпаааны, чикчирикало там и тут... Ой, ты ещё здесь?"
]

# Locations
buildings = {
    "first":   { "latitude": 55.7971077, "longitude": 49.1129913 },
    "second":  { "latitude": 55.8226860, "longitude": 49.1360610 },
    "third":   { "latitude": 55.7918200, "longitude": 49.1374140 },
    "fourth":  { "latitude": 55.7931629, "longitude": 49.1374294 },
    "fifth":   { "latitude": 55.7969110, "longitude": 49.1237459 },
    "sixth":   { "latitude": 55.8542530, "longitude": 49.0980440 },
    "seventh": { "latitude": 55.7971410, "longitude": 49.1345289 },
    "eighth":  { "latitude": 55.8208035, "longitude": 49.1363205 },
    "olymp":   { "latitude": 55.8201111, "longitude": 49.1398743 }
}

dorms = {
    "first":   { "latitude": 55.7984276, "longitude": 49.1154430 },
    "second":  { "latitude": 55.7978831, "longitude": 49.1147940 },
    "third":   { "latitude": 55.8095929, "longitude": 49.1998827 },
    "fourth":  { "latitude": 55.8379590, "longitude": 49.1009150 },
    "fifth":   { "latitude": 55.7927011, "longitude": 49.1644210 },
    "sixth":   { "latitude": 55.7851918, "longitude": 49.1559488 },
    "seventh": { "latitude": 55.7853090, "longitude": 49.1549720 }
}
