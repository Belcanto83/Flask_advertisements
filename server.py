from flask import Flask

from urls import register_api
from models import Advertisement, User
from db_schema import db, DSN

# Создаем экземпляры нашего приложения и БД, связываем их между собой
app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = DSN
app.config['JSON_AS_ASCII'] = False
db.init_app(app)

# Создаем таблицы БД
with app.app_context():
    # db.drop_all()
    db.create_all()

# Регистрируем маршруты
register_api(app, Advertisement, 'advertisements')
register_api(app, User, 'users')

# @app.route('/')
# def hello_world():
#     return jsonify({'hello': 'world'})

# app.add_url_rule('/', view_func=hello_world, methods=['GET'])

# Запускаем приложение (сервер)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
