from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если метод запроса GET, отобразите шаблон формы регистрации
    if request.method == 'GET':
        return render_template('register.html')
    # Если метод запроса POST, получите данные формы и проверьте их
    else:
        # Получите данные формы
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверьте данные формы
        if not (first_name and last_name and email and password):
            # Если какое-то поле отсутствует, верните сообщение об ошибке
            return 'Пожалуйста, заполните все поля.'
        elif User.query.filter_by(email=email).first():
            # Если электронная почта уже существует в базе данных, верните сообщение об ошибке
            return 'Эта электронная почта уже зарегистрирована.'
        else:
            # Если данные формы действительны, создайте нового пользователя и сохраните его в базе данных
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=generate_password_hash(password) # Зашифруйте пароль с помощью модуля werkzeug.security
            )
            db.session.add(user)
            db.session.commit()

            # Верните сообщение об успехе
            return 'Вы успешно зарегистрировались.'


if __name__ == "__main__":
    app.run(debug=True)


