import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype, is_string_dtype

class Ingredient:
    """
    Ingredient class represent grocery ingredient which make up dishes. The class consists with name, category and nutrition.
    Instance Variables:
        name: name is string variable which stand for name of the ingredient's name. For example, Tomato or Spinach might be name. It is essential variable.
        category: category is string variable which stand for the category to which the ingredient belongs. For example, Grain or Meat might be category. It is optional variable.
        nutrition: nutrition is dictionary variable which stands for nutritions contained in the 100g of ingredient. The keys of nutrition is name of nutrition (string) and values of nutrition is amount of key nutrition (numeric). For example, {'Carbohydrate' : 150} might be item of nutrition. It is essential variable.
    Class Variable:
        __catalog: catalog is dictionary variable which point generated Ingredient instances. The keys of catalog is name variable of instance (string) and values are instance (Ingredient). So, you can access to instance by catalog['(name of ingredient)']. However for stability reason, you can not directly access to class catalog. You can get copy of catalog by class function, 'Ingredient.export_catalog()'
    """
    __catalog = {}
    def __init__(self, name, nutrition, category = None):
        """
        The constructor of Ingredient instance. If construction successfully completes successfully, add the instance to the class catalog with the key as name.
        name and nutrition of instance should input. category is optional.
        """
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
        """
        The destructor of Ingredient instance. It delete the instance from class catalog.
        """
        del Ingredient.__catalog[self.name]

    def __repr__(self):
        return "Ingredient object: " + self.name

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
        """
        It return copy of class catalog. Using the catalog, you can access to instance by its name. 'catalog['(name of instance)']'
        """
        return cls.__catalog

class Menu:
    """
    Menu class represent dish which make up diets. The class consists with name, category, ingredients and nutrition.
    Instance Variables:
        name: name is string variable which stand for name of the menu's name. For example, Fruit salad or Beef stew might be name. It is essential variable.
        category: category is string variable which stand for the category to which the menu belongs. For example, salad or soup might be category. It is optional variable.
        ingredients: 'ingredients' is dictionary variable which stand for ingredients contained in the one-time provision of menu. The keys of ingredient is ingredient instance which belongs to menu and the value of ingredient is amount of key ingredient (numeric). It is essential variable.
        note: note is string variable. It is additional information about menu. For example, 'It has spicy flavor' can be note. It is optional variable.
        nutrition: nutrition is dictionary variable which stands for nutritions contained in the one-time provision of menu. The keys of nutrition is name of nutrition (string) and values of nutrition is amount of key nutrition (numeric). For example, {'Carbohydrate' : 150} might be item of nutrition. nutrition is calculated automatically from the ingredient variable. So you don't have to input nutrition of menu to generate instance.
    Class Variable:
        __catalog: catalog is dictionary variable which point generated Menu instances. The keys of catalog is name variable of instance (string) and values are instance (Menu). So, you can access to instance by catalog['(name of menu)']. However for stability reason, you can not directly access to class catalog. You can get copy of catalog by class function, 'Menu.export_catalog()'
    """
    __catalog = {}
    def __init__(self, name, ingredients, category = None, note = None):
        """
        The constructor of Menu instance. If construction successfully completes successfully, add the instance to the class catalog with the key as name.
        name and ingredients variable of instance should input. category and note are optional. nutritions variable is automatically computed.
        """
        self.name = name
        self.category = category
        self.note = note
        assert type(ingredients) == dict, 'The ingredients should be dictionary'
        assert set(type(k) for k in ingredients.keys()) == {Ingredient}, 'The keys of ingredients should be Ingredient object'
        assert is_numeric_dtype(pd.Series(list(ingredients.values()))), 'The value of ingredients should numeric'
        self.ingredients = ingredients
        self.__calculate_nutrition()
        Menu.__catalog[self.name] = self
    
    def __del__(self):
        """
        The destructor of Menu instance. It delete the instance from class catalog.
        """
        del Menu.__catalog[self.name]
                
    def __repr__(self):
        return "Menu object: " + self.name

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

    def __calculate_nutrition(self):
        """
        Make nutritions variable of instance from its ingredients variable. For stable operation, this method cannot be executed alone.
        """
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
        """
        It return copy of class catalog. Using the catalog, you can access to instance by its name. 'catalog['(name of instance)']'
        """
        coppied = cls.__catalog
        return coppied

class Diet:
    """
    Diet class represent plan of diets. The class consists with plan, plan length, ingredient and nutrition.
    Instance Variables:
        plan: plan is dictionary variable which stand for menu composition of diets. The keys of plan is identifier of diet. It can be serial number, sting nickname or date. The values of plan is list of Menu instances. This list is menu composition of the diet. For example {'2021-08-01' : ['Fruit salad', 'Potato soup', 'White bread' ...]} can be item of plan.
        plan_length: plan length is positive integer value which means the length of plan values, the lists of Menu instances. So, all diets should consists of the same number of menus. If this is not satisfied, the constructor will raise error. If you have diet plan which has the lists of different numbers of menus. Try to use 'empty_menu', the dummy menu instance that the our package provides. It is automatically recognized without user input.
        ingredients: 'ingredients' is double dictionary variable which stands for ingredients contained in each menu plan. The keys are identifier of diet. It is same of plan's one. The value of nutirition is again dictioinaty. The keys of inner dictionary is Ingredient instance and value is amount of key ingredient (numeric). This is for the whold of diet. For example, {'2021-08-01' : {'Tomato' : 50, ...}} can be item of ingredients. It is calculated automatically from the menu list of plan. So you don't have to input ingredients of diet to generate instance.
        nutritions: 'nutritions' is double dictionary variable which stands for nutritions contained in each menu plan. The keys are identifier of diet. It is same of plan's one. The value of nutirition is again dictioinaty. The keys of inner dictionary is name of nutrition (string) and value is amount of key nutrition (numeric). This is for the whold of diet. For example, {'2021-08-01' : {'Carbohydrate' : 900, ...}} can be item of nutrition. It is calculated automatically from the menu list of plan. So you don't have to input nutrition of diet to generate instance.
    """
    def __init__(self, plan):
        """
        The constructor of Diet instance.
        plan should input. nutritions and ingredients are automatically computed.
        """
        assert type(plan) == dict, 'The values of diet plan should be Dictionary'
        for v in plan.values():
            assert set(type(k) for k in v) == {Menu}, 'The values of diet plan dictionary should be List of Menu object'
        assert len(set([len(v) for v in plan.values()])) == 1, "All menu lists must have same length. Try using 'empty_menu' to extend short menu list"
        self.plan_length = [len(v) for v in plan.values()][0]
        self.plan = plan
        self.__calculate_nutrition()
        self.__collect_ingredient()
    
    def __repr__(self):
        return "The diet object of " + str(len(self.plan)) + "day(s) and each diet consist with " + str(self.plan_length) + "dish(es)"
    
    def __calculate_nutrition(self):
        """
        Make nutritions variable of instance from its plan variable. For stable operation, this method cannot be executed alone.
        """
        temp_table = pd.DataFrame(dtype = 'float64')
        for date, menu_list in self.plan.items():
            menu_nutrition = pd.Series(dtype = 'float64')
            temp_nutrition = pd.Series(dtype = 'float64')
            for menu in menu_list:
                temp_nutrition = pd.concat([temp_nutrition, pd.Series(menu.nutrition)])
                for nutrition_name in temp_nutrition.index.drop_duplicates():
                    menu_nutrition[nutrition_name] = temp_nutrition.loc[nutrition_name].sum()
            for col in menu_nutrition.keys():
                if col not in temp_table.columns:
                    temp_table[col] = np.nan
            temp_table.loc[date] = menu_nutrition
        temp_table.fillna(0, inplace = True)
        self.nutrition = temp_table.to_dict('index')

    def __collect_ingredient(self):
        """
        Make ingredients variable of instance from its plan variable. For stable operation, this method cannot be executed alone.
        """
        ingredients_all = {}
        for idx in self.plan.keys():
            ing_list = []
            for menu in self.plan[idx]:
                for menu_key in menu.ingredients.keys():
                    ing_list.append(menu_key)
            ingredients_all[idx] = list(set(ing_list))
        self.ingredient = ingredients_all

    def menu_category(self):
        """
        The method which return dataframe which have category data of menus. The index are key of plan (identifier of diet).
        """
        category_df = pd.DataFrame(columns = range(self.plan_length), index = self.plan.keys())
        for idx in self.plan.keys():
            category_df.loc[idx] = [v.category for v in self.plan[idx]]
        return category_df

    def menu_note(self):
        """
        The method which return dataframe which have note data of menus. The index are key of plan (identifier of diet).
        """
        note_df = pd.DataFrame(columns = range(self.plan_length), index = self.plan.keys())
        for idx in self.plan.keys():
            note_df.loc[idx] = [v.note for v in self.plan[idx]]
        return note_df

# The dummy menu instance to fill diet's short plan list.
empty_menu = Menu(name = 'empty', ingredients = {Ingredient(name = 'empty', nutrition = {"" : 0}) : 0})