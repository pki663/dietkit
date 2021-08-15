#%%
import pandas as pd
from .elements import Ingredient, Food, Diet
import re
from os.path import dirname

#%%
def load_ingredients(file_path = None):
    if file_path == None:
        file_path = dirname(__file__) + '/sample_data/sample_ingredients.csv'
    raw_df = pd.read_csv(file_path, encoding = 'cp949', index_col = 0)
    sample_ingredients = {}
    for idx in raw_df.index:
        sample_ingredients[idx] = Ingredient(name = idx, nutrition = pd.to_numeric(raw_df.loc[idx].iloc[1:]).to_dict(), category = raw_df.loc[idx, 'Category'])
    '''
    if add_to_global:
        for key, value in sample_ingredients.items():
            var_name = re.sub('[^0-9a-zA-Zㄱ-힗]', '', key)
            globals()[var_name] = value
    '''
    return sample_ingredients

#%%
def load_foods(ingredients = load_ingredients(), file_path = None):
    if file_path == None:
        file_path = dirname(__file__) + '/sample_data/sample_foods.csv'
    raw_df = pd.read_csv(file_path, encoding = 'cp949', index_col = None)
    raw_ingredients = pd.DataFrame(data = raw_df['weight'].values, index = pd.MultiIndex.from_frame(raw_df.fillna(method = 'ffill')[['name', 'ingredient']]), columns = ['weight'])
    info = raw_df.loc[pd.notna(raw_df['name']), ['name', 'category', 'note']].set_index('name')
    del raw_df

    sample_foods = {}
    for food_name in info.index:
        temp_ingredients = raw_ingredients.xs(food_name)['weight'].to_dict()
        converted_ingredients = {}
        for temp_ing in temp_ingredients.keys():
            converted_ingredients[ingredients[temp_ing]] = temp_ingredients[temp_ing]
        sample_foods[food_name] = Food(name = food_name, ingredients = converted_ingredients, category = info.loc[food_name, 'category'], note = info.loc[food_name, 'note'])
    '''
    if add_to_global:
        for key, value in sample_foods.items():
            var_name = re.sub('[^0-9a-zA-Zㄱ-힗]', '', key)
            globals()[var_name] = value
    '''
    return sample_foods

# %%
def load_diets(foods = load_foods(), num_loads = 100, file_path = None):
    assert num_loads <= 500, "The maximum number of sample diets is 500"
    if file_path == None:
        file_path = dirname(__file__) + '/sample_data/sample_diet.csv'
    raw_df = pd.read_csv(file_path, encoding = 'cp949', index_col = 0).iloc[:num_loads]
    converted_dict = {}
    for idx in raw_df.index:
        converted_foods = []
        for raw_food in list(raw_df.loc[idx].values):
            converted_foods.append(foods[raw_food])
        converted_dict[idx] = converted_foods
    sample_diet = Diet(converted_dict)
    return sample_diet
# %%
