import pandas as pd
from .elements import Ingredient, Menu, Diet
from os.path import dirname

def load_ingredient(file_path = None, sample_language = 'eng'):
    """
    Load ingredient data. If file_path is not passed, method loads sample data. It return instance dictinary of loaded data, which has key: name of ingredient and value: ingredient instance. 
    """
    if file_path == None:
        sample_language = sample_language.lower()
        if sample_language == 'eng':
            file_path = dirname(__file__) + '/samples/sample_ingredients_eng.csv'
        elif sample_language == 'kor':
            file_path = dirname(__file__) + '/samples/sample_ingredients_kor.csv'
        else:
            raise NameError("The available sample_language is 'kor' or 'eng'")

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

def load_menu(ingredients = load_ingredient(), file_path = None, sample_language = 'eng'):
    """
    Load menu data. If file_path is not passed, method loads sample data. It return instance dictinary of loaded data, which has key: name of menu and value: menu instance.
    """
    sample_language = sample_language.lower()
    if file_path == None:
        if sample_language == 'eng':
            file_path = dirname(__file__) + '/samples/sample_menus_eng.csv'
        elif sample_language == 'kor':
            file_path = dirname(__file__) + '/samples/sample_menus_kor.csv'
        else:
            raise NameError("The available sample_language is 'kor' or 'eng'")
    
    raw_df = pd.read_csv(file_path, encoding = 'cp949', index_col = None)
    raw_ingredients = pd.DataFrame(data = raw_df['weight'].values, index = pd.MultiIndex.from_frame(raw_df.fillna(method = 'ffill')[['name', 'ingredient']]), columns = ['weight'])
    info = raw_df.loc[pd.notna(raw_df['name']), ['name', 'category', 'note']].set_index('name')
    del raw_df

    sample_menus = {}
    for menu_name in info.index:
        temp_ingredients = raw_ingredients.xs(menu_name)['weight'].to_dict()
        converted_ingredients = {}
        for temp_ing in temp_ingredients.keys():
            converted_ingredients[ingredients[temp_ing]] = temp_ingredients[temp_ing]
        sample_menus[menu_name] = Menu(name = menu_name, ingredients = converted_ingredients, category = info.loc[menu_name, 'category'], note = info.loc[menu_name, 'note'])
    '''
    if add_to_global:
        for key, value in sample_menus.items():
            var_name = re.sub('[^0-9a-zA-Zㄱ-힗]', '', key)
            globals()[var_name] = value
    '''
    return sample_menus

def load_diet(menus = load_menu(), num_loads = 100, file_path = None, sample_language = 'eng', sample_name = None):
    """
    Load diet data. If file_path is not passed, method loads sample data. You can select which sample data will be loaded by specify 'sample_name' and 'sample_language'. See readme to know what sample names and languages are available.
    """

    if file_path == None:
        sample_name = sample_name.lower()
        assert sample_name in ['expert', 'or', 'ml'], "The available sample_name should be one of 'expert', 'or' and 'ml'"
        sample_language = sample_language.lower()
        assert sample_language in ['eng', 'kor'], "The available sample_language is 'kor' or 'eng'"
        file_path = dirname(__file__) + '/samples/sample_diet_' + sample_name + '_' + sample_language + '.csv'

    raw_df = pd.read_csv(file_path, encoding = 'cp949', index_col = 0).iloc[:num_loads]
    assert num_loads <= len(raw_df), "Requested a larger number of diets than the data have."
    converted_dict = {}
    for idx in raw_df.index:
        converted_menus = []
        for raw_menu in list(raw_df.loc[idx].values):
            converted_menus.append(menus[raw_menu])
        converted_dict[idx] = converted_menus
    sample_diet = Diet(converted_dict)
    return sample_diet