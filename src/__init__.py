import os
from datetime import timedelta

from dotenv import load_dotenv                                                  # type: ignore
load_dotenv()

from flask import Flask                                                         # type: ignore
from flask_bcrypt import Bcrypt                                                 # type: ignore
from flask_migrate import Migrate                                               # type: ignore
from flask_login import LoginManager                                            # type: ignore
from flask_sqlalchemy import SQLAlchemy                                         # type: ignore


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Configurações do app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()


from .core.llm import ILLM, Ollama, LLMBuilder
illm: ILLM = LLMBuilder(llm_type='ollama', model_name='llama3', temperature=0)
illm = illm.get_instance()