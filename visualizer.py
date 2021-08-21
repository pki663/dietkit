import pandas as pd
from .elements import Ingredient, Diet
from .evaluator import diet_test_nutrition, diet_test_ingredient, Criterion
import matplotlib.pyplot as plt
import seaborn as sns

# %%
def bar_menu_test_nutrition(diet, criterias, fig_path):
    """
    Plot bar graph. The graph shows ratio of diet plan that passed input nutrition criterias.
    X-axis is applied criteria. Y-axis is ratio of passed diet plan.
    The graph is saved to fig_path.
    """
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(criterias) == list, 'The criterias should be list of Criteria object'
    assert set(type(k) for k in criterias) == {Criterion}, 'The criterias should be list of Criteria object'
    result_table = pd.DataFrame()
    for criteria in criterias:
        result_table[criteria.on + criteria.condition + str(criteria.value)] = pd.Series(diet_test_nutrition(diet, criteria)).value_counts()
    result_table.transpose().plot(kind='bar', stacked = True).get_figure().savefig(fig_path)

#%%
def bar_menu_test_ingredient(diet, ingredients, fig_path):
    """
    Plot bar graph. The graph shows ratio of diet plan that includes input ingredient.
    X-axis is applied criteria. Y-axis is ratio of passed diet plan.
    The graph is saved to fig_path.
    """
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredients) == list, 'The ingredients should be list of Ingredient object'
    assert set(type(k) for k in ingredients) == {Ingredient}, 'The ingredients should be list of Ingredient object'
    result_table = pd.DataFrame()
    for ingredient in ingredients:
        result_table[ingredient.name] = pd.Series(diet_test_ingredient(diet, ingredient)).value_counts()
    result_table.transpose().plot(kind='bar', stacked = True).get_figure().savefig(fig_path)

# %%
def heatmap_menu_test_nutrition(diet, criterias, fig_path):
    """
    Plot heatmap. The heatmap shows which diet pass input nutrition criteria.
    X-axis is applied criteria. Y-axis is identifier of diet (key of diet's plan dictionary).
    Bright cell means the diet pass criteria. Dark cell means the diet failed to pass.
    The graph is saved to fig_path.
    """
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(criterias) == list, 'The criterias should be list of Criteria object'
    assert set(type(k) for k in criterias) == {Criterion}, 'The criterias should be list of Criteria object'
    result_table = pd.DataFrame()
    for criteria in criterias:
        result_table[criteria.on + criteria.condition + str(criteria.value)] = pd.Series(diet_test_nutrition(diet, criteria))
    ax = sns.heatmap(result_table)
    plt.savefig(fig_path)
# %%
def heatmap_menu_test_ingredient(diet, ingredients, fig_path):
    """
    Plot heatmap. The heatmap shows which diet includes input ingredients.
    X-axis is test ingredient. Y-axis is identifier of diet (key of diet's plan dictionary).
    Bright cell means the diet includes the ingredient. Dark cell means the diet doesn't include it.
    The graph is saved to fig_path.
    """
    assert type(diet) == Diet, 'The diet should be Diet object'
    assert type(ingredients) == list, 'The ingredients should be list of Ingredient object'
    assert set(type(k) for k in ingredients) == {Ingredient}, 'The ingredients should be list of Ingredient object'
    result_table = pd.DataFrame()
    for ingredient in ingredients:
        result_table[ingredient.name] = pd.Series(diet_test_ingredient(diet, ingredient))
    ax = sns.heatmap(result_table)
    plt.savefig(fig_path)

#%%
def diet_ingredient_freq(diet, fig_path, sortby = 'frequency', plot_ratio = 0.1):
    """
    This function graphically show how many times each ingredient has been used in the entire diet. If it was used several times in a menu list, count to 1.
    plot_ratio indicates ratio of will be displayed ingredients among the entire ingredients of entire diet plan. If entire diet include 100 kinds of ingredients and plot_ratio is 0.1, than the graph shows 100 * 0.1 = 10 ingredients. The default value of plot_ratio is 0.1.
    sortby indicates how to sort the ingredients. This is either 'frequency'(default) or 'name'. If sortby is 'frequency', plotting the frequently used ingredients first. If sortby is 'name', plot the fastest ingredients in alphabetical order first.
    """
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