from manim import *
import nltk
from nltk import word_tokenize, regexp_tokenize
from itertools import cycle

BASE_COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW]

class Tokenization(Scene):
    def construct(self):
        input_text = "Elementary, my dear Watson"
        
        # Display word, character, and subword tokenizations
        word_tokens = self.get_tokens(input_text, "word")
        self.display_tokens(word_tokens, method="word")

        character_tokens = self.get_tokens(input_text, "character")
        self.display_tokens(character_tokens, method="character")

        subword_tokens = self.get_tokens(input_text, "subword")
        self.display_tokens(subword_tokens, method="subword")
        
    
    def get_tokens(self, input_text, method):
        if method == "word":
            tokens = word_tokenize(input_text)
        elif method == "character":
            tokens = regexp_tokenize(input_text, r"[^\s]")  # Matches any character including whitespace
        elif method == "subword":
            tokens = ["Element", "ary", ",", "my", "dear", "Watson"]
        else:
            tokens = []  # If method is unrecognized, return an empty list
        return tokens
    
    def display_tokens(self, tokens, method):
        # Create text objects for tokens
        token_obj = Tex(*tokens)

        # Fixed size for rectangles to keep all tokens aligned
        rect_height = 0.6  # Set a uniform height for all rectangles
        rectangles = []
        color_cycle = cycle(BASE_COLORS)
        for color, token_text in zip(color_cycle,token_obj):
            rect_width = token_text.width #+ 0.2  # Add slight padding to the width
            rect = Rectangle(width=rect_width, height=rect_height)
            if method == "character":
                rect.set_fill(color, opacity=0.5)  # Fill color with 50% opacity
                rect.set_stroke(color, width=1)  # Set the stroke/border
            else:
                rect.set_fill(self.get_color(token_text, BASE_COLORS), opacity=0.5)  # Fill color with 50% opacity
                rect.set_stroke(self.get_color(token_text, BASE_COLORS), width=1) 
            rect.move_to(token_text.get_center())  # Align the rectangle with the token
            rectangles.append(rect)
        
        for rect in rectangles[1:]:
            rect.align_to(rectangles[0], UP)

        # Group tokens with their rectangles
        token_rects_group = VGroup(*[VGroup(token_text, rect) for token_text, rect in zip(token_obj, rectangles)]).scale(0.75)
        
        # Position token groups vertically based on method type
        text_method = Text(f"{method} tokenization :").scale(0.5)
        if method == "word":
            token_rects_group.shift(UP)
        elif method == "character":
            token_rects_group.shift(UP * 0)  # Align at center of the screen
        elif method == "subword":
            token_rects_group.shift(DOWN)
        text_method.next_to(token_rects_group, LEFT, buff=0.5)
        # Display on the scene
        self.play(Create(token_rects_group), FadeIn(text_method))
        self.wait(1)

    def get_color(self, token, colors):
        # Assign colors based on token similarity (this is a simple hash-based method)

        return colors[hash(token) % len(colors)]

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = Tokenization()
        scene.render()