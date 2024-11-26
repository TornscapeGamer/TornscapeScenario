import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import logging
from flask import Flask, request
import threading

# Инициализация Flask
app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json  # Получаем данные POST-запроса
    # Проверяем тип события
    if data['type'] == 'confirmation':
        return '61673566'  # Строка подтверждения для ВКонтакте
    return '', 200  # Обработка других типов событий

# Настройка логирования
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Сценарии с картинками и ссылками
scenarios = [
    {"title": "Сценарий 1. Встречный Бой.", "image": "photo-228386465_456239018", "link": "https://rulebook.torn-world.com/scenario.html#anchor-13"},
    {"title": "Сценарий 2. Утерянная Реликвия.", "image": "photo-228386465_456239019", "link": "https://rulebook.torn-world.com/scenario.html#anchor-14"},
    {"title": "Сценарий 3. Спасение.", "image": "photo-228386465_456239020", "link": "https://rulebook.torn-world.com/scenario.html#anchor-15"},
    {"title": "Сценарий 4. Кровь и Пламя.", "image": "photo-228386465_456239021", "link": "https://rulebook.torn-world.com/scenario.html#anchor-16"},
    {"title": "Сценарий 5. Проклятый Артефакт.", "image": "photo-228386465_456239022", "link": "https://rulebook.torn-world.com/scenario.html#anchor-17"},
    {"title": "Сценарий 6. Жатва Отраакса.", "image": "photo-228386465_456239023", "link": "https://rulebook.torn-world.com/scenario.html#anchor-17-1"},
    {"title": "Сценарий 7. Дикая Охота.", "image": "photo-228386465_456239024", "link": "https://rulebook.torn-world.com/scenario.html#anchor-18"},
    {"title": "Сценарий 8. Камни Древних", "image": "photo-228386465_456239025", "link": "https://rulebook.torn-world.com/scenario.html#anchor-19"},
    {"title": "Сценарий 9. Исход.", "image": "photo-228386465_456239026", "link": "https://rulebook.torn-world.com/scenario.html#anchor-20"},
    {"title": "Сценарий 10. Боги слышат нас!", "image": "photo-228386465_456239027", "link": "https://rulebook.torn-world.com/scenario.html#anchor-21"},
    {"title": "Сценарий 11. В Объятия Смерти.", "image": "photo-228386465_456239028", "link": "https://rulebook.torn-world.com/scenario.html#anchor-22"},
    {"title": "Сценарий 12. Источник.", "image": "photo-228386465_456239029", "link": "https://rulebook.torn-world.com/scenario.html#anchor-23"},
    {"title": "Сценарий 13. Доминация.", "image": "photo-228386465_456239030", "link": "https://rulebook.torn-world.com/scenario.html#anchor-24"},
    {"title": "Сценарий 14. Саботаж.", "image": "photo-228386465_456239031", "link": "https://rulebook.torn-world.com/scenario.html#anchor-25"},
]

# Инициализация API ВКонтакте
TOKEN = "vk1.a.F9dozThMpAdgrHjoeAQ3fgzUobz13Wk1KfZsyXV6sYm8W26WIntRnxmZtFrGrAVO1E-VK6neoy31H7_yCNQo3LpKkMXCu036dxTMIIM2ukx6QSXQ1TURr0YF9mhizR3TL8lTO8-xDmaozYkzFu-fV6Iy26Y8U8xQjAHQabpS8dSLPNzMXT2FSh1KUCDNBDSG3EU_pWJsmmoQcQzqcq3lGg"
GROUP_ID = "228386465"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# Ключевые словосочетания
trigger_phrases = [
    "выбери миссию", "выбери сценарий", "подбери миссию", "подбери сценарий",
    "выбери нам миссию", "подбери нам миссию", "выбери нам сценарий", "подбери нам сценарий"
]

# Функция отправки сообщений
def send_message(peer_id, text, attachment=None):
    try:
        vk.messages.send(
            peer_id=peer_id,
            message=text,
            random_id=random.randint(0, 2**31),
            attachment=attachment
        )
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")

# Главная логика бота
def main():
    logging.info("Бот запущен!")
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                try:
                    message = event.object.message["text"].lower()
                    peer_id = event.object.message["peer_id"]
                    logging.info(f"Получено сообщение: {message}")

                    if any(phrase in message for phrase in trigger_phrases):
                        scenario = random.choice(scenarios)
                        logging.info(f"Выбран сценарий: {scenario['title']}")

                        send_message(
                            peer_id=peer_id,
                            text=f"Выбран сценарий: {scenario['title']}\nПодробнее: {scenario['link']}",
                            attachment=f"photo{scenario['image']}"
                        )
                except KeyError as e:
                    logging.error(f"Ошибка обработки события: {e}")
                except Exception as e:
                    logging.error(f"Неизвестная ошибка при обработке события: {e}")
    except Exception as e:
        logging.critical(f"Критическая ошибка в работе бота: {e}")

# Запуск Flask-сервера в отдельном потоке
def run_flask():
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)  # Отключение reloader

if __name__ == "__main__":
    main()
