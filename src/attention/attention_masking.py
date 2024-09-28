from manim import *
import numpy as np
from scipy.special import softmax

np.set_printoptions(precision=2)

class AttentionMasking(Scene):
    def construct(self):
        self.mat = np.random.normal(size=(5,5))
        # Define a sentence as a list of Tex objects for each word
        self.sentence = "Building AI models is cool"
        text_sentence = Text(self.sentence).scale(0.5)
        tex_sentence = Tex(*self.sentence.split(" "))
        text_sentence.to_edge(UP, buff=2)
        sequences = self.build_sentence_mask(tex_sentence)

        # Arrange all sequences vertically and align them to the left
        sequences.arrange(DOWN, buff=0.5).scale(0.6)
        sequences.to_edge(LEFT, buff=0.1)

        # Align each sequence to the left edge
        for sequence in sequences:
            sequence.align_to(sequences, LEFT)
            
        # adding mask matrix
        unm_attn, self.mat = self.get_matrix(self.mat, True)
        self.mat = softmax(self.mat, axis=0)
        nm_attn, self.mat = self.get_matrix(self.mat, False)
        cells = nm_attn.get_entries()
        for cell in cells:
            if cell.tex_string == "0.0":
                cell.set_color(ORANGE)
        
        unm_attn.scale(0.35).next_to(sequences, RIGHT, buff=1)
        nm_attn.scale(0.38).next_to(unm_attn, RIGHT, buff=0.8).shift(DOWN*0.1)
        arrow = Arrow(unm_attn.get_right(), [nm_attn.get_left()[0], nm_attn.get_left()[1]+0.1, 0], 
                      buff=0.1, max_stroke_width_to_length_ratio=8)
        arrow_text = Text("Softmax").scale(0.35).next_to(arrow, UP, buff=0.1)
        
        # Add the sequences to the scene
        self.add(text_sentence, sequences,unm_attn, nm_attn, arrow, arrow_text)
        

    def get_tokens(self, target_index):
        sentence = Tex(*"Building AI models is cool".split(" "))
        
        token_rects_group = VGroup()
        # Create rectangles and align with tokens up to the target index
        for token in sentence[:target_index]:
            
            # Create a rectangle that fits around the word
            rect = Rectangle(width=token.width+0.2, height=0.6)
            rect.set_fill(GREY, opacity=0.5)
            rect.set_stroke(GREY, width=1)

            # Use `rect.surround(word)` instead of `rect.move_to(word.get_center())`
            rect.move_to(token.get_center())
            token_rects_group.add(VGroup(rect, token))
        return token_rects_group
    
    def build_sentence_mask(self, general_sentence):
        # Create a group to hold all sequences
        sequences = VGroup()
        # Generate each line, excluding the last word because it's the predicted word
        for idx in range(1, len(general_sentence)):
            token_rects_group = self.get_tokens(idx)
            # Arrange words and rectangles horizontally
            token_rects_group.arrange(RIGHT, buff=0.1).scale(0.75)

            # Create a question mark with a corresponding rectangle
            question_mark = Tex("??")
            question_rect = Rectangle(width=question_mark.width + 0.2, height=0.4)
            question_rect.set_fill(ORANGE, opacity=0.5)
            question_rect.set_stroke(ORANGE, width=1)
            
            # Align rectangle around the question mark
            question_rect.surround(question_mark)
            question_mark_group = VGroup(question_rect, question_mark)
            question_mark_group.next_to(token_rects_group, RIGHT, buff=0.5)
            
            # Create an arrow pointing to the question mark
            arrow = Arrow(token_rects_group.get_right(), question_mark_group.get_left(), buff=0.1,max_stroke_width_to_length_ratio=8)
            
            # Create a complete sequence group
            sequence = VGroup(token_rects_group, arrow, question_mark_group)
            sequences.add(sequence)
        return sequences

    def get_matrix(self, mat, masking=False):
        mat = np.around(mat, 2)
        if masking==True:
            m = np.asanyarray(mat).T
            mask = np.tri(*m.shape[-2:], k=-1, dtype=bool)
            mat = np.where(mask, float('-inf'), m)
            
        mat_table = MathTable(mat, include_outer_lines=True)
        
        if masking==True:
            cells = mat_table.get_entries()
            for cell in cells:
                if cell.tex_string == "{}".format(float('-inf')):
                    cell.become(MathTex(r"-\infty").move_to(cell))
                    cell.set_color(ORANGE)
            
            # Create word labels for the outer rows and columns
            # Top row labels
            top_labels = VGroup(*[Tex(word) for word in self.sentence.split(" ")])
            
            # Left column labels
            left_labels = VGroup(*[Tex(word) for word in self.sentence.split(" ")])

            # Position top labels above the corresponding matrix columns
            for i, label in enumerate(top_labels):
                label.next_to(mat_table.get_cell((1, i + 1)), UP, buff=0.3)

            # Position left labels to the left of the corresponding matrix rows
            for i, label in enumerate(left_labels):
                label.next_to(mat_table.get_cell((i + 1, 1)), LEFT, buff=0.3)

            # Group the matrix and labels together
            mat_table = VGroup(mat_table, top_labels, left_labels)
        return mat_table, mat
    
    
if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = AttentionMasking()
        scene.render()