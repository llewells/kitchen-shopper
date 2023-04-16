from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.id}: {self.name} ({self.size})>"

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)

    def __repr__(self):
        return f"<RecipeIngredient recipe_id={self.recipe_id}, ingredient_id={self.ingredient_id}>"

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredients', backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return f"<Recipe {self.id}: {self.name}>"
    