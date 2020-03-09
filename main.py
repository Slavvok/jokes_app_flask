from app import app
from app.views import auth, jokes


app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(jokes.app)

from app.models import Joke, User

if __name__ == '__main__':
	app.run()

