class Ingredient:
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.get_details()

    def __init__(self, name, weight=0) -> None:
        self.set_name(name)
        self.set_weight(weight)

    def set_name(self, name) -> None:
        self.name: str = name

    def set_weight(self, weight) -> None:
        self.weight: int = weight

    def get_details(self) -> str:
        return f"{self.name}: {self.weight}"