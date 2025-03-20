#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
py.init_notebook_mode(connected=True)
sns.set(style="white", color_codes=True)

import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px  

def get_column_names(data):
    """ This function will be used to extract the column names for numerical and categorical variables
    info from the dataset
    input: dataframe containing all variables
    output: num_vars-> list of numerical columns
            cat_vars -> list of categorical columns"""
        
    num_var = data.select_dtypes(include=['int', 'float']).columns
    print()
    print('Numerical variables are:\n', num_var)
    print('-------------------------------------------------')

    categ_var = data.select_dtypes(include=['category', 'object']).columns
    print('Categorical variables are:\n', categ_var)
    print('-------------------------------------------------') 
    return num_var,categ_var
    
    
def percentage_null_values(data):
    """
    Function that calculates the percentage of missing values in every column of your dataset
    input: data --> dataframe
    """
    null_perc = round(data.isnull().sum() / data.shape[0],3) * 100.00
    null_perc = pd.DataFrame(null_perc, columns=['Percentage_NaN'])
    null_perc= null_perc.sort_values(by = ['Percentage_NaN'], ascending = False)
    return null_perc


# In[26]:


def select_threshold(data, thr):
    """
    Function that  calculates the percentage of missing values in every column of your dataset
    input: data --> dataframe
    
    """
    null_perc = percentage_nullValues(data)
      
    col_keep = null_perc[null_perc['Percentage_NaN'] < thr]
    col_keep = list(col_keep.index)
    print('Columns to keep:',len(col_keep))
    print('Those columns have a percentage of NaN less than', str(thr), ':')
    print(col_keep)
    data_c= data[col_keep]
    
    return data_c


# In[33]:


def fill_na(data):
    """
    Function to fill NaN with mode (categorical variabls) and mean (numerical variables)
    input: data -> df
    """
    for column in data:
        if data[column].dtype != 'object':
            data[column] = data[column].fillna(data[column].mean())  
        else:
            data[column] = data[column].fillna(data[column].mode()[0]) 
    print('Number of missing values on your dataset are')
    print()
    print(data.isnull().sum())
    return data


# In[2]:

def OutLiersBox(df,nameOfFeature):
    """
    Function to create a BoxPlot and visualise:
    - All Points in the Variable
    - Suspected Outliers in the variable

    """
    trace0 = go.Box(
        y = df[nameOfFeature],
        name = "All Points",
        jitter = 0.3,
        pointpos = -1.8,
        boxpoints = 'all', #define that we want to plot all points
        marker = dict(
            color = 'rgb(7,40,89)'),
        line = dict(
            color = 'rgb(7,40,89)')
    )

    
    trace1 = go.Box(
        y = df[nameOfFeature],
        name = "Suspected Outliers",
        boxpoints = 'suspectedoutliers', # define the suspected Outliers
        marker = dict(
            color = 'rgba(219, 64, 82, 0.6)',
            #outliercolor = 'rgba(219, 64, 82, 0.6)',
            line = dict(
                outlierwidth = 2)),
        line = dict(
            color = 'rgb(8,81,156)')
    )


    data = [trace0,trace1]

    layout = go.Layout(
        title = "{} Outliers".format(nameOfFeature)
    )

    fig = go.Figure(data=data,layout=layout)
    fig.show()
    #fig.write_html("{}_file.html".format(nameOfFeature))

# In[3]:


def corrCoef(data):
    """
    Function aimed to calculate the corrCoef between each pair of variables
    
    input: data->dataframe        
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    num_vars, categ_var = get_column_names(data)
    data_num = data[num_var]
    data_corr = data_num.corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(data_corr,
                xticklabels = data_corr.columns.values,
               yticklabels = data_corr.columns.values,
               annot = True, vmax=1, vmin=-1, center=0, cmap= sns.color_palette("RdBu_r", 7))


# In[4]:

def corrCoef_Threshold(df):
    mask = np.triu(np.ones_like(df.corr(), dtype=bool))

    # Draw the heatmap
    sns.heatmap(df.corr(), annot=True, mask = mask, vmax=1,vmin=-1,
                cmap=sns.color_palette("RdBu_r", 7));


def outlier_treatment(df, colname):
    """
    Function that drops the Outliers based on the IQR upper and lower boundaries 
    input: df --> dataframe
           colname --> str, name of the column
    
    """
    
    # Calculate the percentiles and the IQR
    Q1,Q3 = np.percentile(df[colname], [25,75])
    IQR = Q3 - Q1
    
    # Calculate the upper and lower limit
    lower_limit = Q1 - (1.5 * IQR)
    upper_limit = Q3 + (1.5 * IQR)
    
    # Drop the suspected outliers
    df_clean = df[(df[colname] > lower_limit) & (df[colname] < upper_limit)]
    
    print('Shape of the raw data:', df.shape)
    print('..................')
    print('Shape of the cleaned data:', df_clean.shape)
    return df_clean
       
    
def outliers_loop(df_num):
    """
    jsklfjfl
    
    """
    for item in np.arange(0,len(df_num.columns)):
        if item == 0:
            df_c = outlier_treatment(df_num, df_num.columns[item])
        else:
            df_c = outlier_treatment(df_c, df_num.columns[item]) 
    return df_c         


