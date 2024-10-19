from manim import *

class ResBlock(Scene):
    def construct(self):
        layers = self.create_network(2)
        arrows = self.add_arrows(layers)
        network = VGroup(layers, arrows).scale(0.45)
        skip_conn = self.add_skip_connection(layers[0], layers[-1].get_top() + 0.7 * UP)
        #skip_conn[].next_to(layers[-1], UP, buff=0.5)
        
        output_arrow = Arrow(layers[-1].get_top(), skip_conn[1].get_bottom(), stroke_width=1, buff=0 )
        output = self.add_output(skip_conn[1])
        
        braces = self.add_braces(layers[1], layers[-1])
        
        self.add(layers, arrows, output, skip_conn, output_arrow, braces)
    
    def create_layer(self, color, text):
        rect = Rectangle(height=text.height+0.5, width=text.width+1)
        rect.set_fill(color=color, opacity=0.5)
        rect.set_stroke(color=color, width=0.5)
        rect.move_to(text.get_center())
        return rect
    
    def create_network(self, n_hidden):
        layers = VGroup()
        input_text = Text("Input")
        input_layer = self.create_layer(color=GREY_B, text=input_text)
        layers.add(VGroup(input_text,input_layer))
        
        for i in range(n_hidden):
            layer_text = Text(f"Layer {i+1}".format(i))
            layer = self.create_layer(color=BLUE_C, text=layer_text)
            layers.add(VGroup(layer, layer_text))
        layers.arrange(UP, buff=1)
        return layers
    
    def add_skip_connection(self, in_layer, target):
        addop_text = Tex("+").scale(0.55)
        addop_rect = Rectangle(height=addop_text.height+0.1, width=addop_text.width+0.1)
        addop_rect.set_fill(color=YELLOW_E, opacity=0.5)
        addop_rect.set_stroke(color=YELLOW_E, width=0.5)
        addop_rect.move_to(addop_text.get_center())
        addop = VGroup(addop_text, addop_rect)
        addop.move_to(target)
        
        skip_arrow = ArcBetweenPoints(in_layer.get_top(), addop.get_right(), angle=160*DEGREES,
                                      stroke_width=2)
        skip_arrow.add_tip(tip_length=0.1, tip_width=0.1)
        arrow_text = Text("Skip connection").scale(0.35).next_to(skip_arrow,  RIGHT, buff=0.3)
        return VGroup(VGroup(skip_arrow, arrow_text), addop)
    
    def add_braces(self, start, end):
        bottom_corner = start.get_corner(DL)
        top_corner = end.get_corner(UL)
        brace = BraceBetweenPoints(bottom_corner, top_corner, direction=LEFT)
        brace_text = Tex("f(x) = h(x) - x").scale(0.5).next_to(brace, LEFT, buff=0.1)
        return VGroup(brace, brace_text)
        
    
    def add_arrows(self, layers):
        arrows = VGroup()
        
        for i in range(len(layers) - 1):
            arrow = Arrow(layers[i].get_top(), layers[i+1].get_bottom(), stroke_width=1, buff=0)
            arrows.add(arrow)
        return arrows
    
    def add_output(self, layer):
        output = Tex("h(x)").scale(0.55).next_to(layer, UP, buff=0.5)
        arrow = Arrow(layer.get_top(), output.get_bottom(), buff=0, stroke_width=1)
        return VGroup(arrow, output)