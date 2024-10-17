import os
from manim import *
from PIL import Image

class AEArchitecture(Scene):
    def construct(self):
        # Construct layers and arrows
        layers, arrows = self.construct_ae(5, [3, 3, 2, 3, 3])
        self.add(layers, arrows)
        
        # Add rectangles around specific layers
        rect1, rect2, rect3 = self.add_rect(layers[:2], BLUE_B), self.add_rect(layers[2], PURPLE_B), self.add_rect(layers[3:], BLUE_B)
        text1 = Text("Encoder").scale(0.35).next_to(rect1, UP, buff=0.5)
        text2 = Text("Latent").scale(0.35).next_to(text1, RIGHT, buff=1)
        text3 = Text("Decoder").scale(0.35).next_to(rect3, UP, buff=0.5)
        self.add(rect1, rect2, rect3, text1, text2, text3)
        
        # add input output image
        in_image, in_arrow = self.add_io(rect1, "autoencoders/cassiopeia.jpg")
        out_image, out_arrow = self.add_io(rect3, "autoencoders/cassiopeia.jpg", "out")
        self.add(in_image, out_image, in_arrow, out_arrow)
    
    def add_layer(self, n_neurons, color):
        """Create a single layer with circles representing neurons."""
        layer = VGroup()
        for i in range(n_neurons):
            circ = Circle(radius=0.2, color=color).set_fill(color=color, opacity=0.5)
            layer.add(circ)
        layer.arrange(DOWN, buff=0.3)
        return layer
    
    def add_arrows(self, in_layer, out_layer, stroke_width, tip_length):
        """Add arrows between each pair of neurons in consecutive layers with fixed stroke width and tip length."""
        arrow_group = VGroup()
        for i in range(len(in_layer)):
            for j in range(len(out_layer)):
                arrow = Arrow(
                    in_layer[i].get_right(), 
                    out_layer[j].get_left(), 
                    buff=0.1,
                    stroke_width=stroke_width,  # Set a fixed stroke width
                    tip_length=tip_length  # Set a fixed tip length
                )
                arrow_group.add(arrow)
        return arrow_group
    
    def construct_ae(self, n_layers, layers_size):
        """Construct the autoencoder layers and arrows connecting them."""
        layers = VGroup()
        arrows = VGroup()
        for i in range(n_layers):
            layer = self.add_layer(layers_size[i], GRAY_A)
            layers.add(layer)
        
        # Arrange layers horizontally with a buffer
        layers.arrange(RIGHT, buff=0.7)
        
        # Add arrows between consecutive layers with fixed stroke width and tip length
        for i in range(len(layers) - 1):
            arrow_group = self.add_arrows(layers[i], layers[i+1], stroke_width=2, tip_length=0.08)
            arrows.add(arrow_group)
        
        return layers, arrows
    
    def add_rect(self, layers, color):
        """Add a rectangle around specified layers."""
        if not isinstance(layers.submobjects[0], VGroup):
            rect = Rectangle(height=layers[0].height + 1, width=layers[0].width + 0.5)
        else:
            width = layers[-1].get_right()[0] - layers[0].get_left()[0]
            rect = Rectangle(height=layers[0].height + 0.5, width=layers[0].width + width * 0.85)
        rect.set_fill(color=color, opacity=0.5)
        rect.set_stroke(color=color, width=0.5)
        rect.move_to(layers.get_center())
        return rect
    
    def add_io(self, rect, image_path, io="in"):
        image_array = np.uint8(Image.open(os.path.join("assets",image_path)))
        image = ImageMobject(image_array).scale(0.28)
        if io=="in":
            image.next_to(rect, LEFT, buff=0.8)
            arrow = Arrow(image.get_right(), rect.get_left(), buff=0.1)
        elif io=="out":
            image.next_to(rect, RIGHT, buff=0.8)
            arrow = Arrow(rect.get_right(), image.get_left(), buff=0.1)
        
        return image, arrow

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = AEArchitecture()
        scene.render()