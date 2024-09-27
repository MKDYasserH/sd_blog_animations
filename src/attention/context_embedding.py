from manim import *
from PIL import Image

class ContextEmbedding(ThreeDScene):
    def construct(self):
        axes_config = dict(
                x_range=(-5, 5, 1),
                y_range=(-5, 5, 1),
                z_range=(-3, 3, 1),
                x_length=10,
                y_length=6,
                z_length=4,
                tips=False
            )
        pool1 = Image.open("assets/conv_attn/pool_relax.jpg")
        pool1 = ImageMobject(pool1).scale(0.08)
        pool2 = Image.open("assets/conv_attn/pool_cue.jpeg")
        pool2 = ImageMobject(pool2).scale(0.6)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-120 * DEGREES)
        axes, xy_plane = self.plot_graph(axes_config)
        
        # Shift the axes and the plane together
        axes.shift(LEFT*2,DOWN*5.5)
        xy_plane.shift(LEFT*2,DOWN*5.5)
        self.add(axes, xy_plane)
        
        # Add tokens and corresponding embeddings
        tokens1 = self.get_tokens("I relaxed in the pool", "pool", YELLOW)
        embeddings1 = self.get_embeddings(tokens1, "pool", YELLOW)
        tokens2 = self.get_tokens("He plays pool like a pro", "pool", ORANGE)
        embeddings2 = self.get_embeddings(tokens2, "pool", ORANGE)
        tokens_embeds1 = VGroup(*[VGroup(token, embed).arrange(DOWN, buff=0.6) for token, embed in zip(tokens1, embeddings1)]).arrange(RIGHT, buff=0.05)
        tokens_embeds2 = VGroup(*[VGroup(token, embed).arrange(DOWN, buff=0.6) for token, embed in zip(tokens2, embeddings2)]).arrange(RIGHT, buff=0.05)
        tokens = VGroup(tokens_embeds1, tokens_embeds2)
        tokens.arrange(RIGHT, buff=1.5).shift(UP*2.5)
        
        # Add arrows between each token and its embedding
        # Additionally, adds the vector corresponding to the target word
        arrows = VGroup()
        for token, embed in zip(tokens1, embeddings1):
            arrow = Arrow(token.get_bottom(), embed.get_top(), buff=0.1, color=WHITE)
            if token[0].tex_string == "pool":
                arrow.set_color(YELLOW)
                
                # Extract embedding coordinates from the matrix
                pool_embedding_matrix = embed.get_entries()
                pool_embedding_vector = np.array([float(pool_embedding_matrix[i].get_tex_string()) for i in range(3)])
                # Add vector corresponding to the embedding
                vector = Arrow(start=axes.c2p(0, 0, 0), end=axes.c2p(*pool_embedding_vector), stroke_width=2, 
                               max_tip_length_to_length_ratio=0.1,buff=-1)
                #vector.shift(LEFT*2,DOWN*5.5)
                vector.set_color(YELLOW)
                pool1.next_to(vector.get_end(), UP, buff=0.3)
                self.add(vector, pool1)
                
            arrows.add(arrow)
        
        for token, embed in zip(tokens2, embeddings2):
            arrow = Arrow(token.get_bottom(), embed.get_top(), buff=0.1, color=WHITE)
            if token[0].tex_string == "pool":
                arrow.set_color(ORANGE)
                
                # Extract embedding coordinates from the matrix
                pool_embedding_matrix = embed.get_entries()
                pool_embedding_vector = np.array([float(pool_embedding_matrix[i].get_tex_string()) for i in range(3)])
                # Add vector corresponding to the embedding
                vector = Arrow(start=axes.c2p(0, 0, 0), end=axes.c2p(*pool_embedding_vector), stroke_width=2, 
                               max_tip_length_to_length_ratio=0.1,buff=-1)
                #vector.shift(LEFT*2,DOWN*5.5)
                vector.set_color(ORANGE)
                pool2.next_to(vector.get_end(), UP, buff=0.3)
                self.add(vector, pool2)
                
            arrows.add(arrow)
        
        self.add_fixed_in_frame_mobjects(tokens, arrows)
        
        
        self.wait(1)
    
    def plot_graph(self, config):
        # Create 3D axes
        axes = ThreeDAxes(**config)
        
        # Create a number plane with the same x and y range as the axes
        xy_plane = NumberPlane(
            x_range=config["x_range"], 
            y_range=config["y_range"],
            x_length=config["x_length"],
            y_length=config["y_length"]
        )
        
        # Make sure the plane is positioned at the same origin as the axes
        xy_plane.move_to(axes.c2p(0, 0, 0))

        return axes, xy_plane
    
    def get_tokens(self, sentence, target, color):
        sentence_tokens = Tex(*sentence.split(" "))
        rectangles = []
        for token in sentence_tokens:
            rect_width = token.width #+ 0.2  # Add slight padding to the width
            rect = Rectangle(width=rect_width, height=0.6)
            if token.tex_string == target:
                rect.set_fill(color, opacity=0.5)
                rect.set_stroke(color, width=1)
            else:
                rect.set_fill(GREY, opacity=0.5)
                rect.set_stroke(GREY, width=1)
            
            rect.move_to(token.get_center())  # Align the rectangle with the token
            rectangles.append(rect)
        
        for rect in rectangles[1:]:
            rect.align_to(rectangles[0], UP)
        
        # Group tokens with their rectangles
        token_rects_group = VGroup(*[VGroup(token_text, rect) for token_text, rect in zip(sentence_tokens, rectangles)])
        token_rects_group.arrange(buff=0.1).scale(0.75)
        return token_rects_group
    
    def get_embeddings(self, tokens, target, color):
        embeddings_list = []
        for i in range(len(tokens)):
            embedding = np.random.randint(-2, 2, 3)
            embedding = [[ele] for ele in embedding]
            if tokens[i][0].tex_string == target:
                embedding = [[ele] for ele in [np.random.randint(-2,3), 0, np.random.randint(1,3)]]
                embeddings_list.append(Matrix(embedding).set_color(color).scale(0.45))
            else:
                embeddings_list.append(Matrix(embedding).scale(0.45))
        return VGroup(*embeddings_list)
    
if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = ContextEmbedding()
        scene.render()