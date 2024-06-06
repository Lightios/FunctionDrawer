import threading

import kivy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivymd.app import MDApp
import subprocess



from kivymd.uix.boxlayout import MDBoxLayout


class FunctionDrawerApp(MDApp):
    parameter_two = StringProperty()
    parameter_three = StringProperty()
    form_text = StringProperty()

    form: str

    def on_start(self):
        self.on_form_select("Ogólna")
        self.root.ids.default_check.active = True

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        Window.maximize()

    def schedule_generate_animation(self):
        self.hide_show_loading_circle()
        threading.Thread(target=self.generate_animation).start()

    def generate_animation(self):
        formula = None
        f1 = self.root.ids.f1.text
        f2 = self.root.ids.f2.text
        f3 = self.root.ids.f3.text

        match self.form:
            case "Ogólna":
                formula = f"{f1} * x**2 + {f2} * x + {f3}"
            case "Kanoniczna":
                formula = f"{f1} * (x - {f2})**2 + {f3}"
            case "Iloczynowa":
                formula = f"{f1} * (x - {f2}) * (x - {f3})"

        with open("quadratic_formula.py", "w") as f:
            f.write(f"""
from manim import *

class QuadraticFunction(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={{"color": BLUE}},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        def quadratic(x):
            return {formula}

        graph = ax.plot(quadratic, color=WHITE)
        self.play(Create(ax), Create(labels))
        self.play(Create(graph))
        self.wait()
""")
        subprocess.run(["manim", "-qm", "--format", "gif", "quadratic_formula.py", "QuadraticFunction"])
        Clock.schedule_once(self.update_image, 0.5)

    def update_image(self, dt):
        self.show_video()
        self.hide_show_loading_circle()
        self.root.ids.video.source = "media/videos/quadratic_formula/720p30/QuadraticFunction_ManimCE_v0.18.1.gif"
        self.root.ids.video.reload()

    def show_video(self):
        self.root.ids.video.opacity = 1

    def hide_show_loading_circle(self):
        self.root.ids.loading_circle.opacity = 0 if self.root.ids.loading_circle.opacity == 1 else 1

    def on_form_select(self, form):
        parameters_two = {"Ogólna": "b", "Kanoniczna": "p", "Iloczynowa": "x1"}
        parameters_three = {"Ogólna": "c", "Kanoniczna": "q", "Iloczynowa": "x2"}
        forms = {"Ogólna": "ax^2 + bx + c", "Kanoniczna": "a(x - p)^2 + q", "Iloczynowa": "a(x - x1)(x - x2)"}

        self.form_text = forms[form]
        self.parameter_two = f"Podaj parametr: {parameters_two[form]}"
        self.parameter_three = f"Podaj parametr: {parameters_three[form]}"

        self.form = form


class Check(MDBoxLayout):
    text = StringProperty()
    active = BooleanProperty(False)
    function = ObjectProperty()


FunctionDrawerApp().run()