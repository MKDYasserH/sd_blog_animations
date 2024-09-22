from manim import *
import numpy as np
from itertools import cycle
from sklearn.decomposition import PCA


class SimpleEmbedding(ThreeDScene):
        def construct(self):
            # Words for embedding visualization
            text_list = ["elementary", "dear", "watson"]
            embeddings = [[-2, 0, 1], [-1, 0, -3], [2, 0, 2]]

            # Titles and words setup
            title1 = Text("Words").scale(0.7).to_corner(UL, buff=1)
            title2 = Text("Embedding Space").scale(0.7).next_to(title1, RIGHT, buff=5)  # Place on the right
            text_group = VGroup(*[Text(text, color=YELLOW).scale(0.5) for text in text_list]).arrange(DOWN, buff=0.5).next_to(title1, DOWN, buff=1.5)

            # Create arrow between titles
            arrow = Arrow(title1.get_right(), title2.get_left(), buff=0.3)

            # Configure 3D axes
            axes_config = dict(
                x_range=(-5, 5, 1),
                y_range=(-5, 5, 1),
                z_range=(-4, 4, 1),
                x_length=6,
                y_length=6,
                z_length=4,
            )

            # Create 3D axes and place it on the right near "Embeddings" title
            axes = ThreeDAxes(**axes_config).next_to(text_group,RIGHT).shift(RIGHT*2, UP*2)
            axes.scale(0.75)

            # Add the fixed titles, words, and arrow (they won't rotate with the camera)
            self.add_fixed_in_frame_mobjects(title1, title2, text_group, arrow)

            # Add the 3D axes and vectors (they will rotate with the camera)
            self.add(axes)

            # Loop through text list to add vectors and labels at the embeddings
            for text, text_embed in zip(text_list, embeddings):
                vector = Arrow(start=axes.c2p(0, 0, 0), end=axes.c2p(*text_embed), stroke_width=1.5, tip_length=0.1, buff=-1).set_color(YELLOW)
                label = Text(text, color=YELLOW).scale(0.35).next_to(vector.get_end(), UP)
                self.add_fixed_orientation_mobjects(label)  # Keep the label's orientation fixed
                self.add(vector)

            # Set camera angle for rotation and ambient rotation for 3D effect
            self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)  # Rotate camera for 3D effect
            self.wait(1)

        


if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = SimpleEmbedding()
        scene.render()