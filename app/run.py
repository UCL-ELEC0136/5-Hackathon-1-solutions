# pylint: skip-file
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


# Define the structure for each team's scores
class TeamForm(FlaskForm):
    team_name = StringField("Team Name", validators=[InputRequired()])
    students_score = FloatField(
        "Student's score",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=5, message="Student's score must be between 0 and 5"),
        ],
    )
    edu_score = FloatField(
        "Edu's score",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=5, message="Edu's score must be between 0 and 5"),
        ],
    )
    david_score = FloatField(
        "David's score",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=5, message="David's score must be between 0 and 5"),
        ],
    )    
    code_quality = FloatField(
        "Code quality",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=10, message="Code quality must be between 0 and 10"),
        ],
    )
    reproducibility = FloatField(
        "Reproducibility",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=1, message="Reproducibility must be between 0 and 1"),
        ],
    )
    correctness = FloatField(
        "Correctness",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=17, message="Correctness must be between 0 and 17"),
        ],
    )
    submit = SubmitField("Add Team")


# Data storage for teams
teams = []


@app.route("/", methods=["GET", "POST"])
def index():
    team_form = TeamForm()

    # Handle new team addition
    if team_form.validate_on_submit():
        new_team = {
            "team_name": team_form.team_name.data,
            "scores": [
                team_form.students_score.data,
                team_form.edu_score.data,
                team_form.david_score.data,
                team_form.code_quality.data,
                team_form.reproducibility.data,
                team_form.correctness.data,
            ],
            "maxima": [5, 5, 5, 10, 1, 17],
        }
        teams.append(new_team)
        return redirect(url_for("index"))

    # Calculate average scores for each team
    for team in teams:
        norm_scores = [
            score / maxima for score, maxima in zip(team["scores"], team["maxima"])
        ]
        team["average"] = (
            (sum(norm_scores) / len(norm_scores)) * 100 if norm_scores else 0
        )

    return render_template("index.html", team_form=team_form, teams=teams)


from flask import Flask, render_template, request, redirect, url_for, jsonify


@app.route("/update", methods=["POST"])
def update_scores():
    # Parse JSON data
    data = request.get_json()
    print(data)
    for team_key, scores in data.items():
        team_index = int(team_key.split("-")[1])
        if 0 <= team_index < len(teams):
            teams[team_index]["scores"] = list(map(float, scores))

    return jsonify(success=True)


@app.route("/delete", methods=["POST"])
def delete_team():
    # Get the team index from the form data
    team_index = int(request.form.get("team_index"))
    # Delete the team at the specified index
    if 0 <= team_index < len(teams):
        del teams[team_index]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
