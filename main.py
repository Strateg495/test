from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.image import Image
import json
from datetime import datetime

class ProductInput(BoxLayout):
    def __init__(self, **kwargs):
        super(ProductInput, self).__init__(**kwargs)        
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20             

        self.product_label = Label(text='Product Name:', size_hint=(1, 0.2))
        self.add_widget(self.product_label)

        self.product_input = TextInput(multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.product_input)

        self.expiry_label = Label(text='Expiry Date:', size_hint=(1, 0.2))
        self.add_widget(self.expiry_label)

        self.expiry_input = TextInput(multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.expiry_input)

        self.submit_button = Button(text='Submit', size_hint=(1, 0.2))
        self.submit_button.bind(on_press=self.submit)
        self.add_widget(self.submit_button)

        self.show_button = Button(text='Show Products', size_hint=(1, 0.2))
        self.show_button.bind(on_press=self.show_products)
        self.add_widget(self.show_button)

        self.show_button = Button(text='Show Expired Products', size_hint=(1, 0.2))
        self.show_button.bind(on_press=self.show_expired_products)
        self.add_widget(self.show_button)        

        self.message_label = Label(text='', size_hint=(1, 0.2))
        self.add_widget(self.message_label)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.add_widget(self.scroll_view)

        self.product_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.product_list.bind(minimum_height=self.product_list.setter('height'))
        self.scroll_view.add_widget(self.product_list)

    def submit(self, instance):
        product_name = self.product_input.text
        expiry_date = self.expiry_input.text

        data = {
            'product': product_name,
            'expiry': expiry_date
        }
        with open('products.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

        self.product_input.text = ''
        self.expiry_input.text = ''
        self.message_label.text = 'Product saved successfully!'

    def show_products(self, instance):
        self.product_list.clear_widgets()
        with open('products.json', 'r') as f:
            for line in f:
                data = json.loads(line)
                product_label = Label(text=f'Product: {data["product"]}, Expiry: {data["expiry"]}', size_hint_y=None, height=40)
                self.product_list.add_widget(product_label)
    
    def show_expired_products(self, instance):
        self.product_list.clear_widgets()
        with open('products.json', 'r') as f:
            for line in f:
                data = json.loads(line)
                expiry_date = datetime.strptime(data['expiry'], '%d-%m-%Y')
                if expiry_date <= datetime.now():
                    product_label = Label(text=f'Product: {data["product"]}, Expiry: {data["expiry"]}', size_hint_y=None, height=40)
                    self.product_list.add_widget(product_label)

class ProductApp(App):
    def build(self):        
        Window.size = (400, 600)         
        return ProductInput()
        

if __name__ == '__main__':
    ProductApp().run()