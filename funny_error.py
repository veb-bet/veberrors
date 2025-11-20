import random
from flask import Flask, jsonify, request, render_template_string
from werkzeug.exceptions import HTTPException
import time

app = Flask(__name__)

# ---------- Словарь ----------
dad_jokes_rus = [
    "Сотрудник хлебзавода скинул коллегу в миксер. Расследование показало, что замешан директор предприятия!",
    "— Куда мышь спрятала сыр? — Не знаю, молчит как пармезан!",
    "— Что общего у кандидата наук и лошади, идущей по улице. — Они теоретически подкованы.",
    "— Почему математик не любит природу? — Потому что в ней слишком много корней!",
    "— Что сказал один магнит другому? — Ты меня притягиваешь!",
    "— Что сказал градусник под мышкой? — Какая тёплая компания!",
]

# ---------- Универсальная функция вывода ошибки ----------
def funny_error_page(code, title, message, tip, ascii_art):
    accept = request.headers.get("Accept", "")
    payload = {
        "error": title,
        "code": code,
        "message": message,
        "tip": tip,
    }

    if "application/json" in accept.lower() or request.path.startswith("/api/"):
        return jsonify(payload), code
    else:
        html = f"""
        <html>
        <head><title>{code} — {title}</title></head>
        <body style="font-family:sans-serif; text-align:center; padding:2rem;">
            <h1>{code} — {title}</h1>
            <p style="font-size:1.1rem;">{message}</p>
            <pre style="background:#f6f6f6; display:inline-block; padding:1rem; border-radius:6px;">{ascii_art}</pre>
            <p style="color:#666; margin-top:1rem;">{tip}</p>
        </body>
        </html>
        """
        return render_template_string(html), code

# ---------- 430 ----------
class TooManyDadJokes(HTTPException):
    code = 430
    description = "Too Many Dad Jokes — вы перегрузили систему шутками."

@app.errorhandler(TooManyDadJokes)
def handle_too_many_dad_jokes(error):
    # Выбираем случайную шутку
    joke = random.choice(dad_jokes_rus)
    return funny_error_page(
        430,
        "Too Many Dad Jokes",
        f"Слишком много папиных шуток. Перезарядите чувство юмора и попробуйте снова.\n\nВот пример шутки: {joke}",
        "Совет: попробуйте отправить шутку без слова 'папа'.",
        "  (╯°□°）╯︵ ┻━┻\n  (┛◉Д◉)┛彡┻━┻  — шутки снесли стол",
    )

@app.route("/tell-a-dad-joke", methods=["POST"])
def tell_a_dad_joke():
    data = request.get_json(silent=True) or {}
    joke_sent = data.get("joke", "")
    if "папа" in joke_sent.lower() or len(joke_sent) > 140:
        raise TooManyDadJokes()
    # Если шутка нормальная — отвечаем OK и случайной шуткой
    joke = random.choice(dad_jokes_rus)
    return jsonify({"ok": True, "your_joke": joke_sent, "dad_joke": joke})

# ---------- 472 ----------
class CatInterruption(HTTPException):
    code = 472
    description = "Cat Interruption — кот прошёл по клавиатуре."

@app.errorhandler(CatInterruption)
def handle_cat_interruption(error):
    return funny_error_page(
        472,
        "Cat Interruption",
        "Ваш запрос был прерван котом, который внезапно прошёл по клавиатуре.",
        "Совет: удалите кота с клавиатуры и повторите попытку.",
        "(=^･ω･^=)  — мяу... sdfjkl;weoi",
    )

@app.route("/cat")
def cat_interruption():
    raise CatInterruption()

# ---------- 469 ----------
class OverlySarcasticRequest(HTTPException):
    code = 469
    description = "Overly Sarcastic Request — клиент был слишком саркастичен."

@app.errorhandler(OverlySarcasticRequest)
def handle_overly_sarcastic_request(error):
    return funny_error_page(
        469,
        "Overly Sarcastic Request",
        "Запрос был настолько саркастичен, что сервер не смог ответить серьёзно.",
        "Совет: попробуйте быть чуть менее ироничным в следующий раз.",
        "(¬_¬)  — правда? именно это ты хотел отправить?",
    )

@app.route("/sarcasm")
def sarcasm():
    raise OverlySarcasticRequest()

# ---------- 418 I'm a teapot (расширенная версия) ----------
class TeapotBrewing(HTTPException):
    code = 418
    description = "I'm a teapot — я чайник и завариваю чай."

@app.errorhandler(TeapotBrewing)
def handle_teapot_brewing(error):
    tea_types = ["чёрный", "зелёный", "улун", "пуэр", "травяной"]
    return funny_error_page(
        418,
        "I'm a teapot",
        f"Извините, я сейчас завариваю {random.choice(tea_types)} чай и не могу обработать ваш запрос.",
        "Совет: попробуйте позже, когда чай будет готов.",
        """
            (
          )    (
        .(       ).
         |~~~~~~|
         |      |
         |      |
        '~~~~~~~~'
        """,
    )

@app.route("/tea")
def make_tea():
    raise TeapotBrewing()

# ---------- 525 Coffee Brewing ----------
class CoffeeBrewing(HTTPException):
    code = 525
    description = "Coffee Brewing — сервер варит кофе."

@app.errorhandler(CoffeeBrewing)
def handle_coffee_brewing(error):
    return funny_error_page(
        525,
        "Coffee Brewing",
        "Сервер занят приготовлением утреннего кофе. Без кофеина он не может работать.",
        "Совет: подождите 5 минут и попробуйте снова.",
        """
        ( ( (
         ) ) )
       .........
       |      |]
       \      / 
        `----'
        """,
    )

@app.route("/coffee")
def make_coffee():
    raise CoffeeBrewing()

# ---------- 580 Procrastination ----------
class ProcrastinationError(HTTPException):
    code = 580
    description = "Procrastination Error — сервер откладывает обработку запроса на потом."

@app.errorhandler(ProcrastinationError)
def handle_procrastination(error):
    activities = [
        "листает ленту соцсетей",
        "смотрит смешные видео с котиками", 
        "реорганизует закладки в браузере",
        "играет в пасьянс",
        "упорядочивает файлы на рабочем столе"
    ]
    return funny_error_page(
        580,
        "Procrastination Error",
        f"Сервер сейчас занят: он {random.choice(activities)}. Ваш запрос будет обработан... потом.",
        "Совет: напомните серверу о запросе через пару часов.",
        """
        ╔═══════════════════╗
        ║ Я СДЕЛАЮ ЭТО...   ║
        ║   ПОТОМ!  ͡° ͜ʖ ͡°  ║
        ╚═══════════════════╝
        """,
    )

@app.route("/procrastinate")
def procrastinate():
    raise ProcrastinationError()

# ---------- 599 Time Travel Conflict ----------
class TimeTravelConflict(HTTPException):
    code = 599
    description = "Time Travel Conflict — обнаружен парадокс времени."

@app.errorhandler(TimeTravelConflict)
def handle_time_travel_conflict(error):
    return funny_error_page(
        599,
        "Time Travel Conflict",
        "Ваш запрос создал временной парадокс. Ответ был отправлен вам в прошлом, но вы его ещё не получили.",
        "Совет: проверьте свою почту завтра или вчера.",
        """
        ╔═════════════════════════╗
        ║ 🕐 → 🕑 → 🕒 → 🕓 → 🕔  ║
        ║    ПАРАДОКС!            ║
        ╚═════════════════════════╝
        """,
    )

@app.route("/time-travel")
def time_travel():
    raise TimeTravelConflict()

# ---------- 444 No Response (ленивый сервер) ----------
class TooLazyToRespond(HTTPException):
    code = 444
    description = "Too Lazy To Respond — серверу лень отвечать."

@app.errorhandler(TooLazyToRespond)
def handle_too_lazy(error):
    return funny_error_page(
        444,
        "Too Lazy To Respond",
        "Сервер прочитал ваш запрос, но ему лень формулировать ответ. Может, в другой раз?",
        "Совет: попробуйте попросить вежливее или предложить серверу кофе.",
        """
        .--.
       |o_o |
       |:_/ |
      //   \ \\
     (|     | )
    /'\_   _/`\\
    \___)=(___/
        """,
    )

@app.route("/lazy")
def lazy_endpoint():
    raise TooLazyToRespond()

# ---------- Домашняя страница ----------
@app.route("/")
def index():
    return """
    <h2>Ошибки сервера</h2>
    <ul>
        <li>POST /tell-a-dad-joke — вызывает <b>430 Too Many Dad Jokes</b> с рандомной шуткой</li>
        <li>GET /cat — вызывает <b>472 Cat Interruption</b></li>
        <li>GET /sarcasm — вызывает <b>469 Overly Sarcastic Request</b></li>
        <li>GET /tea — вызывает <b>418 I'm a Teapot</b> (расширенная версия)</li>
        <li>GET /coffee — вызывает <b>525 Coffee Brewing</b></li>
        <li>GET /procrastinate — вызывает <b>580 Procrastination Error</b></li>
        <li>GET /time-travel — вызывает <b>599 Time Travel Conflict</b></li>
        <li>GET /lazy — вызывает <b>444 Too Lazy To Respond</b></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
