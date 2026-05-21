from flask import Flask, render_template, request
from services.database import init_db, save_message, get_history, clear_history
from services.bot_engine import ChatBotEngine

app = Flask(__name__)
init_db()
bot = ChatBotEngine()


@app.route('/', methods=['GET', 'POST'])
def index():
    notice = None
    user_message = ''

    if request.method == 'POST':
        if 'clear_history' in request.form:
            clear_history()
            notice = 'Chat history was cleared successfully.'
        else:
            user_message = request.form.get('message', '').strip()
            bot_reply = bot.get_response(user_message)

            if user_message:
                save_message('user', user_message)
            save_message('bot', bot_reply)

    history = get_history()
    return render_template('index.html', history=history, notice=notice, user_message='')


if __name__ == '__main__':
    app.run(debug=True)
