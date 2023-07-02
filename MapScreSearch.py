from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from geopy.geocoders import Nominatim

KV = '''
<Demo>:
    Screen:
        name: "screen1"
        MDLabel:
            text: "screen 1"
            halign: "center"

        MDRaisedButton:
            text: "Go to screen 2"
            pos_hint: {"center_x": .5, "center_y": .4}
            on_release: root.current = "screen2"

    Screen:
        name: "screen2"
        BoxLayout:
            orientation: "vertical"

            BoxLayout:
                size_hint_y: None
                height: "48dp"

                Widget:
                    size_hint_x: None
                    width: "48dp"

                MDIconButton:
                    icon: "arrow-left"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.current = "screen1"

            BoxLayout:
                size_hint_y: None
                height: "48dp"

                MDTextField:
                    id: search_field
                    hint_text: "Search location"
                    size_hint_x: 0.8
                    on_text_validate: app.show_search_dialog(search_field.text, mapview)

                MDIconButton:
                    icon: "magnify"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.show_search_dialog(search_field.text, mapview)

            MapView:
                id: mapview
                zoom: 10
                lat: 36
                lon: -115
'''

class Demo(ScreenManager):
    pass

class Main(MDApp):
    def build(self):
        Builder.load_string(KV)
        return Demo()

    def show_search_dialog(self, search_text, mapview):
        if not search_text:
            return

        geolocator = Nominatim(user_agent="myapp")
        location = geolocator.geocode(search_text)

        if location is not None:
            lat, lon = location.latitude, location.longitude
            mapview.center_on(lat, lon)
            mapview.zoom = 10
            marker = MapMarkerPopup(lat=lat, lon=lon)
            mapview.add_marker(marker)

class SearchDialogContent(BoxLayout):
    text = StringProperty("")

    def __init__(self, mapview, **kwargs):
        super().__init__(**kwargs)
        self.mapview = mapview

Main().run()
