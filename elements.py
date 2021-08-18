#%%
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype, is_string_dtype
import re

#%%
# The nutrition should be pandas Series object, the Series' index is name of nutrion and value is content of nutrition for 100g of ingredient.
class Ingredient:
    __catalog = {}
    def __init__(self, name, nutrition, category = None):
        self.name = name
        self.category = category
        assert type(nutrition) == dict, 'nutrition should be dictionary'
        for dtype in set([type(i) for i in nutrition.values()]):
            assert is_numeric_dtype(dtype), 'The values of nutrition dictionary should be numeric'
        for dtype in set([type(i) for i in nutrition.keys()]):
            assert is_string_dtype(dtype), 'The keys of nutrition dictionary should be names of nutritions'
        self.nutrition = nutrition
        Ingredient.__catalog[self.name] = self
    
    def __del__(self):
        del Ingredient.__catalog[self.name]

    def __repr__(self):
        return "'" + self.name + "'"

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    '''
    def add_name(self, additional_name):
        assert additional_name == re.sub('[^0-9a-zA-Zㄱ-힗]', '', additional_name), 'It is invalid name'
        globals()[additional_name] = self
    '''
    @classmethod
    def export_catalog(cls):
        coppied = cls.__catalog
        return coppied

#%%
# The ingredients of food should be dictionary, the keys of dictionary is Ingredient object and values is amount of ingredient for one-time serve.
class Food:
    __catalog = {}
    def __init__(self, name, ingredients, category = None, note = None):
        self.name = name
        self.category = category
        self.note = note
        assert type(ingredients) == dict, 'The ingredients should be dictionary'
        assert set(type(k) for k in ingredients.keys()) == {Ingredient}, 'The keys of ingredients should be Ingredient object'
        assert is_numeric_dtype(pd.Series(list(ingredients.values()))), 'The value of ingredients should numeric'
        self.ingredients = ingredients
        self.calculate_nutrition()
        Food.__catalog[self.name] = self
    
    def __del__(self):
        del Food.__catalog[self.name]
                
    def __repr__(self):
        return "'" + self.name + "'"

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

    def calculate_nutrition(self):
        temp_nutrition = pd.Series(dtype = 'float64')
        for ingredient, amount in self.ingredients.items():
            temp_nutrition = pd.concat([temp_nutrition, pd.Series(ingredient.nutrition) * amount / 100])
        self.nutrition = {}
        for nutrition_name in temp_nutrition.index.drop_duplicates():
            self.nutrition[nutrition_name] = temp_nutrition.loc[nutrition_name].sum()
    
    '''
    def add_name(self, additional_name):
        assert additional_name == re.sub('[^0-9a-zA-Zㄱ-힗]', '', additional_name), 'It is invalid name'
        globals()[additional_name] = self
    '''
    @classmethod
    def export_catalog(cls):
        coppied = cls.__catalog
        return coppied

#%%
class Diet:
    def __init__(self, plan):
        assert type(plan) == dict, 'The values of diet plan should be Dictionary'
        for v in plan.values():
            assert set(type(k) for k in v) == {Food}, 'The values of diet plan dictionary should be List of Food object'
        assert len(set([len(v) for v in plan.values()])) == 1, "All food lists must have same length. Try using 'empty_food' to extend short food list"
        self.plan_length = [len(v) for v in plan.values()][0]
        self.plan = plan
        self.calculate_nutrition()
        self.collect_ingredient()
    
    def __repr__(self):
        return "The diet of " + str(len(self.plan)) + "day(s) and each diet consist with " + str(self.plan_length) + "dish(es)"
    
    def calculate_nutrition(self):
        temp_table = pd.DataFrame(dtype = 'float64')
        for date, food_list in self.plan.items():
            menu_nutrition = pd.Series(dtype = 'float64')
            temp_nutrition = pd.Series(dtype = 'float64')
            for food in food_list:
                temp_nutrition = pd.concat([temp_nutrition, pd.Series(food.nutrition)])
                for nutrition_name in temp_nutrition.index.drop_duplicates():
                    menu_nutrition[nutrition_name] = temp_nutrition.loc[nutrition_name].sum()
            for col in menu_nutrition.keys():
                if col not in temp_table.columns:
                    temp_table[col] = np.nan
            temp_table.loc[date] = menu_nutrition
        temp_table.fillna(0, inplace = True)
        self.nutrition = temp_table.to_dict('index')

    def collect_ingredient(self):
        ingredients_all = {}
        for idx in self.plan.keys():
            ing_list = []
            for food in self.plan[idx]:
                for food_key in food.ingredients.keys():
                    ing_list.append(food_key)
            ingredients_all[idx] = list(set(ing_list))
        self.ingredient = ingredients_all

    def menu_category(self):
        category_df = pd.DataFrame(columns = range(self.plan_length), index = self.plan.keys())
        for idx in self.plan.keys():
            category_df.loc[idx] = [v.category for v in self.plan[idx]]
        return category_df

    def menu_note(self):
        note_df = pd.DataFrame(columns = range(self.plan_length), index = self.plan.keys())
        for idx in self.plan.keys():
            note_df.loc[idx] = [v.note for v in self.plan[idx]]
        return note_df

#%%
empty_food = Food(name = 'empty', ingredients = {Ingredient(name = 'empty', nutrition = {"" : 0}) : 0})
# %%
