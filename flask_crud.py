from flask import Flask, render_template, request, jsonify
from models import db, Recipe, Ingredient, RecipeIngredient

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


# Create a new recipe
@app.route("/recipes", methods=["POST"])
def create_recipe():
    # Extract the recipe data from the request body
    recipe_data = request.get_json()
    name = recipe_data["name"]
    instructions = recipe_data["instructions"]
    ingredients_data = recipe_data["ingredients"]
    # Create a new Recipe object
    new_recipe = Recipe(name=name, instructions=instructions)
    # Loop through the ingredients data and create Ingredient and RecipeIngredient objects
    for ingredient_data in ingredients_data:
        # Check if the ingredient already exists in the database
        ingredient = Ingredient.query.filter_by(name=ingredient_data["name"]).first()
        if not ingredient:
            # If the ingredient doesn't exist, create a new Ingredient object
            ingredient = Ingredient(
                name=ingredient_data["name"], size=ingredient_data["size"]
            )
            db.session.add(ingredient)
        # Create a new RecipeIngredient object linking the recipe and the ingredient
        recipe_ingredient = RecipeIngredient(
            amount=ingredient_data["amount"], ingredient=ingredient
        )
        # Add the RecipeIngredient object to the new_recipe.ingredients relationship
        new_recipe.ingredients.append(recipe_ingredient)
    # Add the new_recipe object to the database session
    db.session.add(new_recipe)
    # Commit the changes to the database
    db.session.commit()
    # Render the 'recipe.html' template with the new recipe data
    return render_template('recipe.html', recipe=new_recipe), 201


# Create a new ingredient
@app.route("/ingredients", methods=["POST"])
def create_ingredient():
    # Extract the ingredient data from the request body
    ingredient_data = request.get_json()
    name = ingredient_data["name"]
    size = ingredient_data["size"]
    # Create a new Ingredient object
    new_ingredient = Ingredient(name=name, size=size)
    # Add the new_ingredient object to the database session
    db.session.add(new_ingredient)
    # Commit the changes to the database
    db.session.commit()
    # Render a template with the new ingredient data
    return render_template("view_ingredient.html", ingredient=new_ingredient), 201



# Retrieve all recipes
@app.route("/recipes", methods=["GET"])
def get_all_recipes():
    # Query the database for all Recipe objects
    recipes = Recipe.query.all()
    # Render the recipe data using a template
    return render_template("recipes.html", recipes=recipes)



# Retrieve a single recipe by ID
@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    # Query the database for the Recipe object with the specified ID
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        # If the recipe doesn't exist, return a 404 Not Found error
        return render_template("404.html"), 404
    # Return a rendered template with the recipe data
    return render_template("recipe.html", recipe=recipe)



# Retrieve all ingredients
@app.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    # Query the database for all Ingredient objects
    ingredients = Ingredient.query.all()
    # Render the ingredient data using a template
    return render_template("ingredients.html", ingredients=ingredients)


# Retrieve a single ingredient by ID
@app.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    # Query the database for the Ingredient object with the specified ID
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        # If the ingredient doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Ingredient not found"), 404
    # Render a template with the ingredient data
    return render_template("ingredient.html", ingredient=ingredient)


# Update a recipe by ID
@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    # Query the database for the Recipe object with the specified ID
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        # If the recipe doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Recipe not found"), 404
    # Update the recipe name if provided in the request
    if "name" in request.json:
        recipe.name = request.json["name"]
    # Update the recipe instructions if provided in the request
    if "instructions" in request.json:
        recipe.instructions = request.json["instructions"]
    # Update the recipe ingredients if provided in the request
    if "ingredients" in request.json:
        # Clear the existing ingredients for the recipe
        recipe.ingredients.clear()
        # Iterate over the ingredient data in the request
        for ingredient_data in request.json["ingredients"]:
            # Query the database for the Ingredient object with the specified ID
            ingredient = Ingredient.query.get(ingredient_data["id"])
            if not ingredient:
                # If the ingredient doesn't exist, return a 404 Not Found error
                return render_template("error.html", message="Ingredient not found"), 404
            # Create a new Recipe_Ingredient object with the specified amount
            recipe_ingredient = RecipeIngredient(
                amount=ingredient_data["amount"], ingredient=ingredient
            )
            # Add the Recipe_Ingredient object to the recipe
            recipe.ingredients.append(recipe_ingredient)
    # Commit the changes to the database
    db.session.commit()
    # Render the template with the updated recipe data
    return render_template("recipe.html", recipe=recipe)


# Update an ingredient by ID
@app.route("/ingredients/<int:ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    # Query the database for the Ingredient object with the specified ID
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        # If the ingredient doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Ingredient not found"), 404
    # Update the ingredient name if provided in the request
    if "name" in request.json:
        ingredient.name = request.json["name"]
    # Update the ingredient size if provided in the request
    if "size" in request.json:
        ingredient.size = request.json["size"]
    # Commit the changes to the database
    db.session.commit()
    # Render the template with the updated ingredient data
    return render_template("ingredient.html", ingredient=ingredient)


# Deleting a recipe
@app.route("/recipe/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        # Delete all associated recipe_ingredient objects
        RecipeIngredient.query.filter_by(recipe_id=id).delete()
        # Delete the recipe object itself
        db.session.delete(recipe)
        db.session.commit()
        return render_template("message.html", message="Recipe deleted successfully."), 200
    else:
        return render_template("error.html", message="Recipe not found."), 404


# Deleting an ingredient
@app.route("/ingredient/<int:id>", methods=["DELETE"])
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if ingredient:
        # Delete all associated recipe_ingredient objects
        RecipeIngredient.query.filter_by(ingredient_id=id).delete()
        # Delete the ingredient object itself
        db.session.delete(ingredient)
        db.session.commit()
        return render_template("message.html", message="Ingredient deleted successfully."), 200
    else:
        return render_template("error.html", message="Ingredient not found."), 404
