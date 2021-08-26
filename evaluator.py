from .elements import Ingredient, Menu, Diet
import pandas as pd
from os.path import dirname
from pandas.api.types import is_numeric_dtype, is_string_dtype

class Criterion:
    """
    Criteria class represent nutrition criteria. This is used as input to the evaluation method to evaluate nutrition of the menu or diet. 
    Instance Variables:
        on: What nutrients does this criteria limit? It should be string value.
        value: What is the limit value? It should be numeric value.
        condition: What is pass condition of criteria? It is one of '>', '<', '<=', '>='.
            '<=': Pass if (amount of nutrition) <= (criteria's value)
            '>=': Pass if (amount of nutrition) >= (criteria's value)
            '<': Pass if (amount of nutrition) < (criteria's value)
            '>': Pass if (amount of nutrition) > (criteria's value)
    """
    def __init__(self, on, condition, value):
        assert condition in ['>', '<', '<=', '>='], "The condition should one of '>', '<', '<=', '>='"
        assert is_numeric_dtype(value), "The value should numeric"
        self.condition = condition
        self.value = value
        self.on = on
    
    def __repr__(self):
        return 'The criteria determine (' + self.on + ' ' + self.condition + ' ' + str(self.value) + ')'

def load_sample_criteria(sample_name = 'korean_standard_criteria'):
    """
    Load sample criteria from file. The sample criteria is Korean standard nutrition criteria.
    """
    standard_table = pd.read_csv(dirname(__file__) + '/samples/' + sample_name + '.csv', index_col = None)
    standard_table['value'] = pd.to_numeric(standard_table['value'])
    criteria_list = []
    for idx in standard_table.index:
        criteria_list.append(Criterion(on = standard_table.loc[idx, 'on'], condition = standard_table.loc[idx, 'condition'], value = standard_table.loc[idx, 'value']))
    return criteria_list

def menu_test_nutrition(menu, criteria):
    """
    Test menu's nutrition with Criteria instance. If menu pass criteria, it returns True. Otherwise, False.
    """
    assert type(criteria) == Criterion, 'The criteria should be Criteria object'
    assert type(menu) == Menu, 'The menu should be Menu object'
    if criteria.condition == '>=':
        return menu.nutrition[criteria.on] >= criteria.value
    elif criteria.condition == '<=':
        return menu.nutrition[criteria.on] <= criteria.value
    elif criteria.condition == '>':
        return menu.nutrition[criteria.on] > criteria.value
    elif criteria.condition == '<':
        return menu.nutrition[criteria.on] < criteria.value

def diet_test_nutrition(diet, criteria):
    """
    Test diet's nutrition with Criteria instance. This function apply criteria to each menu list of the diet's plan.
    It returns dictionary. The key is same of diet's plan (identifier of diet). The value is boolean if the plan's food list pass criteria.
    """
    assert type(criteria) == Criterion, 'The criteria should be Criteria object'
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

def menu_test_ingredient(menu, ingredient):
    """
    Test the menu includes input ingredient. If the menu includes, function returns True. Otherwise, False.
    """
    assert type(menu) == Menu, 'The menu should be Menu object'
    assert type(ingredient) == Ingredient, 'The ingredient should be Ingredient object'
    if ingredient in menu.ingredients.keys():
        return True
    else:
        return False

def diet_test_ingredient(diet, ingredient):
    """
    Test the diet includes input ingredient. This function apply test to each menu list of the diet's plan.
    It returns dictionary. The key is same of diet's plan (identifier of diet). The value is boolean if the plan's food list pass test.
    """
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredient) == Ingredient, 'The ingredient should be Ingredient object'
    eval_result = {}
    for date in diet.ingredient.keys():
        eval_result[date] = ingredient in diet.ingredient[date]
    return eval_result