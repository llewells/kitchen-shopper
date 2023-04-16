class Recipe:
    ingredients: list = []

    def __repr__(self):
        return (
            f"Name: {self.name}, Length: {self.time}, Ingredients: {self.ingredients}"
        )

    def __init__(self, id, name="", time="", ingredients=[]) -> None:
        self.id = id
        self.set_name(name)
        self.set_time(time)
        self.add_ingredients(ingredients)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'time':self.time
        }

    def set_name(self, name) -> None:
        self.name: str = name

    def set_time(self, time) -> None:
        self.time: str = time

    def add_ingredients(self, ingredients) -> None:
        [self.add_ingredient(i) for i in ingredients]

    def add_ingredient(self, ingredient) -> None:
        self.ingredients.append(ingredient)