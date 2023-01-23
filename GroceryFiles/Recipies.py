import sqlite3


class Ingredient:
    def __init__(self, amount:float, unit:str, name:str):
        self.__name = name
        self.__amount = float(amount)
        self.__unit = unit

    def __str__(self):
        return "{0} {1} {2}".format(round(self.__amount, 2), self.__unit, self.__name)
    
    def GetName(self):
        return self.__name
    
    def GetAmount(self):
        return self.__amount
    
    def Add(self, amount):
        self.__amount += amount
    
    def GetUnit(self):
        return self.__unit


class Recipe:
    def __init__(self, name:str, ingredients:Ingredient):
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

    def __repr__():
        return "Recipe()"

    def __str__(self):
        return self.__name


class Grocery_Item:
    def __init__(self, amount:int, name:str):
        self.__amount = amount
        self.__name = name

    def __str__(self):
        return "{0} {1}".format(self.__amount, self.__name)


def create_tables(cursor):
    cursor.execute('''CREATE TABLE ingredients (
                        id INTEGER PRIMARY KEY,
                        name TEXT);''')
    cursor.execute('''CREATE TABLE recipes (
                        id INTEGER PRIMARY KEY,
                        name TEXT);''')
    cursor.execute('''CREATE TABLE recipe_ingredient (
                        id INTEGER PRIMARY KEY,
                        recipe_id INTEGER,
                        ingredient_id INTEGER,
                        amount TEXT,
                        unit TEXT,
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id));''')


# Function to insert a new ingredient
def insert_ingredient(cursor, ingredient):
    cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (ingredient,))
    ingredient_id = cursor.lastrowid
    return ingredient_id

# Function to insert a new recipe
def insert_recipe(cursor, recipe):
    cursor.execute("INSERT INTO recipes (name) VALUES (?)", (recipe["__name"],))
    recipe_id = cursor.lastrowid
    return recipe_id

# Function to insert a new recipe_ingredient relationship
def insert_recipe_ingredient(cursor, recipe_id, ingredient_id, amount, unit):
    cursor.execute("INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount, unit) VALUES (?,?,?,?)", (recipe_id, ingredient_id, amount, unit))


def push_recipe(recipe):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("Select name from recipes where name = ?", (recipe["__name"],))
    result = cursor.fetchall()

    if len(result) == 0:
        recipe_id = insert_recipe(cursor, recipe)
        ingredients = recipe["__ingredients"]

        for ingredient in ingredients:
            ingredient_id = insert_ingredient(cursor, ingredient["__name"])
            insert_recipe_ingredient(cursor, recipe_id, ingredient_id, ingredient["__amount"], ingredient["__unit"])

    conn.commit()
    conn.close()

def fetch_recipe_ID(recipe_id:int):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    query = "SELECT name FROM recipes WHERE id = ?"
    cursor.execute(query, (recipe_id,))
    recipe_name = cursor.fetchone()[0]

    query =  """
    SELECT recipe_ingredient.amount, recipe_ingredient.unit, ingredients.name
    FROM recipes
    JOIN recipe_ingredient ON recipes.id = recipe_ingredient.recipe_id
    JOIN ingredients ON recipe_ingredient.ingredient_id = ingredients.id
    WHERE recipes.id = ?
    """

    # Execute the query
    cursor.execute(query, (recipe_id,))

    # Fetch the results
    results = cursor.fetchall()

    ingredients = []

    for i in results:
        ingredient = Ingredient(i[0], i[1], i[2])
        ingredients.append(ingredient)

    recipe = Recipe(recipe_name, ingredients)

    conn.close()

    return recipe

def fetch_recipe_name(name:str):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    query = "SELECT id FROM recipes WHERE name = ?"
    cursor.execute(query, (name,))
    recipe_id = cursor.fetchone()[0]

    query =  """
    SELECT recipe_ingredient.amount, recipe_ingredient.unit, ingredients.name
    FROM recipes
    JOIN recipe_ingredient ON recipes.id = recipe_ingredient.recipe_id
    JOIN ingredients ON recipe_ingredient.ingredient_id = ingredients.id
    WHERE recipes.id = ?
    """

    # Execute the query
    cursor.execute(query, (recipe_id,))

    # Fetch the results
    results = cursor.fetchall()

    ingredients = []

    for i in results:
        ingredient = Ingredient(i[0], i[1], i[2])
        ingredients.append(ingredient)

    recipe = Recipe(name, ingredients)

    conn.close()

    return recipe

def fuzzy_recipe_search(name:str):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    query = f"SELECT id, name FROM recipes WHERE name LIKE '%{name}%'"
    cursor.execute(query)
    matches = cursor.fetchall()

    recipeDict = {}

    for match in matches:
        recipeDict[match[1]] = match[0]

    conn.close()

    return recipeDict

recipeCount = -1

# Get Recipe by ID
tempRecipe = fetch_recipe_ID(60).ToDict()
print(tempRecipe['__name'])

for ing in tempRecipe["__ingredients"]:
    print(ing)

print()

# Get Recipe by NAME
tempRecipe = fetch_recipe_name("Chicken Biryani").ToDict()
print(tempRecipe['__name'])

for ing in tempRecipe["__ingredients"]:
    print(ing)

recipe_matches = fuzzy_recipe_search("indian")
print(len(recipe_matches))
print()