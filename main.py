class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        val = float(value)
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name and self.unit == other.unit
        return False
    
#fl = Ingredient('мука', 2, 'кг')
#print(fl)

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio):
        new_ingredients = []
        for item in self.ingredients:
            new_ingredients.append(Ingredient(item.name, item.quantity * ratio, item.unit))
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [f"Рецепт: {self.title}"]
        
        for item in self.ingredients:
            lines.append(f"- {item}")
        return "\n".join(lines)
    
class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        summary = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            summary[key] = summary.get(key, 0.0) + ingredient.quantity
        
        result = [Ingredient(name, qty, unit) for (name, unit), qty in summary.items()]
        return sorted(result, key=lambda x: x.name)

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled_base = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_base.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"
    
#dr = DietaryRecipe("Салат", "веган")
#dr.add_ingredient(Ingredient("Огурец", 1, "шт"))
#print(dr)
#print("#########")
#print(dr.scale(3))
