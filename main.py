from app import create_app
from config import Config
from app.views import auth, jokes

app = create_app(Config)

app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(jokes.jokes)


if __name__ == '__main__':
    app.run()
