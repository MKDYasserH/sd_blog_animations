from manim import *

class AEArchitecture(Scene):
    def construct(self):
        layers, arrows = self.construct_ae(3, [3, 2, 3])
        self.add(layers, arrows)
    
    
    def add_layer(self, n_neurons, color):
        layer = VGroup()
        for i in range(n_neurons):
            circ = Circle(radius=0.5, color=color).set_fill(color=color, opacity=0.5)
            layer.add(circ)
        layer.arrange(DOWN, buff=0.5)
        return layer
    
    def add_arrows(self, in_layer, out_layer, width, tip_width):
        arrow_group = VGroup()
        for i in range(len(in_layer)):
            for j in range(len(out_layer)):
                arrow = Arrow(in_layer[i].get_right(), out_layer[j].get_left(), 
                              max_stroke_width_to_length_ratio=width, max_tip_length_to_length_ratio=tip_width, buff=0.1)
                arrow_group.add(arrow)
        return arrow_group
    
    def construct_ae(self, n_layers, layers_size):
        layers = VGroup()
        arrows = VGroup()
        for i in range(n_layers):
            layer = self.add_layer(layers_size[i], GRAY_A)
            layers.add(layer)
        
        layers.arrange(RIGHT, buff=1)
        
        for i in range(len(layers)-1):
            arrow_group =  self.add_arrows(layers[i], layers[i+1], 5, 0.1)
            arrows.add(arrow_group)
        
        return layers, arrows

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = AEArchitecture()
        scene.render()