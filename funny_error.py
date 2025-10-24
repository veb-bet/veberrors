# funny_error.py
from flask import Flask, jsonify, request, render_template_string
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

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
    return funny_error_page(
        430,
        "Too Many Dad Jokes",
        "Слишком много папиных шуток. Перезарядите чувство юмора и попробуйте снова.",
        "Совет: попробуйте отправить шутку без слова 'папа'.",
        "  (╯°□°）╯︵ ┻━┻\n  (┛◉Д◉)┛彡┻━┻  — шутки снесли стол",
    )

@app.route("/tell-a-dad-joke", methods=["POST"])
def tell_a_dad_joke():
    data = request.get_json(silent=True) or {}
    joke = data.get("joke", "")
    if "папа" in joke.lower() or len(joke) > 140:
        raise TooManyDadJokes()
    return jsonify({"ok": True, "you_sent": joke})


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


# ---------- Домашняя страница ----------
@app.route("/")
def index():
    return """
    <h2>Ошибки сервера</h2>
    <ul>
        <li>POST /tell-a-dad-joke — вызывает <b>430 Too Many Dad Jokes</b></li>
        <li>GET /cat — вызывает <b>472 Cat Interruption</b></li>
        <li>GET /sarcasm — вызывает <b>469 Overly Sarcastic Request</b></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
