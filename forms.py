from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectMultipleField,
    SubmitField,
    FloatField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length, Optional


# Create a form for ingredient
class IngredientForm():
    name = StringField("Ingredient Name", validators=[DataRequired()])
    size = StringField("Ingredient Size", validators=[DataRequired()])


# Create a form for creating a new ingredient
class CreateIngredientForm(FlaskForm, IngredientForm):
    submit = SubmitField("Create Ingredient")

class UpdateIngredientForm(FlaskForm, IngredientForm):
    update = SubmitField("Update Ingredient" )
    delete = SubmitField("Delete Ingredient" )

# Define a delete form for ingredients
class DeleteIngredientForm(FlaskForm, IngredientForm):
    delete = SubmitField("Delete Ingredient" )


# Create a form for creating a new recipe
class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    instructions = TextAreaField("Instructions", validators=[DataRequired()])
    ingredients = SelectMultipleField("Ingredients", validators=[DataRequired()])
    new_ingredient_name = StringField("New Ingredient Name")
    new_ingredient_size = StringField("New Ingredient Size")


class UpdateRecipeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    instructions = TextAreaField("Instructions", validators=[DataRequired()])
    ingredients = SelectMultipleField(
        "Ingredients", coerce=int, validators=[DataRequired()]
    )
    amounts = FloatField("Amounts", validators=[DataRequired()])


# Define a delete form for recipes
class RecipeDeleteForm(FlaskForm):
    submit = SubmitField("Delete")
