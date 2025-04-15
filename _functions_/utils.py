import matplotlib
from matplotlib.ticker import FuncFormatter

# Define a function to format numbers in thousands and millions
# The function takes a number and its position as input and returns a formatted string
# This is to replace the default number formatting in matplotlib
# The function is used to display numbers in a more readable format, especially for large numbers
def thousands_millions_formatter(x, pos):
    if x >= 1e6:
        return f'{x*1e-6:.0f}M'
    elif x >= 1e3:
        return f'{x*1e-3:.0f}K'
    else:
        return f'{int(x)}'

# Define a function to format numbers in thousands using european style
# The function takes a number and its position as input and returns a formatted string
# This is to replace the default number formatting in matplotlib
# The function is used to display numbers in a more readable format, especially for large numbers

def european_thousands(x, pos):
    return f'{x:,.0f}'.replace(',', '.')


def format_axes(ax):
    '''Function to format axes for better readability.
    It hides the top and right spines and formats the y-axis ticks.
    Args:
        ax (matplotlib.axes.Axes or list of matplotlib.axes.Axes): The axes to format.
    '''
    #if not isinstance(ax, (list, tuple)):
    #    ax = [ax]
    #for a in ax:
    #    if not isinstance(a, matplotlib.axes.Axes):
    #        raise TypeError("Expected ax to be a matplotlib.axes.Axes instance or a list/tuple of them.")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_millions_formatter))
