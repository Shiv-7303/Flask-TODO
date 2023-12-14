from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app=app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, autoincrement=True)
    desc = db.Column(
        db.String(100),
        nullable=False,
    )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"


with app.app_context():
    db.create_all()


@app.route(
    "/",
    methods=[
        "GET",
        "POST",
    ],
)
def home():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = ToDo(desc=desc, title=title)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    return render_template("index.html",alltodo=alltodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    instance = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(instance=instance)
    db.session.commit()
    return redirect("/")

@app.route("/update",)
def update(sno):
    return "This is the product page"


if __name__ == "__main__":
    app.run(debug=True)
