from manim import *
from PIL import Image

class BrainVC(ThreeDScene):
    def construct(self):
        # Input Image and Text
        image_array = np.uint8(Image.open("assets/conv_attn/brain_vc.jpg"))
        image = ImageMobject(image_array).to_corner(LEFT, buff=0.5) # Slightly smaller image

        #  Receptive Field size
        rect1 = Rectangle(width=1.5, height=0.5).shift(DOWN * 3)
        text1 = Text("V1").scale(0.5).next_to(rect1, LEFT, buff=0.3)
        rect2 = Rectangle(width=1.5, height=0.5).next_to(rect1, UP, buff=0.5)
        text2 = Text("V2").scale(0.5).next_to(rect2, LEFT, buff=0.3)
        rect3 = Rectangle(width=1.5, height=0.5).next_to(rect2, UP, buff=0.5)
        text3 = Text("V4").scale(0.5).next_to(rect3, LEFT, buff=0.3)
        rect4 = Rectangle(width=1.5, height=0.5).next_to(rect3, UP, buff=0.5)
        text4 = Text("IT").scale(0.5).next_to(rect4, LEFT, buff=0.3)

        # Add shapes to each rectangle
        # Rectangle 1: Three small circles
        small_dots = VGroup(
            Dot(radius=0.2, fill_color=ORANGE).move_to(rect1.get_center() + LEFT * 1),
            Dot(radius=0.2, fill_color=ORANGE).move_to(rect1.get_center()),
            Dot(radius=0.2, fill_color=ORANGE).move_to(rect1.get_center() + RIGHT * 1)
        ).scale(0.35)

        # Rectangle 2: Three bigger dots
        big_dots = VGroup(
            Dot(radius=0.4, fill_color=ORANGE).move_to(rect2.get_center() + LEFT * 1),
            Dot(radius=0.4, fill_color=ORANGE).move_to(rect2.get_center()),
            Dot(radius=0.4, fill_color=ORANGE).move_to(rect2.get_center() + RIGHT * 1)
        ).scale(0.35)

        # Rectangle 3: Smaller ellipse
        small_ellipse = Ellipse(width=0.7, height=0.2, color=ORANGE, fill_color=ORANGE, fill_opacity=1).move_to(rect3.get_center())

        # Rectangle 4: Bigger ellipse
        big_ellipse = Ellipse(width=1.2, height=0.4, color=ORANGE, fill_color=ORANGE, fill_opacity=1).move_to(rect4.get_center())
        
        ## Arrows 
        arrow1 = VGroup(
            Arrow(small_dots[0].get_top(), rect2.get_bottom(), buff=0.1),
            Arrow(small_dots[1].get_top(), rect2.get_bottom(), buff=0.1),
            Arrow(small_dots[2].get_top(), rect2.get_bottom(), buff=0.1))
        arrow2 = VGroup(
            Arrow(big_dots[0].get_top(), rect3.get_bottom(), buff=0.1),
            Arrow(big_dots[1].get_top(), rect3.get_bottom(), buff=0.1),
            Arrow(big_dots[2].get_top(), rect3.get_bottom(), buff=0.1))
        arrow3 = Arrow(rect3.get_top(), rect4.get_bottom(), buff=0.1)
        
        # Group everything together
        stack1 = VGroup(rect1, text1, small_dots, rect2, text2, big_dots, rect3, text3, small_ellipse, 
                 rect4, text4, big_ellipse, arrow1, arrow2, arrow3).next_to(image,RIGHT, buff=1).scale(0.7)
        
        rfs_text = Text("Receptive Fields size").scale(0.35).next_to(stack1, UP, buff=0.2)
        
        #  Receptive Field size
        shape1 = VGroup(
            Line(LEFT+(1/2)*UP, RIGHT+(1/3)*DOWN).scale(0.25).next_to(rect1, RIGHT, buff=0.8),
            Line(DOWN+(1/3)*RIGHT, UP+(1/2)*LEFT).scale(0.25).next_to(rect1, RIGHT, buff=0.8)
            ).shift(DOWN*0.8)
        shape_text1 = Text("Lines").scale(0.5).next_to(shape1, RIGHT, buff=0.3)
        shape2 = Rectangle(width=0.4, height=0.4, color=ORANGE).next_to(rect2, RIGHT, buff=0.8).shift(DOWN*0.45)
        shape_text2 = Text("Shapes").scale(0.5).next_to(shape2, RIGHT, buff=0.3)
        shape3 = Sphere(
            center=(3, 0, 0),
            radius=1,
            resolution=(20, 20),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU]
        ).scale(0.35).set_color(RED).next_to(rect3, RIGHT, buff=0.8).shift(LEFT*0.15,DOWN*0.2)
        shape_text3 = Text("Objects").scale(0.5).next_to(shape3, RIGHT, buff=0.3)
        shape4 = ImageMobject(np.uint8(Image.open("assets/conv_attn/face.jpg"))).scale(0.14).next_to(rect4, RIGHT, buff=0.8).shift(UP*0.1,LEFT*0.15)
        shape_text4 = Text("Faces").scale(0.5).next_to(shape4, RIGHT, buff=0.3)
        
        stack2 = Group(shape1, shape2, shape3, shape4).scale(0.7).next_to(stack1, RIGHT, buff=0.7)
        stack2_text = VGroup(shape_text1, shape_text2, shape_text3, shape_text4).scale(0.7).next_to(stack2, RIGHT, buff=0.2)
        viz_text = Text("Features").scale(0.35).next_to(stack2, UP, buff=0.2)
        # Add animation
        self.play(
            FadeIn(image),
            FadeIn(stack1),
            FadeIn(rfs_text),
            FadeIn(stack2),
            FadeIn(stack2_text),
            FadeIn(viz_text)
        )
        
        self.wait(2)