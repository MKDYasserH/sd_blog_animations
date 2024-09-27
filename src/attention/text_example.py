from manim import *

class TextExample(Scene):
    def construct(self):
        # Short text example
        short_title = Text("Encoder-Decoder Attention")
        short_text_en = "He plays pool like a pro"
        short_text_fr = "Il joue au billard ..."
        short_group = VGroup()
        
        long_group = VGroup()
        # Paragraph of text
        long_text = "You are a wizard Harry"
        long_text = Tex(*long_text.split(" ")).arrange(RIGHT, buff=0.2)
        long_group.add(long_text)
        for word in long_text:
            if word.tex_string != "Harry":
                arrow = Line(word.get_top(), long_text[4].get_top(), stroke_width=0.5, path_arc=-120*DEGREES).set_color(GOLD)
                long_group.add(arrow)
        long_text[4].set_color(GOLD)
        
        # Position words on the screen
        short_text_en = Tex(*short_text_en.split(" ")).arrange(RIGHT, buff=0.2)
        short_text_fr = Tex(*short_text_fr.split(" ")).arrange(RIGHT, buff=0.2)
        short_text_fr.next_to(short_text_en, RIGHT, buff=1)
        short_text_arrow = Arrow(short_text_en.get_right(), short_text_fr.get_left())
        encoder_brace = BraceBetweenPoints(short_text_en.get_corner(DL), short_text_en.get_corner(DR))
        encoder_title = Text("Encoder").scale(0.5).next_to(encoder_brace, DOWN, buff=0.5)
        decoder_brace = BraceBetweenPoints(short_text_fr.get_corner(DL), short_text_fr.get_corner(DR))
        decoder_title = Text("Decoder").scale(0.5).next_to(decoder_brace, DOWN, buff=0.5)
        short_group.add(short_text_en, short_text_fr, short_text_arrow, encoder_brace, encoder_title,
                        decoder_brace, decoder_title)
        
        short_text_fr[3].set_color(GOLD)
        
        for word in short_text_en:
            if word.tex_string != "pool":
                arrow = Line(word.get_top(), short_text_fr[3].get_top(), stroke_width=0.5, path_arc=-120*DEGREES).set_color(GOLD)
                short_group.add(arrow)
            else:
                arrow = Line(word.get_top(), short_text_fr[3].get_top(), stroke_width=2.5, path_arc=-120*DEGREES).set_color(GOLD)
                short_group.add(arrow)
        
        short_group.shift(LEFT*6.5).scale(0.5)
        short_title.next_to(short_group, UP, buff=0.5).scale(0.5)
        long_title = Text("Self-Attention").scale(0.5).next_to(short_title, RIGHT, buff=3.5)
        long_group.next_to(short_group, RIGHT, buff=1).scale(0.5)
        v_line = Line(short_group.get_left(), long_group.get_right()).rotate(90*DEGREES)
        v_line.scale(0.4).shift(RIGHT*1.5)
        
        self.add(short_group, short_title, long_group, long_title, v_line)
        
        
        

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = TextExample()
        scene.render()