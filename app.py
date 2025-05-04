from flask import Flask , render_template , request ,flash , url_for , redirect
from flask_sqlalchemy import SQLAlchemy
from utils.software_types import Software_types
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:@localhost:3306/disisolves"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "BIANCA"
db = SQLAlchemy(app)


@app.route("/")
def index():
    problems = Problems.query.all()
    return render_template("index.html" , problems = problems)

@app.route("/disisolves/admin/problems/create" , methods=("GET" , "POST"))
def create_problems():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        software_types = request.form.get('software_types') #flash_messages = [Tile Reuired , description]
        has_error = False
        if not title:
            flash("Title required" , category="error")
            has_error = True
        if not description:
             flash("Description requred" , category="error")
             has_error = True
        if not software_types:
            flash("Software Types Required" , category="error")
            has_error = True
        if not has_error:
            db.session.add(Problems(
                title =  title,
                description = description,
                software_types = software_types,
                posted_by = "Bianca"
            ))

            db.session.commit()

            return redirect("/")
    return render_template("admin/create_problems.html")


@app.route("/disisolves/problems/<id>")
def problem_details(id):
    problem = Problems.query.filter_by(id = id).first_or_404()
    return render_template("problem_detail.html" , problem=problem)



@app.route("/disisolves/admin/problems/<id>/edit")
def update_problem(id):
    return render_template("admin/update_problem.html")


class Problems(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title=db.Column(db.Text , nullable = False)
    description =db.Column(db.Text , nullable = False)
    software_types =db.Column(db.Enum(Software_types) , nullable = False)
    posted_by =db.Column(db.Text , nullable = False)
    posted_at = db.Column(db.DateTime, default = datetime.UTC)

with app.app_context():
    db.create_all()



