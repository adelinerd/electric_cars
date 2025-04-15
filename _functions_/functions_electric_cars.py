
## This script contains functions and constants used for data analysis and visualization
# in the context of electric cars in Germany. 
# It includes functions for data preprocessing, merging Excel sheets, and creating new DataFrames.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import geopandas as gpd

from utils import thousands_millions_formatter

# Define a list of German states
# The list includes all 16 federal states of Germany
# Each state is represented by its full name in German.
# The states are used in various contexts, including administrative purposes,
# statistical analysis, and geographical representation.
# The states are:
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

# Define a dictionary to map German states to their respective abbreviations
# The abbreviations are based on the official two-letter codes used in Germany
# These codes are commonly used in various contexts, including vehicle registration plates
# and administrative purposes.
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
# Define a dictionary to map German states to their respective colors
# The colors are chosen to be distinct and visually appealing
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

# Define a dictionary to map German states to their respective names in English
# The names are chosen to be more recognizable for an international audience
state_name_mapping = {
    "Baden-Württemberg": "Baden-Wurttemberg",
    "Bayern": "Bavaria",
    "Berlin": "Berlin",
    "Brandenburg": "Brandenburg",
    "Bremen": "Bremen",
    "Hamburg": "Hamburg",
    "Hessen": "Hesse",
    "Mecklenburg-Vorpommern": "Mecklenburg-Western Pomerania",
    "Niedersachsen": "Lower Saxony",
    "Nordrhein-Westfalen": "North Rhine-Westphalia",
    "Rheinland-Pfalz": "Rhineland-Palatinate",
    "Saarland": "Saarland",
    "Sachsen": "Saxony",
    "Sachsen-Anhalt": "Saxony-Anhalt",
    "Schleswig-Holstein": "Schleswig-Holstein",
    "Thüringen": "Thuringia"
}

color_electric = "#81E552" #neongreen
color_hybrid = "#FD8714" #orange
color_gas = "#59BD2F" # green
color_benzin = "#029BD8"
color_diesel = "#FFDA00"

# Define a dictionary to map fuel types to their respective colors
# The colors are chosen to be distinct and visually appealing. Besides, they match the colors used in the presentation.
colors_fuel = { 
    "Electric": "#81E552", 
    "Plug-in Hybrid": "#4CD8E8" ,
    "Hybrid total": "#FD8714",
    "Gas": "#59BD2F",
    "Gasoline": "#029BD8",
    "Diesel": "#FFDA00"
}


# Define a list of colors used in presentation
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



# Define a function to merge multiple sheets from an Excel file into a single DataFrame
# The function assumes that the sheet names are years and that the first row of each sheet contains the column headers
# The function will add a new column 'Year' to the DataFrame, which will contain the year corresponding to each sheet

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

def plot_comparison_maps (geodf, first_column, first_title, second_column, second_title):
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    
    # Map 1: 
    if not isinstance(geodf, pd.DataFrame):
        raise TypeError("geodf must be a GeoDataFrame. Ensure the input is correct.")
    
    gdf_plot  = geodf.plot(
        column=first_column,
        cmap="Greens",
        linewidth=0.8,
        edgecolor='0.8',
        legend=True,
        ax=axes[0]
    )
    axes[0].yaxis.set_major_formatter(FuncFormatter(thousands_millions_formatter))
    axes[0].set_title(first_title, fontsize=14)
    axes[0].axis("off")
    
    # Get the colorbar object from the figure
    cbar = gdf_plot.get_figure().get_axes()[-1]  # last axis is the colorbar
    
    # Apply the custom formatter to colorbar ticks
    cbar.yaxis.set_major_formatter(FuncFormatter(thousands_millions_formatter))
    
    
    # Map 2:
    geodf.plot(
        column=second_column,
        cmap="Greens",
        linewidth=0.8,
        edgecolor='0.8',
        legend=True,
        ax=axes[1]
    )
    axes[1].set_title(second_title, fontsize=14)
    axes[1].axis("off")
    
    plt.tight_layout()
    plt.show()                     


# Define a function to annotate states on a map
# The function takes an axis object, a GeoDataFrame, and a label function as input
# The label function is used to generate the labels for each state
def annotate_states(ax, geodf, label_func):
    for _, row in geodf.iterrows():
        centroid = row["geometry"].centroid
        centroid_x, centroid_y = centroid.x, centroid.y

        if row['state'] == 'Brandenburg':  # Adjust Berlin/Brandenburg overlap
            south_point = row["geometry"].bounds[1]
            adjusted_y = (centroid_y + south_point) / 2
            adjusted_x = centroid_x
        else:
            adjusted_x, adjusted_y = centroid_x, centroid_y

        ax.annotate(
            label_func(row),  # Flexible label
            xy=(adjusted_x, adjusted_y),
            ha="center",
            fontsize=8,
            color="black",
            weight="bold"
        )
