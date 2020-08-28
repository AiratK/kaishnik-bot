from bot import keys


CREATOR: int = int(keys.CREATOR)

CONTROL_PANEL: str = (
    "*Control panel*\n"
    "_creator access only_\n"
    "\n"
    "_{} - required, [] - optional_\n"
    "\n"
    "*stats*\n"
    "/users\n"
    "/metrics \[ drop ]\n"
    "/data {\n"
        "\t\t\t\[ ids: {\n"
            "\t\t\t\t\t\t\[ id&… ]\n"
            "\t\t\t\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
            "\t\t\t\t\t\t\[ extended ]\[ compact ]\n"
            "\t\t\t\t\t\t\[ group-chat ]\n"
        "\t\t\t} ]\n"
        "\t\t\t\[ username: {} ]\n"
        "\t\t\t\[ firstname: {} ]\n"
        "\t\t\t\[ number: {} ]\n"
        "\t\t\t\[ index: {} ]\n"
        "\t\t\t\[ name: {} ]\n"
        "\t\t\t\[ group: {} ]\n"
        "\t\t\t\[ year: {} ]\n"
    "}\n"
    "\n"
    "*cleaning*\n"
    "/clear\n"
    "/erase { ids: {\n"
        "\t\t\t\[ id&… ]\n"
        "\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
        "\t\t\t\[ extended ]\[ compact ]\n"
        "\t\t\t\[ group-chat ]\n"
    "} }\n"
    "/drop {\n"
        "\t\t\t\[ silently ]\n"
        "\t\t\t{ ids: {\n"
            "\t\t\t\t\t\t\[ id&… ]\n"
            "\t\t\t\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
            "\t\t\t\t\t\t\[ extended ]\[ compact ]\n"
            "\t\t\t\t\t\t\[ group-chat ]\n"
        "\t\t\t} }\n"
        "\t\t\t\[ message: {} ]\n"
    "}\n"
    "/guarddrop { ids: {\n"
        "\t\t\t\[ id&… ]\n"
        "\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
        "\t\t\t\[ extended ]\[ compact ]\n"
        "\t\t\t\[ group-chat ]\n"
    "} }\n"
    "\n"
    "*others*\n"
    "/broadcast {\n"
        "\t\t\t{ ids: {\n"
            "\t\t\t\t\t\t\[ id&… ]\n"
            "\t\t\t\t\t\t\[ all ]\[ unlogin ]\[ me ]\n"
            "\t\t\t\t\t\t\[ extended ]\[ compact ]\n"
            "\t\t\t\t\t\t\[ group-chat ]\n"
        "\t\t\t} }\n"
        "\t\t\t\[ signed: false ]\n"
        "\t\t\t\[ notify: false ]\n"
        "\t\t\t{ message: {} }\n"
    "}\n"
    "/dayoff {\n"
        "\t\t\t\[ list ]\n"
        "\t\t\t\[ add: { day-month } ]\n"
        "\t\t\t\[ message: {} ]\n"
        "\t\t\t\[ drop: {\n"
            "\t\t\t\t\t\t\[ day-month ]\n"
            "\t\t\t\t\t\t\[ all ]\n"
        "\t\t\t} ]\n"
    "}\n"
    "/backup\n"
    "\n"
    "*hashtags*\n"
    "# users\n"
    "# metrics\n"
    "# data\n"
    "# erased\n"
    "# broadcast\n"
    "# dropped\n"
    "# guarddropped"
)

USERS_STATS: str = (
    "*Users*\n"
    "_stats of #users_\n"
    "\n"
    "*institutes*\n"
    "• {faculty_1}: {faculty_1_number}\n"
    "• {faculty_2}: {faculty_2_number}\n"
    "• {faculty_3}: {faculty_3_number}\n"
    "• {faculty_4}: {faculty_4_number}\n"
    "• {faculty_5}: {faculty_5_number}\n"
    "• {faculty_6}: {faculty_6_number}\n"
    "\n"
    "*years*\n"
    "• {year_1}: {year_1_number}\n"
    "• {year_2}: {year_2_number}\n"
    "• {year_3}: {year_3_number}\n"
    "• {year_4}: {year_4_number}\n"
    "• {year_5}: {year_5_number}\n"
    "• {year_6}: {year_6_number}\n"
    "\n"
    "*{type_1}*: {type_1_number}\n"
    "*{type_2}*: {type_2_number}\n"
    "*{type_3}*: {type_3_number}\n"
    "\n"
    "*unsetup*: {unsetup_number}\n"
    "\n"
    "*{total}* users in total!"
)

COMMAND_REQUESTS_STATS: str = (
    "*Metrics*\n"
    "_daily #metrics_\n"
    "\n"
    "*commands*\n"
    "• /classes: {classes_request_number}\n"
    "• /score: {score_request_number}\n"
    "• /lecturers: {lecturers_request_number}\n"
    "• /notes: {notes_request_number}\n"
    "• /week: {week_request_number}\n"
    "• /exams: {exams_request_number}\n"
    "• /dice: {dice_request_number}\n"
    "• /locations: {locations_request_number}\n"
    "• /brs: {brs_request_number}\n"
    "• /edit: {edit_request_number}\n"
    "• /settings: {settings_request_number}\n"
    "• /help: {help_request_number}\n"
    "• /donate: {donate_request_number}\n"
    "\n"
    "• /cancel: {cancel_request_number}\n"
    "\n"
    "• /start: {start_request_number}\n"
    "• /login: {login_request_number}\n"
    "\n"
    "*unknown*\n"
    "• non-text: {unknown_nontext_message_request_number}\n"
    "• text: {unknown_text_message_request_number}\n"
    "• callback: {unknown_callback_request_number}\n"
    "\n"
    "*others*\n"
    "• no permissions: {no_permissions_number}\n"
    "• unlogin: {unlogin_request_number}\n"
    "\n"
    "*{total_request_number}* requests in total!"
)

USER_DATA: str = (
    "{fullname} @{username}\n"
    "chat id {chat_id}\n"
    "{type}-type\n"
    "\n"
    "• Institute: {institute}\n"
    "• Year: {year}\n"
    "• Group: {group_number}\n"
    "• Name: {name}\n"
    "• Card: {card}\n"
    "\n"
    "• Notes: {notes_number}\n"
    "• Edited subjects: {edited_classes_number}\n"
    "• Fellow students: {fellow_students_number}\n"
    "\n"
    "• Guard text: {guard_text}\n"
    "• Guard message: {guard_message}\n"
    "\n"
    "#{hashtag}"
)

BROADCAST_MESSAGE_TEMPLATE: str = (
    "*Телеграмма от разработчика*\n"
    "#broadcast\n"
    "\n"
    "{broadcast_message}\n"
    "\n"
    "Поддержать бота финансово: /donate\n"
    "Написать разработчику: @airatk"
)
