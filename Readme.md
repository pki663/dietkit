# Pydiet (working title)
PyDiet is a library that provides tools for managing and analyzing diets.

## Class Structure
This library includes three classes to represent diet: Ingredient, Menu and Diet.  
Ingredient class stands for grocery ingredients. Each Ingredient instance includes nutrition information.  
Menu class stands for dishes served in diet. Each Menu instance contains its own ingredients.  
Diet class stands for diet plan. It is not single diet, but bundle of several diets. It is consist with pair of identifier and contents of diet.  
  
Also, Pydiet contains class 'Criteria' which stands for nutrition criteria. It is used as input to the evaluation method to evaluate nutrition of the menu or diet.

## Functions
Pydiet's function is divided into three main functions: Loader, Evaluator and Visualizer.  
Loader functions load ingredient, menu or diet data. If the specific file path is not passed, it automatically loads the our sample data.  
Evaluator functions evaluate the menu or diet in terms of ingredients and nutrition based on user's criteria.
Visualizer functions graphically visualize the diet's information or evaluation results.

## Dependencis
 * pandas
 * matplotlib
 * seaborn
 * Will be detailed soon...

## Installation
This will soon be available for installation using pip.

## About sample data
The sample ingredient data were extracted from the 9th revision of the National Standard Food Components provided by Rural Development Administration of Korean government.  
The sample menu data is collected from Center for Children's Foodservice Management in Republic of Korea.  
The sample diet data is work of our research.  
You can find detailed information about sample data in the study: 'PyDiet: A menu-sequence diet dataset for diet planning'(link will be added).

## License
The source code for pydiet is subject to the BSD license.  
However, the sample data provided by pydiet is distributed according to CC BY-NC-SA.