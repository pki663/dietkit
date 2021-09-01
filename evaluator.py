from .elements import Ingredient, Menu, Diet
import pandas as pd
from os.path import dirname
from pandas.api.types import is_numeric_dtype

class Criterion:
    """
    Criterion class represent nutrition criterion. This is used as input to the evaluation method to evaluate nutrition of the menu or diet. 
    Instance Variables:
        on: What nutrients does this criterion limit? It should be string value.
        value: What is the limit value? It should be numeric value.
        condition: What is pass condition of criterion? It is one of '>', '<', '<=', '>='.
            '<=': Pass if (amount of nutrition) <= (criterion's value)
            '>=': Pass if (amount of nutrition) >= (criterion's value)
            '<': Pass if (amount of nutrition) < (criterion's value)
            '>': Pass if (amount of nutrition) > (criterion's value)
    """
    def __init__(self, on, condition, value):
        assert condition in ['>', '<', '<=', '>='], "The condition should one of '>', '<', '<=', '>='"
        assert is_numeric_dtype(type(value)), "The value should numeric"
        self.condition = condition
        self.value = value
        self.on = on
    
    def __repr__(self):
        return 'The criterion determine (' + self.on + ' ' + self.condition + ' ' + str(self.value) + ')'

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
    if type(criteria) == Criterion:
        criteria = [criteria]
    elif (type(criteria) == list):
        if not set(type(k) for k in criteria) == {Criterion}:
            raise TypeError( 'The criteria should be Criterion object or list of Criterion object')
    assert type(menu) == Menu, 'The menu should be Menu object'
    result = pd.Series(index = [repr(i) for i in criteria])
    for criterion in criteria:
        if criterion.condition == '>=':
            result.loc[repr(criterion)] = menu.nutrition[criterion.on] >= criterion.value
        elif criterion.condition == '<=':
            result.loc[repr(criterion)] = menu.nutrition[criterion.on] <= criterion.value
        elif criterion.condition == '>':
            result.loc[repr(criterion)] = menu.nutrition[criterion.on] > criterion.value
        elif criterion.condition == '<':
            result.loc[repr(criterion)] = menu.nutrition[criterion.on] < criterion.value
    return bool(result.min())

def diet_test_nutrition(diet, criteria):
    """
    Test diet's nutrition with Criteria instance. This function apply criteria to each menu list of the diet's plan.
    It returns dictionary. The key is same of diet's plan (identifier of diet). The value is boolean if the plan's food list pass criteria.
    """
    if type(criteria) == Criterion:
        criteria = [criteria]
    elif (type(criteria) == list):
        if not set(type(k) for k in criteria) == {Criterion}:
            raise TypeError( 'The criteria should be Criterion object or list of Criterion object')
    assert type(diet) == Diet, 'The diet should be Diet object'
    result = pd.DataFrame(index = [repr(i) for i in criteria], columns = diet.nutrition.keys())
    for date in diet.nutrition.keys():
        for criterion in criteria:
            if criterion.condition == '>=':
                temp_result = diet.nutrition[date][criterion.on] >= criterion.value           
            elif criterion.condition == '<=':
                temp_result = diet.nutrition[date][criterion.on] <= criterion.value 
            elif criterion.condition == '>':
                temp_result = diet.nutrition[date][criterion.on] > criterion.value
            elif criterion.condition == '<':
                temp_result = diet.nutrition[date][criterion.on] < criterion.value
            result.loc[repr(criterion), date] = temp_result

    return result.min(axis = 0).astype(bool).to_dict()

def menu_test_ingredient(menu, ingredients):
    """
    Test the menu includes input ingredients. If the menu includes, function returns True. Otherwise, False.
    """
    if type(ingredients) == Ingredient:
        ingredients = [ingredients]
    elif (type(ingredients) == list):
        if not set(type(k) for k in ingredients) == {Ingredient}:
            raise TypeError('The ingredients should be Ingredient object or list of Ingredient object')
    assert type(menu) == Menu, 'The menu should be Menu object'
    result = pd.Series(index = [i.name for i in ingredients])
    for ing in ingredients:
        if ing in menu.ingredients.keys():
            result.loc[ing.name] = True
        else:
            result.loc[ing.name] = False
    return bool(result.min())

def diet_test_ingredient(diet, ingredients):
    """
    Test the diet includes input ingredient. This function apply test to each menu list of the diet's plan.
    It returns dictionary. The key is same of diet's plan (identifier of diet). The value is boolean if the plan's food list pass test.
    """
    if type(ingredients) == Ingredient:
        ingredients = [ingredients]
    elif (type(ingredients) == list):
        if not set(type(k) for k in ingredients) == {Ingredient}:
            raise TypeError('The ingredients should be Ingredient object or list of Ingredient object')
    assert type(diet) == Diet, 'The diet should be Diet object'
    result = pd.DataFrame(index = [i.name for i in ingredients], columns = diet.ingredient.keys())
    for date in diet.nutrition.keys():
        for ing in ingredients:
            result.loc[ing.name, date] = ing in diet.ingredient[date]

    return result.min(axis = 0).astype(bool).to_dict()