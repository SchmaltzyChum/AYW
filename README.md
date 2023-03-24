# Python App, annotate graphs with news.

This is a simple Python project that demonstrates how to create an android, IOS or Web application using python to annotate candlestick graphs with news events so that users can understand the market events and more easily research stocks.
The programm automatically detects peaks and troughs, fetch news articles related to the stocks peaks and troughs and add them on the graph.

## Installation of Packages

To run the app you need to install the following packages:

- kivy
- pandas
- plotly
- kivy_garden

You can install them using pip. Open a terminal and run the following command:

pip install kivy pandas plotly kivy_garden

To run the peak detection you need to install stock_indicators:

pip install stock_indicators

Attention this packages also need the .NET6 version==6. You need to install it manually.

Just following the instruction here: https://dotnet.microsoft.com/en-us/download/dotnet/7.0

Maybe you need to also install the clr package: 

pip install clr


Note that some dependencies, such as Python itself or the Kivy's dependencies (e.g. Cython), may need to be installed separately. You can find more information in the Kivy documentation.

## Architecture

![Alt-Text](/images/POC_Architecture.png) 

## Running the App

To run the app, navigate to the directory where the `App.py` file is located and run the following command:

python App.py


This will launch the app. You can interact with the UI and plot some data.

That's it! If you have any questions or issues, please feel free to contact me.

## Example Output

If everything was installed correctly and the app was launched correctly, the output should look like this:

### Menu
![Alt-Text](/images/example_menu.png) 

### Example stock graph with market events
![Alt-Text](/images/example_stock_graph.png) 


## Annotation

The scripts main.py, stock_news.py and api.py preforms the fetching of SIX's pricing data finds major stock events and fetches news regarging that stock that was released in conjunction with that market rise/fall.
