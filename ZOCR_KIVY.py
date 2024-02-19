from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label 
from kivy.core.window import Window
from plyer.facades import Camera
import time

class ZOCR(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        # Tabbed layout
        tabbed_panel = TabbedPanel(do_default_tab= False)
        tab1 = TabbedPanelItem(text='SCAN')
        tab1.add_widget(Label(text='Content for Tab 1'))
        top_frame = Label(text="Top Frame", size_hint_y=None, height=40)
        tab1.add_widget(top_frame)
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        button1 = Button(text="Button 1")
        button2 = Button(text="Button 2")
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        tab1.add_widget(button_layout)
        tab2 = TabbedPanelItem(text='PROCESS')
        tab2.add_widget(Label(text='Content for Tab 2'))
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)
        main_layout.add_widget(tabbed_panel)
        return main_layout
if __name__ == '__main__':
    ZOCR().run()
