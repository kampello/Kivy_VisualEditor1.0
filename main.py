import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.lang import Builder
from kv_exporter import export_to_kv


class Editor(BoxLayout):
    selected_widget = None
    dragging_widget = None

    def add_widget_to_canvas(self, widget_type):
        canvas = self.ids.canvas_area
        widget = None

        if widget_type == 'Button':
            widget = Button(text='Botão', size_hint=(None, None), size=(100, 50), pos=(100, 100))
        elif widget_type == 'Label':
            widget = Label(text='Label', size_hint=(None, None), size=(100, 50), pos=(100, 160),color=(0, 0, 0, 1))

        if widget:
            widget.bind(on_touch_down=self.on_widget_touch_down)
            widget.bind(on_touch_move=self.on_widget_touch_move)
            widget.bind(on_touch_up=self.on_widget_touch_up)
            canvas.add_widget(widget)

    def on_widget_touch_down(self, widget, touch):
        if widget.collide_point(*touch.pos):
            self.selected_widget = widget
            self.dragging_widget = widget
            self.ids.prop_label.text = f"Selecionado: {widget.__class__.__name__}"
            self.ids.prop_text.text = getattr(widget, 'text', '')
            self.ids.prop_id.text = getattr(widget, 'id', '')
            self.ids.prop_width.text = str(int(widget.width))
            self.ids.prop_height.text = str(int(widget.height))
            return True
        return False

    def on_widget_touch_move(self, widget, touch):
        if self.dragging_widget == widget:
            canvas = self.ids.canvas_area
            new_x = min(max(touch.x - widget.width / 2, canvas.x), canvas.right - widget.width)
            new_y = min(max(touch.y - widget.height / 2, canvas.y), canvas.top - widget.height)
            widget.pos = (new_x, new_y)
            return True
        return False

    def on_widget_touch_up(self, widget, touch):
        if self.dragging_widget == widget:
            self.dragging_widget = None
            return True
        return False

    def update_selected_text(self, text):
        if self.selected_widget and hasattr(self.selected_widget, 'text'):
            self.selected_widget.text = text

    def update_selected_id(self, id_text):
        if self.selected_widget:
            self.selected_widget.id = id_text

    def update_selected_width(self, width_text):
        if self.selected_widget:
            try:
                self.selected_widget.width = int(width_text)
            except ValueError:
                pass

    def update_selected_height(self, height_text):
        if self.selected_widget:
            try:
                self.selected_widget.height = int(height_text)
            except ValueError:
                pass

    def open_color_picker(self, target='text'):
        content = BoxLayout(orientation='vertical')
        self.color_picker = ColorPicker()
        content.add_widget(self.color_picker)

        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10, padding=10)
        btn_cancel = Button(text='Cancelar')
        btn_ok = Button(text='OK')
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_ok)
        content.add_widget(buttons)

        self.color_target = target

        self.popup = Popup(title='Selecione a cor', content=content, size_hint=(0.8, 0.8), auto_dismiss=False)
        btn_cancel.bind(on_release=self.popup.dismiss)
        btn_ok.bind(on_release=self.apply_color_and_dismiss)
        self.popup.open()

    def apply_color_and_dismiss(self, *args):
        rgba = self.color_picker.color
        if self.color_target == 'text':
            self.apply_text_color(rgba)
        elif self.color_target == 'background':
            self.apply_background_color(rgba)
        self.popup.dismiss()

    def apply_text_color(self, rgba):
        if self.selected_widget and hasattr(self.selected_widget, 'color'):
            self.selected_widget.color = rgba

    def apply_background_color(self, rgba):
        if not self.selected_widget:
            return
        if isinstance(self.selected_widget, Button):
            self.selected_widget.background_color = rgba
        elif isinstance(self.selected_widget, Label):
            canvas = self.selected_widget.canvas.before
            canvas.clear()
            from kivy.graphics import Color, Rectangle
            with self.selected_widget.canvas.before:
                Color(*rgba)
                rect = Rectangle(pos=self.selected_widget.pos, size=self.selected_widget.size)

            def update_rect(instance, value):
                rect.pos = instance.pos
                rect.size = instance.size

            self.selected_widget.bind(pos=update_rect, size=update_rect)

    def export_layout(self):
        canvas = self.ids.canvas_area

        # Cria pasta se não existir
        export_folder = 'exported_ui'
        os.makedirs(export_folder, exist_ok=True)

        # Exporta o arquivo .kv para a pasta
        kv_path = os.path.join(export_folder, 'kivy.kv')
        export_to_kv(canvas.children[::-1], filepath=kv_path)

        # Salva o main.py na mesma pasta
        self.save_main_py(export_folder)

    def save_main_py(self, folder):
        main_py_content = '''from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

class RootWidget(FloatLayout):
    pass

class MyApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Builder.load_file('kivy.kv')
    MyApp().run()
'''
        main_py_path = os.path.join(folder, 'main.py')
        with open(main_py_path, "w", encoding="utf-8") as f:
            f.write(main_py_content)


# <- fora da classe Editor
class KVEditorApp(App):
    def build(self):
        return Editor()


if __name__ == '__main__':
    KVEditorApp().run()
