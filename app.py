from flask import Flask
from flask_migrate import Migrate

from db import db
from routes.clip_bp import clip_bp
from routes.comment_bp import comment_bp

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(clip_bp)
app.register_blueprint(comment_bp, url_prefix='/comment')

if __name__ == '__main__':
    app.run()
