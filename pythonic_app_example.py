from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import ButtonBehavior
from kivy.config import Config
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from kivy_garden.graph import Graph, MeshLinePlot
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivy.uix.gridlayout import GridLayout

Builder.load_string('''
<ImageButton>:
    source: root.image_source
    allow_stretch: True
    keep_ratio: False
''')

class ImageButton(ButtonBehavior, Image):
    image_source = StringProperty('')
    text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_press(self):
        self.color = (0.5, 0.5, 0.5, 1)
        self.scale = 1.1

    def on_release(self):
        Clock.schedule_once(lambda dt: self.reset_color_and_scale(), 0.15)

    def reset_color_and_scale(self):
        self.color = (1, 1, 1, 1)
        self.scale = 1


# Set the background color to white
Window.clearcolor = (1, 1, 1, 1)

class WelcomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.welcome_label = Label(text=' ', color=(0, 0, 0, 1))
        layout.add_widget(self.welcome_label)
        
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.logo = Image(source='logo.png')
        anchor.add_widget(self.logo)
        layout.add_widget(anchor)
        
        self.welcome_label = Label(text='Welcome!', color=(0, 0, 0, 1))
        layout.add_widget(self.welcome_label)

        # Animate the label's opacity property
        anim = Animation(opacity=0, duration=2) + Animation(opacity=1, duration=2)
        anim.repeat = True
        anim.start(self.welcome_label)

        self.get_started_button = Button(text='Get Started', size_hint_y=None, height=30)
        self.get_started_button.bind(on_press=self.get_started)
        layout.add_widget(self.get_started_button)

        self.add_widget(layout)

    def get_started(self, instance):
        self.manager.current = 'menu'


class WelcomeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomePage(name='welcome'))
        sm.add_widget(MenuPage(name='menu'))
        sm.add_widget(StockPage(name='stocks'))


        return sm
    

class MenuPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[10, 20, 10, 20], spacing=10)

        self.menu_label = Label(text='Menu', font_size='30sp', size_hint_y=None, height='40sp', halign='center', valign='middle', color=(0, 0, 0, 1))
        layout.add_widget(self.menu_label)

        self.option1_button = ImageButton(image_source='option1.webp', text='Option 1')
        self.option1_button.bind(on_press=self.get_stocks)

        layout.add_widget(self.option1_button)

        self.option2_button = ImageButton(image_source='option2.webp', text='Option 2')
        layout.add_widget(self.option2_button)

        self.option3_button = ImageButton(image_source='option3.webp', text='Option 3')
        layout.add_widget(self.option3_button)

        self.add_widget(layout)

    
    def get_stocks(self, instance):
        self.manager.current = 'stocks'



class StockPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Create a button widget for the back action
        back_button = Button(text='Back')
        back_button.bind(on_press=self.back_button_pressed)
        layout.add_widget(back_button)

        # Load stock data using Pandas
        data = pd.read_csv('your_stock_data.csv')

        # Create a candlestick chart using Plotly Express
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                             open=data['open'],
                                             high=data['high'],
                                             low=data['low'],
                                             close=data['close'])])

        # Add annotations to the chart
        fig.add_annotation(x="2022-07-12", y=data.loc[data['Date'] == "2022-07-12", 'close'].iloc[0],
                        text='Stock Event 1 Explained by news', showarrow=True, arrowhead=1)
        fig.add_annotation(x="2023-03-10", y=data.loc[data['Date'] == "2023-03-10", 'close'].iloc[0],
                   text='Stock Event 2 Explained by news', showarrow=True, arrowhead=1)

        # Customize the chart appearance
        fig.update_layout(title='Stock Candlestick Chart',
                        xaxis_title='Date',
                        yaxis_title='Price')     

        # Convert the Plotly chart to a static image
        img_bytes = fig.to_image(format="png", width=800, height=600, scale=2)
        
        # Save the image to a file
        with open("stock_chart.png", "wb") as f:
            f.write(img_bytes)

        # Create an Image widget to display the chart
        chart_image = Image(source="stock_chart.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
        chart_container = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.8))
        chart_container.add_widget(chart_image)
        
        # Add the chart image to the layout
        layout.add_widget(chart_container)

        # Add the layout to the StockPage
        self.add_widget(layout)
        
    
    def back_button_pressed(self, instance):
        # Handle the back action
        self.manager.current = 'menu'

if __name__ == '__main__':
    Window.size = (270, 500)
    WelcomeApp().run()
