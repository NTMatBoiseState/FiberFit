import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib notebook
from ipywidgets import *
from IPython.display import display
from IPython.html import widgets
import base64
res = 'computed results'
plt.style.use('ggplot')
from src.fibers_QQQQQQ_invert import fiber_analysis
from quanfima_torun import fiber_visualization
import os
import glob
#button = widgets.Button(description='My Button')
#out = widgets.Output()
#import ipyvuetify as v   
from IPython.display import display, FileLink
# linking button and function together using a button's method
#button.on_click(on_button_clicked)
# displaying button and its output together
#widgets.VBox([button,out])

from src.foruploading5 import ff,upload,prepimages
import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
from ipywidgets import interact, interact_manual
def s(_):
    s = widgets.FileUpload(accept='', multiple=True)
    return s.data

def run(_):

    button = widgets.Button(
        description='Run Fiber Analysis',
        layout={'width': '300px'})
    out= widgets.Output()
    def on_button_clicked(_):
      # "linking function with output"
        with out:
              # what happens when we press the button
            clear_output()
            print('Program executing. Output in output folder on home page')
            fiber_analysis( CO_lower=int(text1.value),
                    CO_upper=int(text2.value), 
                    angleInc=int(text3.value),
                    radStep=float(text4.value),
                    mypath='Data/',
                    savepath='output/')
    text1 = widgets.Text(
                placeholder='20',
                description="Max fiber Thickness (pixels)",
                layout={'width':'300px'},
                style={'description_width':'175px'})
    text2 = widgets.Text(
                placeholder='2',
                description="Min fiber Thickness (pixels)",
                layout={'width':'300px'},
                style={'description_width':'175px'})
    text3 = widgets.Text(
                placeholder='1',
                description="Angle Increment (degrees)",
                layout={'width':'300px'},
                style={'description_width':'175px'})
    text4 = widgets.Text(
                placeholder='0.5',
                description="Radial Step Size (radians)",
                layout={'width':'300 px'},
                style={'description_width':'175px'})
    button.on_click(on_button_clicked)
    box=widgets.VBox([text1,text2,text3,text4,button])
    display(box,out)
def run2(_):

    button = widgets.Button(
        description='Run Fiber Orientation Visualization',
        layout={'width': '300px'})
    out= widgets.Output()
    def on_button_clicked(_):
      # "linking function with output"
        with out:
              # what happens when we press the button
            clear_output()
            print('Program executing. Output in output folder on home page')
            fiber_visualization()
   
    button.on_click(on_button_clicked)
    box=widgets.VBox([button])
    display(box,out)

from ipywidgets import HTML
HTML()
    
def save(_):
    filename = 'notebook.tar.gz'
    b64 = base64.b64encode(res.encode())
    payload = b64.decode()
    #BUTTONS
    html_buttons = '''<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <a download="{filename}" href="notebook.tar.gz" download>
    <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-warning">Download File</button>
    </a>
    </body>
    </html>
    '''
    html_button = html_buttons.format(payload=payload,filename=filename)
    display(HTML(html_button))
    out= widgets.Output()   

    
def clear(_):
    button = widgets.Button(
        description='Clear Data',
        layout={'width': '300px'})
    out= widgets.Output()
    def on_button_clicked(_):
      # "linking function with output"
        with out:
              # what happens when we press the button
            clear_output()
            print('Program executing. Files in Data and output folder will be cleared')
            files = glob.glob('Data/*',recursive=True)
            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

            files = glob.glob('output/*',recursive=True)

            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))
    button.on_click(on_button_clicked)
    box=widgets.VBox([button])
    display(box,out)
    out= widgets.Output() 
