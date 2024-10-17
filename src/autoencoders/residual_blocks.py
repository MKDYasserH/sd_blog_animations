from manim import *

class ResBlock(Scene):
    def construct(self):
        raise NotImplementedError
    
    def create_layer(self, color, text):
        rect = Rectangle(height=text.height+0.5, width=text.width+1)
        rect.set_fill(color=color, opacity=0.5)
        rect.set_stroke(color=color, width=0.5)
        rect.move_to(text.get_center())
        return rect
    
    def create_network(self, n_hidden):
        layers = VGroup()
        
        input_layer = self.create_layer(color=GREY_B, text=Text("Input"))
        layers.add(input_layer)
        
        for i in range(n_hidden):
            layer = self.create_layer(color=BLUE_C, text=Text(f"Layer {i}".format(i)))
            layers.add(layer)
        
        return layers
    
    def add_skip_arrow(self):
        raise NotImplementedError
    
    def add_brackets(self):
        raise NotImplementedError