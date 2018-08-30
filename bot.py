# *-* coding: utf-8 *-*
import telebot, os
from aiohttp import web
import utils

token=os.environ["BOT_API_TOKEN"]

WEBHOOK_HOST = 'zaycevmusicbot.herokuapp.com'
WEBHOOK_PORT = int(os.environ.get("PORT","8443"))
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://{}".format(WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/{}/".format(token)

bot=telebot.AsyncTeleBot(token)
app = web.Application()

async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post('/{token}/', handle)

@bot.message_handler(commands=["start","help"])
def help(message):
    bot.send_message(message.chat.id,
'''Привет!
Я бот для поиска музыки на zaycev.net
Команды:
/help - вывести эту справку
/search - искать музыку
Для поиска введите что искать, затем выберите подходящую музыку, и наконец введите что отправить:
ссылку или файл
Бот сделан пользователем MrNaif_bel (https://t.me/MrNaif_bel)
За идею спасибо Zefirka_number_1 (https://t.me/Zefirka_number_1)''')
@bot.message_handler(commands=["search"])
def pre_search(message):
    sent=bot.send_message(message.chat.id,"Введите, что искать:")
    bot.register_next_step_handler(sent.wait(),search)

def search(message):
    try:
        lst, names=utils.main(message.text)
    except TypeError:
        bot.send_message(message.chat.id,"Ничего не было найдено!")
        return
    s="Выберите музыку командами 1, 2 и т.д."
    for i in range(0,len(names)):
        s+="\n"+str(i+1)+". "+names[i]
    sent=bot.send_message(message.chat.id,s)
    bot.register_next_step_handler(sent.wait(),select_name,lst)

def select_name(message, lst):
    selected=message.text
    try:
        selected=int(selected)
    except (ValueError, TypeError):
        bot.send_message(message.chat.id, "Введите цифры(1,2 и т.д.)")
    else:
        try:
            selected=lst[selected-1]
        except IndexError:
            bot.send_message(message.chat.id,"Введите номер существующей песни")
        else:
            sent=bot.send_message(message.chat.id,"Введите что отправить: 'ссылка', 'файл'")
            bot.register_next_step_handler(sent.wait(), send_it, selected)

def send_it(message, selected):
    text=message.text.lower()
    if text == "ссылка":
        bot.send_message(message.chat.id,selected)
    elif text == "файл":
        bot.send_audio(message.chat.id,selected)
    else:
        bot.send_message(message.chat.id,"Введите 'ссылка' или 'файл'")

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT
)
#polling for testing
'''if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except:
            pass'''
