#Grocery app
import math

confirm = 'y'
recipes = {'pancakes':[[1.5, "cup", 'all-purpose flour'], [3.5, 'tbs', 'baking powder'], [.25, 'tsp', 'salt'], [1.25, 'cup', 'milk'], [3, 'tbs', 'butter'], [1, 'whole', 'egg']],
        "broccoli cheddar soup":[[1, 'whole', 'onion'], [3, 'clove', 'garlic'], [1, 'whole', 'potato'], [1, 'whole', 'broccoli'], [200, 'gram', 'spinach'], [1, 'liter', 'chicken stock'], [100, "ml", 'cream'], [400, 'gram', 'cheddar'], [2, 'tbs', 'olive oil']]}
selected_recipes = []
unit_items = {"all-purpose flour":2267.962, "baking powder":230, "salt":737, "milk":3.78, "butter":454, "egg":12, 'olive oil':.504, 'cheddar':907.185, "cream":907.185, 'spinach':311.845, 'chicken stock':1, "garlic":1, 'onion':1, 'potato':1}
gram_list = {"all-purpose flour":{"cup":120, 'tbs':7.8, 'tsp':2.6, 'gram':1}, "baking powder":{"cup":220.8, 'tbs':13.8, 'tsp':4, 'gram':1}, "salt":{"cup":273, 'tbs':17.06, 'tsp':7, 'gram':1}, "butter":{"cup":227, 'tbs':14, 'tsp':4.7, 'gram':1}, 'spinach':{"cup":30.0467060355, 'gram':1}, 'cheddar':{"cup":120, 'gram':1}}
liter_list = {"milk":{"cup":.236588, 'tbs':.0147868, 'tsp':.00492892, 'ml':.001, 'liter':1}, 'chicken stock':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}, 'cream':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}, 'olive oil':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}}
whole_list = {"egg": {"carton": 12, "whole": 1}, 'garlic':{'whole':1, "bulb":1, 'clove':1}, "onion":{'whole': 1}, 'broccoli':{"head": 1, 'whole':1}, 'potato':{'whole':1}}
grocery_list = []
shopping_list = []


def convert_to_g_L(measure, unit, name, multi = 1):
    converted_measure_list = []
    if name in gram_list:
        converted_measure = 0
        converted_measure += measure * multi * gram_list[name][unit]
        converted_measure_list.append(converted_measure)
        converted_measure_list.append(unit)
        converted_measure_list.append(name)
        return (converted_measure_list)
    elif name in liter_list:
        converted_measure = 0
        converted_measure += measure * multi * liter_list[name][unit]
        converted_measure_list.append(converted_measure)
        converted_measure_list.append(unit)
        converted_measure_list.append(name)
        return (converted_measure_list)
    else:
        converted_measure = 0
        print(measure, unit, name, multi)
        converted_measure += measure * multi * whole_list[name][unit]
        converted_measure_list.append(converted_measure)
        converted_measure_list.append(unit)
        converted_measure_list.append(name)
        return (converted_measure_list)

while confirm == 'y':
    selected_recipes.append(recipes[input('Which recipes do you want to shop for: ')])
    multi = int(input("How many times will you make this meal?"))
    confirm = input('Add another? [y] or [n]')

#print(selected_recipes)
for list in selected_recipes:
    for i in list:
        grocery_list.append(convert_to_g_L(i[0], i[1], i[2], multi))


def unit_item_calc():
    whole_item = []
    for list in grocery_list:
        if list == None:
            continue
        if list[2] in unit_items:
            whole_item.append(math.ceil(list[0] / unit_items[list[2]]))
            whole_item.append(list[2])

    return whole_item


shopping_list.append(unit_item_calc())

print(shopping_list)