import pytest

from main import Ingredient, Recipe, ShoppingList



def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 300, "г")  
    ing3 = Ingredient("Сахар", 500, "г") 
    ing4 = Ingredient("Мука", 500, "кг") 

    assert ing1 == ing2 
    assert ing1 != ing3
    assert ing1 != ing4


# 2
def test_recipe_init():
    ing = Ingredient("Мука", 500, "г")
    recipe = Recipe("Тесто", [ing])
    assert recipe.title == "Тесто"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ing

def test_recipe_add_ingredient():
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 500

    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 800

def test_recipe_scale():
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    
    scaled_recipe = recipe.scale(2)
    
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 1000
    assert recipe.ingredients[0].quantity == 500

    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_recipe_len():
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Вода", 200, "мл"))
    assert len(recipe) == 2


# 3

def test_shopping_list_add_recipe():
    sl = ShoppingList()
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    
    sl.add_recipe(recipe, 2)
    assert len(sl._items) == 1
    
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    sl = ShoppingList()
    recipe1 = Recipe("Блинчики")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    
    recipe2 = Recipe("Омлет")
    recipe2.add_ingredient(Ingredient("Яйцо", 2, "шт"))
    
    sl.add_recipe(recipe1, 1)
    sl.add_recipe(recipe2, 1)
    
    sl.remove_recipe("Блинчики")
    assert len(sl._items) == 1
    assert sl._items[0][1] == "Омлет"
    
    sl.remove_recipe("Борщ")
    assert len(sl._items) == 1

def test_shopping_list_get_list():
    sl = ShoppingList()
    
    recipe1 = Recipe("Тесто")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    
    recipe2 = Recipe("Хлеб")
    recipe2.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe2.add_ingredient(Ingredient("Вода", 200, "мл"))
    
    sl.add_recipe(recipe1, 1)
    sl.add_recipe(recipe2, 1)
    
    final_list = sl.get_list()
    
    assert len(final_list) == 2
    
    assert final_list[0].name == "Вода"
    assert final_list[0].quantity == 200
    
    assert final_list[1].name == "Мука"
    assert final_list[1].quantity == 800 

def test_shopping_list_add():
    sl1 = ShoppingList()
    recipe1 = Recipe("Тесто")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    sl1.add_recipe(recipe1, 1)

    sl2 = ShoppingList()
    recipe2 = Recipe("Омлет")
    recipe2.add_ingredient(Ingredient("Яйцо", 2, "шт"))
    sl2.add_recipe(recipe2, 1)



    sl3 = sl1 + sl2
    
    assert len(sl3._items) == 2
    assert len(sl1._items) == 1
    assert len(sl2._items) == 1