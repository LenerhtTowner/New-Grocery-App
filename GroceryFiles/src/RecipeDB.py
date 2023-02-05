import sqlite3
from typing import List

### Usage example############################################################################################################################################################################
# recipe_db = RecipeDb('recipes.db')
# recipe_db.create_tables()

# recipe1 = Recipe("Spaghetti Bolognese", [Ingredient(1, "lb", "Ground beef"), Ingredient(1, "can", "Crushed tomatoes"), Ingredient(1, "tsp", "Salt"), Ingredient(1, "tsp", "Pepper")])
# recipe_db.push_recipe(recipe1)

# print(recipe_db.fetch_recipe_ID(1))
# print(recipe_db.fetch_all_recipes())

# recipe_db.close()
#############################################################################################################################################################################################

class Ingredient:
    def __init__(self, amount:float, unit:str, name:str):
        self.__name = name
        self.__amount = amount
        self.__unit = unit


    def __str__(self):
        return "{0} {1} {2}".format(round(self.__amount, 2), self.__unit, self.__name)
    

    def GetName(self):
        return self.__name
    

    def GetAmount(self):
        return self.__amount
    
    
    def GetUnit(self):
        return self.__unit
    

    def Add(self, amount):
        self.__amount += amount


class Recipe:
    def __init__(self, name:str, ingredients:List[Ingredient]):
        self.__name = name
        self.__ingredients = ingredients


    def GetName(self):
        return self.__name
    

    def GetIngredients(self):
        return self.__ingredients


    def ToDict(self):
        jsonData = {'__name': self.__name, '__ingredients': []}
        for ing in self.__ingredients:
            jsonData['__ingredients'].append(ing.__dict__)

        return jsonData


    def __str__(self):
        return self.__name


class Grocery_Item:
    def __init__(self, amount:int, name:str):
        self.__amount = amount
        self.__name = name

    def __str__(self):
        return "{0} {1}".format(self.__amount, self.__name)


class RecipeDb:
    def __init__(self, db_name:str):
        self.conn = sqlite3.connect(db_name)


    def CreateTables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE ingredients (
                            id INTEGER PRIMARY KEY,
                            name TEXT);''')
        cursor.execute('''CREATE TABLE recipes (
                            id INTEGER PRIMARY KEY,
                            name TEXT);''')
        cursor.execute('''CREATE TABLE recipe_ingredients (
                            id INTEGER PRIMARY KEY,
                            recipe_id INTEGER,
                            ingredient_id INTEGER,
                            amount REAL,
                            unit TEXT,
                            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id));''')
        self.conn.commit()


    def InsertIngredient(self, ingredient: Ingredient):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (ingredient.get_name(),))
        ingredient_id = cursor.lastrowid
        self.conn.commit()
        return ingredient_id


    def InsertRecipe(self, recipe: Recipe):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO recipes (name) VALUES (?)", (recipe.get_name(),))
        recipe_id = cursor.lastrowid
        self.conn.commit()
        return recipe_id


    def InsertRecipeIngredient(self, recipe_id: int, ingredient_id: int, amount: float, unit: str):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES (?,?,?,?)", (recipe_id, ingredient_id, amount, unit))
        self.conn.commit()


    def PushRecipe(self, recipe: Recipe):
        cursor = self.conn.cursor()
        cursor.execute("Select name from recipes where name = ?", (recipe.get_name(),))
        result = cursor.fetchall()

        if len(result) == 0:
            recipe_id = self.insert_recipe(recipe)
            ingredients = recipe.get_ingredients()

            for ingredient in ingredients:
                ingredient_id = self.insert_ingredient(ingredient)
                self.insert_recipe_ingredients(recipe_id, ingredient_id, ingredient.get_amount(), ingredient.get_unit())


    def FetchRecipe_ID(self, recipe_id:int):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM recipes WHERE id = {recipe_id}")
        name = cursor.fetchone()
        cursor.execute('''SELECT recipe_ingredients.amount, recipe_ingredients.unit, ingredients.name
                          FROM recipes
                          JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
                          JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
                          WHERE recipes.id = ?''', (recipe_id,))
        result = cursor.fetchall()
        ingredients = []
        for row in result:
            ingredients.append(Ingredient(row[0], row[1], row[2]))
        recipe = Recipe(name[0], ingredients)
        return recipe


    def FetchRecipe_Name(self, name:str):
        cursor = self.conn.cursor()
        query = "SELECT id FROM recipes WHERE name = ?"
        cursor.execute(query, (name,))
        recipe_id = cursor.fetchone()[0]

        # Execute the query
        cursor.execute("""SELECT recipe_ingredients.amount, recipe_ingredients.unit, ingredients.name
                      FROM recipes
                      JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
                      JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
                      WHERE recipes.id = ?
                      """, (recipe_id,))
        results = cursor.fetchall()

        ingredients = []

        for i in results:
            ingredient = Ingredient(i[0], i[1], i[2])
            ingredients.append(ingredient)

        recipe = Recipe(name, ingredients)

        return recipe
        
        
    def FuzzyRecipeSearch(self, name:str):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id, name FROM recipes WHERE name LIKE '%{name}%'")
        matches = cursor.fetchall()

        recipeDict = {}

        for match in matches:
            recipeDict[match[1]] = match[0]

        return recipeDict
    

    def Close(self):
        print("RecipeDB.Close()")
        if (self.conn != None):
            self.conn.close()


recipeDB = RecipeDb("GroceryFiles\\assets\\recipes.db")