# -*- coding: utf-8 -*-
"""AIAS_B2_M1_MP1_NB_Credit_Card_Default_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YJkLwWqob363OOWjKR_aRzR6llCz_NwB

# Machine Learning and AI for Autonomous Systems
## A program by IISc and TalentSprint
### Mini Project: Credit Card Default Risk Analysis

## Learning Objectives

At the end of the mini project, you will be able to

* understand the application of machine learning in finacial sector
* use a real world dataset.
* compare between different types of classification methods and their pros and cons.

**Packages used:**  
* `Pandas` for data frames and easy to read csv files  
* `Numpy` for array and matrix mathematics functions  
* `Matplotlib` and `Seaborn` for visualization
*  `sklearn` for the metrics and pre-processing

### Dataset Description

The dataset chosen for this mini project is [default of credit card clients Data Set](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients) with 30000 instances each having 25 attributes.
"""

# import the libraries used for machine learning
import numpy as np
import pandas as pd
import scipy.optimize as opt

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import set_option
#from pandas_profiling import ProfileReport
plt.style.use('ggplot')

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
#from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import roc_curve

import os

"""**Exercise 1**: Load the data show the top few rows of the dataframe.  (***1 point***)"""

from google.colab import files
uploaded = files.upload()

# YOUR CODE HERE

data = data.drop(labels=0, axis=0)
# YOUR CODE HERE

"""**Exercise 2**: Perform the following

- Exploratory Data Analysis (***2 points***)
- Preprocessing (***2 points***)

## Exploratory data analysis

there are total 23 explanatory variables and one response variable. Some variable need to be converted to categories. such as.

* __Gender(X2)__
1 = Male, 2 = Female

* __EDUCATION(X3)__
1 = graduate school; 2 = university; 3 = high school; 4 = others
* __Marital status(X4)__
1 = married; 2 = single; 3 = others
* __Repayment status(X6-X11)__
   -2= no consumption, -1= pay duly, 1 = payment delay for one month, 2 = payment delay for two months, ...,8 = payment delay for eight months,9 = payment delay for nine months and above

   these variables should be converted to categorical variable
"""

# YOUR CODE HERE   # drop column "ID"
data.info()

"""### Statistics
The detail statistics of the dataset
"""

print("STATISTICS OF NUMERIC COLUMNS")
print()
print(data.describe().T)

data.X2.value_counts() # male, female counts

data.X3.value_counts() #Education categories

data.X4.value_counts() # Marriage catagories

data.X6.describe()

"""# Visualization"""

from IPython.core.pylabtools import figsize
# plot the frequency of defaults
# YOUR CODE HERE

# Plot distribution of age and limit balance
plt.subplots(figsize=(20,5))
plt.subplot(121)
# YOUR CODE HERE

plt.subplot(122)
# YOUR CODE HERE

plt.show()

#Plot the defaulter(Y), marriage(X4) vs age(X5) use seborn library


# YOUR CODE HERE

# plot the defaulter(Y), sex(X2) vs age(X5)
# YOUR CODE HERE

"""# Preprocessing"""

{'X3': 'EDU'}.items()

# write a function for onehot_encode
def onehot_encode(df, column_dict):
    df = df.copy()
# YOUR CODE HERE
    return df

def preprocess_inputs(df):
    df = df.copy()



    df = onehot_encode(
        df,
        {
            'X3': 'EDU',
            'X4': 'MAR'
        }
    )

    # Split df into X and y
    y = df['Y'].copy()
    X = df.drop('Y', axis=1).copy()

    # Scale X with a standard scaler
    # YOUR CODE HERE

    return X, y

X, y = preprocess_inputs(data)

X

y

{column: len(X[column].unique()) for column in X.columns}

"""**Exercise 3** (3 Points)

Train the model using the 4 ML models:

- Logistic Regression
- Perceptron
- SVM

## Training

Application of machine learning models, such as

### Logistic Regression
Logistic regression is named for the function used at the core of the method, the logistic function.

The logistic function, more popularly called the sigmoid function was to describe properties of population growth in ecology, rising quickly and maxing out at the carrying capacity of the environment.

It’s an S-shaped curve that can take any real-valued number and map it into a value between 0 and 1, but never exactly at those limits.

$\frac{1}{ (1 + e^{-value})}$

Where $e$ is the base of the natural logarithms and value is the actual numerical value that you want to transform. Below is a plot of the numbers between $-5$ and $5$ transformed into the range $0$ and $1$ using the logistic function.

### The Perceptron

The Perceptron is one of the simplest ANN architectures, invented in 1957 by Frank Rosenblatt. It is based on a slightly different artificial neuron (shown in the figure below) called a **threshold logic unit (TLU)**. The inputs and the output are numbers (instead of binary on/off values), and each input connection is associated with a weight. The TLU computes a weighted sum of its inputs $$(z = w_1 x_1 + w_2 x_2 + ⋯ + w_n x_n = x^⊺ w)$$, then applies a step function to that sum and outputs the result: $$h_w(x) = step(z)$$, where $z = x^⊺ w$.
<br><br>
<center>
<img src="https://www.oreilly.com/library/view/neural-networks-and/9781492037354/assets/mlst_1004.png" width= 400px/>
</center>

$\hspace{10cm} \text {Threshold logic unit}$
<br><br>
The most common step function used in Perceptrons is the Heaviside step function. Sometimes the sign function is used instead.

$$heaviside (z) = \begin{equation}
\left\{
  \begin{aligned}
    &0&  if\ \  z < 0\\
    &1&  if\ \  z \ge 0\\
  \end{aligned}
  \right.
\end{equation}
$$

$$sgn (z) = \begin{equation}
\left\{
  \begin{aligned}
    &-1&  if\ \  z < 0\\
    &0&  if\ \  z = 0\\
    &1&  if\ \  z > 0\\
  \end{aligned}
  \right.
\end{equation}
$$

A single TLU can be used for simple linear binary classification. It computes a linear combination of the inputs, and if the result exceeds a threshold, it outputs the positive class. Otherwise, it outputs the negative class.



The decision boundary of each output neuron is linear, so Perceptrons are incapable of learning complex patterns (just like Logistic Regression classifiers). However, if the training instances are linearly separable, Rosenblatt demonstrated that this algorithm would converge to a solution. This is called the Perceptron convergence theorem.

### Support Vector Machines: Maximizing the Margin

Support vector machines offer one way to improve on this. The intuition is this: rather than simply drawing a zero-width line between the classes, we can draw around each line a margin of some width, up to the nearest point. Here is an example of how this might look:

### Random Forests

A random forest is a collection of decision trees whose results are aggregated into one final result. Random Forest  is a supervised classification algorithm. There is a direct relationship between the number of trees in the forest and the results it can get: the larger the number of trees, the more accurate the result. But here creating the forest is not the same as constructing the decision tree with the information gain or gain index approach.

The difference between the Random Forest algorithm and the decision tree algorithm is that in Random Forest, the process of finding the root node and splitting the feature nodes will run randomly.
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)

# YOUR CODE HERE

"""**Exercise 4**

Evaluate the models and display the results ( 2 points)

### Model Evaluation

To evaluate the performance of a classification model, the following metrics are used:

* Confusion matrix
  * Accuracy
  * Precision
  * Recall
  * F1-Score
"""

# YOUR CODE HERE