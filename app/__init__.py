import atexit
import pathlib
import logging
import pickle

from flask import Flask, render_template, g, request, redirect, url_for, current_app, session, abort, jsonify, flash, send_file
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from .utils.Config import Config
from .utils.logger_models import *
from logging.handlers import QueueListener, QueueHandler, RotatingFileHandler
from logging.config import dictConfig
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from sqlalchemy import URL

def load_metadata(engine):
    logger = logging.getLogger(__name__)
    try:
        with open('metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        logger.info("Metadatos cargados desde el caché.")
    except FileNotFoundError:
        metadata = MetaData()
        with open('metadata.pkl', 'wb') as f:
            pickle.dump(metadata, f)
        logger.info("Metadatos reflejados y guardados en el caché.")
    metadata.reflect(engine)
    return metadata

def setup_logging():

    config_file = pathlib.Path("app/utils/logging_configdict.json")
    dict_config = None
    with open(config_file) as f_in:
        dict_config = json.load(f_in)

    log_queue = Queue()
    logging.config.dictConfig(dict_config)
    root_logger = logging.getLogger('root')
    queue_handler = QueueHandler(log_queue)
    root_logger.addHandler(queue_handler)
    queue_listener = QueueListener(log_queue, *logging.getLogger('notusable').handlers)
    # Iniciar el listener
    queue_listener.start()
    atexit.register(queue_listener.stop)

db = SQLAlchemy()
Base = automap_base()
mail = Mail()


def create_app(config_path:str='config.json',debug=False):
    setup_logging()

    logger = logging.getLogger("init")

    # Init config file
    config = Config(config_path)

    # set logging configuration
    logging.basicConfig(
        level=config.LOG_LEVEL if config.LOG_LEVEL in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') else 'DEBUG')

    #logging.getLogger('sqlalchemy.engine').setLevel(config.LOG_LEVEL if config.LOG_LEVEL in ('DEBUG','INFO','WARNING','ERROR','CRITICAL') else 'DEBUG')

    # Init app
    app = Flask(__name__)
    if debug: app.debug = True
    logger.debug(f"App initiated with debug mode: {app.debug}")

    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
    logger.debug(f"Mail parameters configured")

    # Other configs
    app.config['SECRET_KEY'] = config.APP_SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    url_obj = URL.create("mssql+pyodbc", username=config.DB_USERNAME, password=config.DB_PASSWORD, host=config.DB_HOST,
                         database=config.DB_NAME, query={
            "driver": config.DB_DRIVER,
            "TrustServerCertificate": "yes",
            "trusted_connection": "no"
        })
    app.config['SQLALCHEMY_DATABASE_URI'] = url_obj.render_as_string(False)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logger.debug(f"Secret keys and database uri configured")

    # init sqlalchemy extension
    db.init_app(app)

    migrate = Migrate(app=app, db=db)

    # Init mail extension
    appmail = mail.init_app(app)

    # JWT setup
    jwt = JWTManager(app)

    metadata = MetaData()

    logger.debug(f"DB, migrate, appmail and jwt initiated")

    with app.app_context():
        logger.info(app.config['SQLALCHEMY_DATABASE_URI'])
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        logger.info("Engine created" + str(engine))

        metadata = load_metadata(engine)
        logger.info(f"metadata loaded")

        Base.metadata = metadata
        Base.prepare(engine, reflect=True)
        logger.info(f"Base prepared")

        from .models import User,Cliente,TiquetCabecera,TiquetLinea,Almacen

        logger.info(f"Models imported, preparing base")
        Base.prepare(engine, reflect=True)
        logger.info(f"Base prepared with models")

        app.config['Base'] = Base

        from .login import login_bp

        app.register_blueprint(login_bp)

        from .time_series import timeseries_bp

        app.register_blueprint(timeseries_bp)

        logger.info(f"Creating all tables")
        Base.metadata.create_all(engine)

    @app.route('/')
    def index():
        return jsonify({'message': 'Hello World!'})


    return app