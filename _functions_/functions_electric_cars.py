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


german_states = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
]

german_states_abbreviations = {
    "Baden-Württemberg" : "BW",
    "Bayern": "BY",
    "Berlin": "BE",
    "Brandenburg": "BB",
    "Bremen": "HB",
    "Hamburg": "HH",
    "Hessen": "HE",
    "Mecklenburg-Vorpommern": "MV",
    "Niedersachsen": "NI",
    "Nordrhein-Westfalen": "NW",
    "Rheinland-Pfalz": "RP",
    "Saarland": "SL",
    "Sachsen": "SN",
    "Sachsen-Anhalt": "ST",
    "Schleswig-Holstein": "SH",
    "Thüringen": "TH"
}
# Define the German states and their abbreviations
german_states = [
    "Baden-Württemberg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
]

german_states_colors = {
    'Baden-Württemberg': '#ff7f0e',  # bright orange
    'Bayern': '#1f77b4',  # blue
    'Berlin': '#d62728',  # red
    'Brandenburg': '#2ca02c',  # green
    'Bremen': '#9467bd',  # purple
    'Hamburg': '#8c564b',  # brown
    'Hessen': '#e377c2',  # pink
    'Mecklenburg-Vorpommern': '#7f7f7f',  # gray
    'Niedersachsen': '#bcbd22',  # olive
    'Nordrhein-Westfalen': '#17becf',  # cyan
    'Rheinland-Pfalz': '#ffbb78',  # light orange
    'Saarland': '#98df8a',  # light green
    'Sachsen': '#ff9896',  # salmon
    'Sachsen-Anhalt': '#c5b0d5',  # lavender
    'Schleswig-Holstein': '#f7b6d2',  # light pink
    'Thüringen': '#c49c94'  # beige
}

color_electric = "#81E552"
color_hybrid = "#FD8714"
color_gas = "#59BD2F"
color_benzin = "#029BD8"
color_diesel = "#FFDA00"

colors_fuel = { 
    "Electric": "#81E552", 
    "Plug-in Hybrid": "#4CD8E8" ,
    "Hybrid total": "#FD8714",
    "Gas": "#59BD2F",
    "Benzin": "#029BD8",
    "Diesel": "#FFDA00"
}


presentation_colors = ['#81E552', '#59BD2F', '#FD8714', '#4CD8E8', '#029BD8', '#FFDA00']

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




def merge_excel_sheets(file_path):
    """
    Function to merge multiple sheets from an Excel file into a single DataFrame.
    It assumes that the sheet names are years and that the first row of each sheet contains the column headers.
    The function will add a new column 'Year' to the DataFrame, which will contain the year corresponding to each sheet.
    This is useful for datasets where each sheet represents data for a different year.
    input: file_path --> path to the Excel file
    output: merged DataFrame
    """
    xls = pd.ExcelFile(file_path)
    
    # Read all sheets into a single DataFrame
    df_list = []
    for sheet in xls.sheet_names:
        temp_df = pd.read_excel(xls, sheet_name=sheet)
        temp_df["Year"] = int(sheet)  # Convert sheet name to year (assuming it's a valid year)
        df_list.append(temp_df)

    # Merge all dataframes
    final_df = pd.concat(df_list, ignore_index=True)
    
    return final_df

def create_new_dataframe(df):    
    # we consider electric and hybrid as electrical, since they all use the charging stations
    electric_types = ["Electric", "Plug-in Hybrid"]

    # filter the electrical vehicles
    eautos = df[df["fuel"].isin(electric_types)]
    # summs the electrical vehicles
    e_autos_per_state = eautos.groupby("state").agg(
    number_of_electric_cars=("total_cars", "sum")     
    ).reset_index()

    # filter the total of cars    
    total_cars = df [df['fuel'] == 'Total']
    total_cars.drop(columns=['fuel', 'year'], inplace=True)

    autos_state = e_autos_per_state.merge(total_cars, on = "state", how="left")
    autos_state
    autos_state['number_non_electric_cars'] = autos_state['total_cars'] - autos_state['number_of_electric_cars']
    autos_state.rename (columns = {'total_cars':'number_cars'}, inplace = True)
    return autos_state

                     