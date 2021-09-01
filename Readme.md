# Dietkit
Dietkit is a library that provides tools for managing and analyzing diets.  
[![DOI](https://zenodo.org/badge/396463175.svg)](https://zenodo.org/badge/latestdoi/396463175)

## Guide
We present example execution in forms of IPython notebook. It includes how to use the classes and functions of dietkit and how to analyze data using them. Therefore, it will provide useful insight about dietkit. So, we strongly recommend to read carefully our example, `sample_execution.ipynb` in root folder.

## Class Structure
This library includes three classes to represent diet: Ingredient, Menu and Diet.  
Ingredient class stands for grocery ingredients. Each Ingredient instance includes nutrition information.  
Menu class stands for dishes served in diet. Each Menu instance contains its own ingredients.  
Diet class stands for diet plan. It is not single diet, but bundle of several diets. It is consist with pair of identifier and contents of diet.  
Also, Dietkit contains class 'Criteria' which stands for nutrition criteria. It is used as input to the evaluation method to evaluate nutrition of the menu or diet.

## Functions
Dietkit's function is divided into three main functions: Loader, Evaluator and Visualizer.  
Loader functions load ingredient, menu or diet data. If the specific file path is not passed, it automatically loads the our sample data.  
Evaluator functions evaluate the menu or diet in terms of ingredients and nutrition based on user's criteria.
Visualizer functions graphically visualize the diet's information or evaluation results.

## Dependencis
 * pandas (>=3.7)
 * matplotlib (>= 3.0.0)
 * seaborn (>= 0.11.0)

## Installation
You can install this package by `pip install dietkit`

## Tip
If `from dietkit import *` is input, dietkit will import all of its functions and classes. It can take quite a long time (About 3 minutes). So, it is recommended to import only the functions to be used.

## About sample data
The sample ingredient data were extracted from the 9th revision of the National Standard Food Components provided by Rural Development Administration of Korean government.  
The sample menu data is collected from Center for Children's food service management under the Ministry of Food and Drug safety of the Korean government.  
The sample diet data is work of our research.  
You can find detailed information about sample data in the study: 'Creating the K–MIND dataset for dietplanning and healthcare research: Byintegrating the capabilities of combinatorialoptimization, experts, and controllablegeneration'.

## Related documents
This package is subject results of the research: [link TBD]  
You can check detail information about this package and its sample data in supplementary material of above research: [link TBD]

## Related repository
Here is an example of using dietkit for machine learning of diet data. This will be a helpful case for data scientists:  
<https://github.com/Leo-Lee92/Diet-Generation-As-Sequence>

## License
The source code for Dietkit is subject to the LGPL license.  
However, the sample data following another license. See readme file of 'samples' folder.
