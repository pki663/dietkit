#%%
from .elements import Ingredient, Food, Diet
import pandas as pd
from os.path import dirname
from pandas.api.types import is_numeric_dtype, is_string_dtype

#%%
class Criteria:
    def __init__(self, on, condition, value):
        assert condition in ['>', '<', '<=', '>='], "The condition should one of '>', '<', '<=', '>='"
        assert is_numeric_dtype(value), "The value should numeric"
        self.condition = condition
        self.value = value
        self.on = on
    
    def __repr__(self):
        return 'The criteria determine (' + self.on + ' ' + self.condition + ' ' + str(self.value) + ')'

#%%
def load_sample_criteria(sample_name = 'Korean_standard'):
    standard_table = pd.read_csv(dirname(__file__) + '/sample_data/' + sample_name + '.csv', index_col = None)
    standard_table['value'] = pd.to_numeric(standard_table['value'])
    criteria_list = []
    for idx in standard_table.index:
        criteria_list.append(Criteria(on = standard_table.loc[idx, 'on'], condition = standard_table.loc[idx, 'condition'], value = standard_table.loc[idx, 'value']))
    return criteria_list

#%%
def food_test_nutrition(food, criteria):
    assert type(criteria) == Criteria, 'The criteria should be Criteria object'
    assert type(food) == Food, 'The food should be Food object'
    if criteria.condition == '>=':
        return food.nutrition[criteria.on] >= criteria.value
    elif criteria.condition == '<=':
        return food.nutrition[criteria.on] <= criteria.value
    elif criteria.condition == '>':
        return food.nutrition[criteria.on] > criteria.value
    elif criteria.condition == '<':
        return food.nutrition[criteria.on] < criteria.value

#%%
def diet_test_nutrition(diet, criteria):
    assert type(criteria) == Criteria, 'The criteria should be Criteria object'
    assert type(diet) == Diet, 'The diet should be Diet object'
    eval_result = {}
    for date in diet.nutrition.keys():
        if criteria.condition == '>=':
            eval_result[date] = diet.nutrition[date][criteria.on] >= criteria.value           
        elif criteria.condition == '<=':
            eval_result[date] = diet.nutrition[date][criteria.on] <= criteria.value 
        elif criteria.condition == '>':
            eval_result[date] = diet.nutrition[date][criteria.on] > criteria.value
        elif criteria.condition == '<':
            eval_result[date] = diet.nutrition[date][criteria.on] < criteria.value
    return eval_result

#%%
# Return True if input food includes input ingredient.
def food_test_ingredient(food, ingredient):
    assert type(food) == Food, 'The food should be Food object'
    assert type(ingredient) == Ingredient, 'The ingredient should be Ingredient object'
    if ingredient in food.ingredients.keys():
        return True
    else:
        return False

#%%
# Return True if input diet includes input ingradient.
# If deep is True, 
def diet_test_ingredient(diet, ingredient):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredient) == Ingredient, 'The ingredient should be Ingredient object'
    eval_result = {}
    for date in diet.ingredient.keys():
        eval_result[date] = ingredient in diet.ingredient[date]
    return eval_result
