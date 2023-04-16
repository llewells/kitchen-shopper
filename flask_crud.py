from flask import Flask, abort, render_template, request, redirect
from models import db, Recipe

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/data/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createpage.html")

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        recipe = Recipe(
            name=name,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect("/data")


@app.route("/data")
def RetrieveDataList():
    recipes = Recipe.query.all()
    return render_template("datalist.html", recipes=recipes)


@app.route("/data/<int:id>")
def RetrieveSingleRecipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if recipe:
        return render_template("data.html", recipe=recipe)
    return f"Recipe with id = {id} Doenst exist"


@app.route("/data/<int:id>/update", methods=["GET", "POST"])
def update(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if request.method == "POST":
        if recipe:
            db.session.delete(recipe)
            db.session.commit()

            name = request.form["name"]
            description = request.form["description"]
            ingredients = request.form["ingredients"]
            instructions = request.form["instructions"]

            recipe = Recipe(
                name=name,
                description=description,
                ingredients=ingredients,
            )

            db.session.add(recipe)
            db.session.commit()
            return redirect(f"/data/{id}")
        return f"recipe with id = {id} Does nit exist"

    return render_template("update.html", recipe=recipe)


@app.route("/data/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if request.method == "POST":
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return redirect("/data")
        abort(404)

    return render_template("delete.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
