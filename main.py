from flask import Flask, render_template, request, jsonify
from models import db, Recipe, Ingredient, RecipeIngredient
from forms import IngredientForm, RecipeForm, CreateIngredientForm, UpdateIngredientForm, UpdateRecipeForm
import secrets

# Import necessary modules from Flask-WTF
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


# Define the error handler for the 405 HTTP status code
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("error.html", message="Method Not Allowed"), 405


# Set up CSRF protection
csrf = CSRFProtect(app)


# Create a new recipe
@app.route("/recipes/create", methods=["GET", "POST"])
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        name = form.name.data
        instructions = form.instructions.data
        ingredients_data = form.ingredients.data
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
        return render_template("recipe.html", recipe=new_recipe), 201
    # If the form is not validated, render the 'create_recipe.html' template with the form
    return render_template("create_recipe.html", form=form)



# Create a new ingredient
@app.route("/ingredients/create", methods=["GET", "POST"])
def create_ingredient():
    form = CreateIngredientForm()
    if form.validate_on_submit():
        # Extract the ingredient data from the form
        name = form.name.data
        size = form.size.data
        # Create a new Ingredient object
        new_ingredient = Ingredient(name=name, size=size)
        # Add the new_ingredient object to the database session
        db.session.add(new_ingredient)
        # Commit the changes to the database
        db.session.commit()
        # Render a template with the new ingredient data
        return render_template("view_ingredient.html", ingredient=new_ingredient), 201
    # Render the 'create_ingredient.html' template with the form for creating a new ingredient
    return render_template("create_ingredient.html", form=form)



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
    # Create a new instance of RecipeForm and populate it with the recipe data
    form = RecipeForm(obj=recipe)
    # Render the template with the recipe data and the form
    return render_template("recipe.html", recipe=recipe, form=form)


@app.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    # Query the database for all Ingredient objects
    ingredients = Ingredient.query.all()
    # Create a new instance of IngredientForm for adding a new ingredient
    form = IngredientForm()
    # Render the ingredient data and the form using a template
    return render_template("ingredients.html", ingredients=ingredients, form=form)


# Retrieve a single ingredient by ID
@app.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    # Query the database for the Ingredient object with the specified ID
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        # If the ingredient doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Ingredient not found"), 404
    # Create an instance of the IngredientForm and populate it with the ingredient data
    form = IngredientForm(obj=ingredient)
    # Render a template with the ingredient data and the form for editing the ingredient
    return render_template("ingredient.html", ingredient=ingredient, form=form)



# Update a recipe by ID
@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    # Query the database for the Recipe object with the specified ID
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        # If the recipe doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Recipe not found"), 404
    
    # Create a form instance with the data from the request
    form = UpdateRecipeForm(request.form)
    
    if form.validate():
        # Update the recipe name if provided in the form
        recipe.name = form.name.data
        # Update the recipe instructions if provided in the form
        recipe.instructions = form.instructions.data
        
        # Clear the existing ingredients for the recipe
        recipe.ingredients.clear()
        # Iterate over the ingredient data in the form
        for ingredient_data in form.ingredients.data:
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
    
    # If form validation fails, render the form with the validation errors
    return render_template("edit_recipe.html", form=form, recipe=recipe), 400




@app.route("/ingredients/<int:ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    # Query the database for the Ingredient object with the specified ID
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        # If the ingredient doesn't exist, return a 404 Not Found error
        return render_template("error.html", message="Ingredient not found"), 404

    # Create an instance of the form and populate it with the request data
    form = UpdateIngredientForm(request.form)

    # Update the ingredient name and size if the form data is valid
    if form.validate_on_submit():
        ingredient.name = form.name.data
        ingredient.size = form.size.data
        # Commit the changes to the database
        db.session.commit()
        # Render the template with the updated ingredient data
        return render_template("ingredient.html", ingredient=ingredient)

    # If the form data is invalid, render the form with the validation errors
    return render_template("edit_ingredient.html", form=form, ingredient=ingredient)


# Deleting a recipe
@app.route("/recipe/<int:id>", methods=["POST"])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        # Delete all associated recipe_ingredient objects
        RecipeIngredient.query.filter_by(recipe_id=id).delete()
        # Delete the recipe object itself
        db.session.delete(recipe)
        db.session.commit()
        return (
            render_template("message.html", message="Recipe deleted successfully."),
            200,
        )
    else:
        return render_template("error.html", message="Recipe not found."), 404

# Deleting an ingredient
@app.route("/ingredient/<int:id>", methods=["POST"])
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if ingredient:
        # Delete all associated recipe_ingredient objects
        RecipeIngredient.query.filter_by(ingredient_id=id).delete()
        # Delete the ingredient object itself
        db.session.delete(ingredient)
        db.session.commit()
        return (
            render_template("message.html", message="Ingredient deleted successfully."),
            200,
        )
    else:
        return render_template("error.html", message="Ingredient not found."), 404

if __name__ == "__main__":
    app.run("localhost", port=5000)
