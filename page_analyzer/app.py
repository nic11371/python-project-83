import os
from flask import (
    # get_flashed_messages,
    # flash,
    Flask,
    # redirect,
    render_template,
    # request,
    # url_for
)
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def root():
    return render_template(
        'pages/index.html'
    )
