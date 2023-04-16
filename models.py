from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)

    def __init__(self, name, description, ingredients, instructions):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.instructions =  instructions
 
    def __repr__(self):
        return f"{self.name}:{self.id}"

