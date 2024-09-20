from manim import *

def apply_shear(pos, degree):
    skew_matrix = np.array([
            [1, degree, 0],  # Skew the x-direction by 0.5 times the y-value
            [0, 1, 0],
            [0, 0, 1]
        ])
    return skew_matrix @ pos

def select_cell(x, y, xstep, ystep, rect):
    x_pos = (y - rect.width/xstep/2) + 0.5
    y_pos = (rect.height/ystep/2 - x) - 0.5
    highlight_square = Square(side_length=1, color=BLUE, fill_opacity=0.5).move_to([x_pos, y_pos, 0])
    return highlight_square

class PaddingStride(Scene):
    def construct(self):      
        
        # Build inclined rectangles
        top_rect1 = Rectangle(width=7, height=5, grid_xstep=1, grid_ystep=1).scale(0.4)
        bottom_rect1 = Rectangle(width=7, height=5, grid_xstep=1, grid_ystep=1).scale(0.4).next_to(top_rect1, DOWN, buff=1.5).shift(RIGHT*0.7, UP*0.3)
        bottom_rect1.set_fill(color=BLACK, opacity=1)
        padded_rect = Rectangle(width=9, height=7, grid_xstep=1, grid_ystep=1).scale(0.4).next_to(top_rect1, DOWN, buff=1.5).shift(RIGHT*0.7, UP*0.7)
        padded_rect.set_fill(color=GRAY, opacity=1)
        
        # Highlighting squares
        highlighted_square1 = Rectangle(width=1, height=1, color=PURPLE, fill_opacity=1).scale(0.35).shift(DOWN/1.3+LEFT*1.25)
        highlighted_square2 = Rectangle(width=1, height=1, color=ORANGE, fill_opacity=1).scale(0.35).shift(DOWN/1.3+LEFT/1.25)
        padding_square = Rectangle(width=1, height=1, color=BLUE, fill_opacity=1).scale(0.35).shift(DOWN*4.4+RIGHT*2.3)
        padding_square_text = Text("Zero padding", color=BLUE).scale(0.35).next_to(padding_square, RIGHT, buff=-1)
        
        # Applying shear
        top_rect1.apply_function(lambda p: apply_shear(p, 0.7))
        highlighted_square1.apply_function(lambda p: apply_shear(p, 0.7))
        highlighted_square2.apply_function(lambda p: apply_shear(p, 0.7))
        bottom_rect1.apply_function(lambda p: apply_shear(p, 0.7))
        padded_rect.apply_function(lambda p: apply_shear(p, 0.7))
        padding_square.apply_function(lambda p: apply_shear(p, 0.7))
        pad_title = Text("With Padding").scale(0.5).next_to(top_rect1, UP, buff=0.7)
        
        # Projection square
        proj_square = Rectangle(width=3, height=3, color=PURPLE, fill_opacity=0.4).scale(0.4).shift(DOWN*4+LEFT/2)
        proj_square.apply_function(lambda p: apply_shear(p, 0.7))
        proj_square2 = Rectangle(width=3, height=3, color=ORANGE, fill_opacity=0.4).scale(0.4).shift(DOWN*4+LEFT/6)
        proj_square2.apply_function(lambda p: apply_shear(p, 0.7))
        
        # Compute the positions of the corners after the shear transformation
        proj_corners = [
            proj_square.get_corner(UL),  # Upper Left
            proj_square.get_corner(UR),  # Upper Right
            proj_square.get_corner(DL),  # Down Left
            proj_square.get_corner(DR)   # Down Right
        ]
        proj_corners2 = [
            proj_square2.get_corner(UL),  # Upper Left
            proj_square2.get_corner(UR),  # Upper Right
            proj_square2.get_corner(DL),  # Down Left
            proj_square2.get_corner(DR)   # Down Right
        ]
        
        # Adjusted Dashed lines from the bottom of the highlighted square to each corner of the projection square
        dashed_lines = VGroup(
            DashedLine(start=highlighted_square1.get_bottom(), end=(proj_corners[0][0]+0.8,proj_corners2[0][1], proj_corners[0][2]), 
                       dash_length=0.1, color=PURPLE),
            DashedLine(start=highlighted_square1.get_bottom(), end=proj_corners[1], dash_length=0.1, color=PURPLE),
            DashedLine(start=highlighted_square1.get_bottom(), end=proj_corners[2], dash_length=0.1, color=PURPLE),
            DashedLine(start=highlighted_square1.get_bottom(), end=(proj_corners[3][0]-0.8,proj_corners[3][1], proj_corners[3][2]), 
                       dash_length=0.1, color=PURPLE)
        )
        
        dashed_lines2 = VGroup(
            DashedLine(start=highlighted_square2.get_bottom(), end=(proj_corners2[0][0]+0.8,proj_corners2[0][1], proj_corners2[0][2]), 
                       dash_length=0.1, color=ORANGE),
            DashedLine(start=highlighted_square2.get_bottom(), end=proj_corners2[1], dash_length=0.1, color=ORANGE),
            DashedLine(start=highlighted_square2.get_bottom(), end=proj_corners2[2], dash_length=0.1, color=ORANGE),
            DashedLine(start=highlighted_square2.get_bottom(), end=(proj_corners2[3][0]-0.8,proj_corners2[3][1], proj_corners2[3][2]), 
                       dash_length=0.1, color=ORANGE)
        )
        
        # Add braces
        brace1 = BraceBetweenPoints(proj_corners[2],(proj_corners[3][0]-0.8,proj_corners[3][1], proj_corners[3][2]))
        brace2 = BraceBetweenPoints(proj_corners[2], (proj_corners[0][0]+0.8,proj_corners[0][1], proj_corners[0][2]), LEFT)
        brace2.apply_function(lambda p: apply_shear(p, 0.7)).shift(RIGHT*3.2)
        brace_text1 = MathTex(r'f_{\text{w}}=3').scale(0.5).next_to(brace1, DOWN, buff=0.1)
        brace_text2 = MathTex(r'f_{\text{h}}=3').scale(0.5).next_to(brace2, LEFT, buff=0.1)
        
        # Add dimensions
        dim1 = MathTex(r"(5\times 7)").scale(0.5).next_to(top_rect1, RIGHT, buff=0.5)
        dim2 = MathTex(r"(5\times 7)").scale(0.5).next_to(dim1, DOWN, buff=3)
        
        pad_elements = Group(pad_title, top_rect1, bottom_rect1, padded_rect,highlighted_square1, highlighted_square2, 
                               proj_square2, proj_square, dashed_lines, dashed_lines2, padding_square_text,
                                brace1, brace_text1, brace2, brace_text2, dim1, dim2, padding_square)
        pad_elements.to_corner(LEFT+UP).scale(0.75)
        
       
        # Add data box
        info_box = Rectangle(height=2, width=1.5).shift(DOWN/4+RIGHT*5.5)
        info_text1 = MathTex(r"\text{Stride}=1")
        info_text2 = MathTex(r"\text{Padding}=1")
        info_text3 = MathTex(r"\text{input}_{\text{h}}=5")
        info_text4 = MathTex(r"\text{input}_{\text{w}}=7")
        info_text = VGroup(info_text1, info_text2, info_text3, info_text4)
        info_text.arrange(DOWN, buff=0.5).scale(0.4).move_to(info_box.get_center())
        
        # Output size formula
        formula = MathTex(r"\text{output}_{\text{w}/\text{h}} = \frac{\text{input}_{\text{w}/\text{h}} - f_{\text{w}/\text{h}} + 2\times \text{Padding}}{\text{Stride}} + 1")
        formula.scale(0.4).next_to(info_box, LEFT, buff=0.5)
        
        # Arrows
        arrow1 = CurvedArrow(dim2.get_right(), formula.get_bottom(), stroke_width=1, tip_length=0.15)
        arrow2 = CurvedArrow(formula.get_top(), dim1.get_right(), stroke_width=1, tip_length=0.15)
        arrow3 = Arrow(padding_square.get_right(), padding_square_text.get_left(), color=BLUE)
        
       
        self.play(FadeIn(padded_rect), FadeIn(top_rect1), FadeIn(bottom_rect1), FadeIn(highlighted_square1), 
                  FadeIn(highlighted_square2), FadeIn(proj_square2), FadeIn(dashed_lines2),
                  FadeIn(proj_square), FadeIn(dashed_lines), FadeIn(pad_title))
        self.play(FadeIn(brace1), FadeIn(brace_text1), FadeIn(brace2), FadeIn(brace_text2), 
                  FadeIn(dim1), FadeIn(dim2), FadeIn(info_box), FadeIn(info_text), FadeIn(formula),
                  FadeIn(arrow1), FadeIn(arrow2), FadeIn(padding_square), FadeIn(padding_square_text), GrowArrow(arrow3))
        
        self.wait(2)