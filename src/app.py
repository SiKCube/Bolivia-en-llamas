from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from jinja2 import FileSystemLoader, Environment

app = Flask(__name__)

#Flask CONFIGURATION

template_loader = FileSystemLoader(app.template_folder)
template_env = Environment(loader=template_loader, auto_reload=True)

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#    username="SiKCube",
#    password="p4n.21n.qu3s0",
#    hostname="SiKCube.mysql.pythonanywhere-services.com",
#    databasename="SiKCube$default",
# )

SQLALCHEMY_DATABASE_URI = "mysql://root:qbo`tjo`rvftp@localhost/tests_db"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    content = db.Column(db.String(4096))

    @staticmethod
    def add_comment(nombre, comentario):
        comment = Comment(name=nombre, content=comentario)

        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def read_all():
        data = db.session.query(Comment).all()
        return_db = []

        for row in data:
            return_db.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "comment": row.content
                }
            )
        return return_db


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("inicio.html")


@app.route('/que-es')
def que_es():
    return render_template("que-es.html")


@app.route('/causas')
def causas():
    return render_template("causas.html")


@app.route('/beneficios')
def beneficios():
    return render_template("beneficios.html")


@app.route('/danos')
def danos():
    return render_template("danos.html")


@app.route('/fuentes')
def fuentes():
    return render_template("fuentes.html")


@app.route('/comentarios', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        nombre = request.form['name']
        comentario = request.form['comment']

        Comment.add_comment(nombre=nombre, comentario=comentario)
        return redirect(url_for("home"))
    return template_env.get_template('comments.html').render(comments=Comment.read_all())


if __name__ == '__main__':
    app.run(debug=True, port=1000)
