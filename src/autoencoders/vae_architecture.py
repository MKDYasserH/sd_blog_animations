import os
from manim import *
from PIL import Image

LAYER_SIZE = [5, 4, 3]
COLORS = [GREY_B, GREEN_D, YELLOW_D]
ENCODER_LAYERS = ["Input", "Hidden\hspace{0.1cm}1", "Hidden\hspace{0.1cm}2"]
DECODER_LAYERS = ["Hidden\hspace{0.1cm}4", "Hidden\hspace{0.1cm}5", "Output"]

class VAEArchitecture(Scene):
    def construct(self):
        encoder, decoder = self.construct_ae(len(LAYER_SIZE), LAYER_SIZE)
        encoder.scale(0.35).shift(DOWN)
        decoder.scale(0.35)
        decoder.next_to(encoder, UP, buff=2)
        encoder_arrows, decoder_arrows = self.add_arrows(encoder), self.add_arrows(decoder)
        first_row, second_row, fr_arrows, last_arrow = self.construct_bottleneck(encoder, decoder)
        
        image_array = np.uint8(Image.open(os.path.join("assets","autoencoders/gaussian_distro_3D.png")))
        image = ImageMobject(image_array).scale(0.2).next_to(second_row, RIGHT, buff=0.5)
        image_text = MathTex(r"\mathcal{N}(0,1)").scale(0.35).next_to(image, UP, buff=0.3)
         
        self.add(encoder, decoder, encoder_arrows, decoder_arrows, first_row, 
                 second_row, fr_arrows, image, image_text, last_arrow)
    
    def add_layer(self, n_neurons, color):
        """Create a single layer with circles representing neurons."""
        layer = VGroup()
        for i in range(n_neurons):
            circ = Circle(radius=0.2, color=color).set_fill(color=color, opacity=0.5)
            layer.add(circ)
        layer.arrange(DOWN, buff=0.3)
        return layer
    
    def construct_ae(self, n_layers, layers_width):
        encoder = VGroup()
        decoder = VGroup()
        # Encoder
        for i in range(n_layers):
            rect = self.create_rectangle_with_text(ENCODER_LAYERS[i], width=layers_width[i], 
                                                   height=1, color=COLORS[i])
            encoder.add(rect)
            encoder.arrange(UP, buff=0.5)
        
        # Decoder
        reversed_list = list(reversed(layers_width))
        for i in range(n_layers):
            rect = self.create_rectangle_with_text(DECODER_LAYERS[i], width=reversed_list[i], 
                                                   height=1, color=list(reversed(COLORS))[i])
            decoder.add(rect)
            decoder.arrange(UP, buff=0.5)
            
        return encoder, decoder
    
    def construct_bottleneck(self, encoder, decoder):
        fr_arrows = VGroup()
        
        mean = self.create_rectangle_with_text("\mu", width=1, height=1, color=ORANGE)
        variance = self.create_rectangle_with_text("\sigma", width=1, height=1, color=ORANGE)
        first_row = VGroup(mean, variance).scale(0.35).arrange(RIGHT, buff=0.3).next_to(encoder[-1], UP, buff=0.5)
        first_row.shift(RIGHT*0.33)
        noise = self.create_rectangle_with_text("\\text{Gaussian noise}", width=3.5, height=1, color=BLUE_D)
        #noise_text = Text("Gaussian noise").scale(0.25).next_to(noise, UP, buff=0.2)
        add_op = self.create_rectangle_with_text("+", width=1, height=1, color=GRAY)
        mul_op = self.create_rectangle_with_text("\\times", width=1, height=1, color=GRAY)
        second_row = VGroup(add_op, mul_op, noise).scale(0.35).arrange(RIGHT, buff=0.3)
        second_row.next_to(first_row, UP, buff=0.3).shift(RIGHT*0.76)
        
        for i in range(len(first_row)):
            fr_arrows.add(Arrow(encoder[-1].get_top(), first_row[i].get_bottom(), stroke_width=2, tip_length=0.08, buff=0.1))
            fr_arrows.add(Arrow(first_row[i].get_top(), second_row[i].get_bottom(), stroke_width=2, tip_length=0.1))
        
        noise_arrow = Arrow(noise.get_left(), mul_op.get_right(), stroke_width=3, tip_length=0.1, buff=0.05)
        op_arrow = Arrow(mul_op.get_left(), add_op.get_right(), stroke_width=3, tip_length=0.1, buff=0.05)
        fr_arrows.add(noise_arrow, op_arrow)
        last_arrow = Arrow(add_op.get_top(), decoder[0].get_bottom(), stroke_width=3, tip_length=0.08, buff=0.05)
        return first_row, second_row, fr_arrows, last_arrow
    
    def add_arrows(self, layers):
        arrows = VGroup()
        for i in range(len(layers)-1):
            arrow = Arrow(layers[i].get_top(), layers[i+1].get_bottom(), 
                          stroke_width=3, tip_length=0.1, buff=0.1)
            arrows.add(arrow)
        return arrows
    
        
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

    def create_rectangle_with_text(self, text, width, height, color=WHITE):
        """Creates a rectangle with a given text label and a 3D stack effect."""
        # Create label and rectangle with original dimensions
        label = MathTex(text)
        rect = Rectangle(width=width, height=height)
        rect.set_fill(color, opacity=0.8)
        rect.set_stroke(color, width=1)
        rect.move_to(label.get_center())
        rect_text = VGroup(rect, label)
        return rect_text

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = VAEArchitecture()
        scene.render()