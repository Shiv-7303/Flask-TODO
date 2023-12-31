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
        title = request.form["title"].strip()
        desc = request.form["desc"].strip()
        todo = ToDo(desc=desc, title=title)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    return render_template("index.html", alltodo=alltodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    instance = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(instance=instance)
    db.session.commit()
    return redirect("/")


@app.route(
    "/update/<int:sno>",
    methods=[
        "GET",
        "POST",
    ],
)
def update(sno):
    if request.method == "POST":
        title = request.form["title"].strip()
        desc = request.form["desc"].strip()
        instance = ToDo.query.filter_by(sno=sno).first()
        instance.title = title
        instance.desc = desc
        db.session.add(instance)
        db.session.commit()
        return redirect("/")
    instance = ToDo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=instance)



@app.route("/search",methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        title = request.form["title"].strip()
        instance = ToDo.query.filter_by(title=title).all()
        if instance:
            return render_template("search.html", todos=instance)
        else:
            return render_template("search.html", message = "NO TODO Found")
    else:
        return render_template('search.html')
        

if __name__ == "__main__":
    app.run(debug=True)
