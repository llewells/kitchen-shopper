from classes.recipe import Recipe
from classes.ingredient import Ingredient

def main() -> None:
    spag = Ingredient("spag", 1)
    spag.set_weight(100)

    bol = Ingredient("bol")
    bol.set_weight(50)

    ingredients = [spag, bol]

    spag_bol = Recipe(name="spag bol", time="10mins", ingredients=ingredients)

    print(spag_bol)


if __name__ == "__main__":
    main()
