#%%
import pandas as pd
from .elements import Ingredient, Diet
from .evaluation import diet_test_nutrition, diet_test_ingredient, Criteria
import matplotlib.pyplot as plt
import seaborn as sns

# %%
def bar_menu_test_nutrition(diet, criterias, fig_path):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(criterias) == list, 'The criterias should be list of Criteria object'
    assert set(type(k) for k in criterias) == {Criteria}, 'The criterias should be list of Criteria object'
    result_table = pd.DataFrame()
    for criteria in criterias:
        result_table['crit_' + str(criterias.index(criteria) + 1)] = pd.Series(diet_test_nutrition(diet, criteria)).value_counts()
    result_table.transpose().plot(kind='bar', stacked = True, figsize=(20, 10), fontsize=15).get_figure().savefig(fig_path)

#%%
def bar_menu_test_ingredient(diet, ingredients, fig_path):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredients) == list, 'The ingredients should be list of Ingredient object'
    assert set(type(k) for k in ingredients) == {Ingredient}, 'The ingredients should be list of Ingredient object'
    result_table = pd.DataFrame()
    for ingredient in ingredients:
        result_table[ingredient.name] = pd.Series(diet_test_ingredient(diet, ingredient)).value_counts()
    result_table.transpose().plot(kind='bar', stacked = True, figsize=(20, 10), fontsize=15).get_figure().savefig(fig_path)

# %%
def heatmap_menu_test_nutrition(diet, criterias, fig_path):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(criterias) == list, 'The criterias should be list of Criteria object'
    assert set(type(k) for k in criterias) == {Criteria}, 'The criterias should be list of Criteria object'
    result_table = pd.DataFrame()
    for criteria in criterias:
        result_table[criteria.condition + criteria.on] = pd.Series(diet_test_nutrition(diet, criteria))
    ax = sns.heatmap(result_table)
    plt.savefig(fig_path)
# %%
def heatmap_menu_test_ingredient(diet, ingredients, fig_path):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredients) == list, 'The ingredients should be list of Ingredient object'
    assert set(type(k) for k in ingredients) == {Ingredient}, 'The ingredients should be list of Ingredient object'
    result_table = pd.DataFrame()
    for ingredient in ingredients:
        result_table[ingredient.name] = pd.Series(diet_test_ingredient(diet, ingredient))
    ax = sns.heatmap(result_table)
    plt.savefig(fig_path)

#%%
def diet_ingredient_freq(diet, fig_path, sortby = 'name', plot_ratio = 0.1):
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert sortby in ['name', 'frequency'], 'The sortby should "name" or "frequency"'
    all_ing = []
    for date in diet.ingredient.keys():
        all_ing.extend([ing.name for ing in diet.ingredient[date]])
    if sortby == 'name':
        plot_series = pd.Series(all_ing).value_counts().sort_index()
    elif sortby == 'frequency':
        plot_series = pd.Series(all_ing).value_counts().sort_values()
    plot_num = round(len(plot_series) * plot_ratio)
    plot_series.iloc[:plot_num].plot(kind = 'bar', figsize=(20, 10), fontsize=15).get_figure().savefig(fig_path)