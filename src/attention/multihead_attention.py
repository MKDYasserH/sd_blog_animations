from manim import *

class MultiHeadAttn(Scene):
    def construct(self):
        # Step 1: Create Q, K, and V rectangles
        q_rect = self.create_rectangle_with_text("Q", color=GRAY_BROWN)
        k_rect = self.create_rectangle_with_text("K", color=GRAY_BROWN)
        v_rect = self.create_rectangle_with_text("V", color=GRAY_BROWN)

        # Arrange Q, K, and V horizontally
        qkv_group = VGroup(q_rect, k_rect, v_rect).scale(0.5).arrange(RIGHT, buff=0.5)
        qkv_group.to_edge(LEFT+DOWN*2.5)  # Position Q, K, V at the left

        # Step 2: Create the Split rectangle
        split_rect = self.create_rectangle_with_text("Split", color=GOLD_B).scale(0.5)
        split_rect.next_to(qkv_group, UP, buff=0.5)

        # Step 3: Create a stack of Q, K, V rectangles after split
        q_stack, _ = self.create_rectangle_with_text("Q", color=GRAY_BROWN, stack=True)
        k_stack, _= self.create_rectangle_with_text("K", color=GRAY_BROWN, stack=True)
        v_stack, brace1 = self.create_rectangle_with_text("V", color=GRAY_BROWN, stack=True)
        stack_group = VGroup(q_stack, k_stack, v_stack).scale(0.5).arrange(RIGHT, buff=0.5)
        stack_group.next_to(split_rect, UP, buff=0.5)

        # Step 4: Create Scaled Dot-Product Attention rectangle
        attn_rect, brace2 = self.create_rectangle_with_text("Scaled Dot-Product\nAttention", color=PURPLE_C, stack=True)
        attn_rect.scale(0.5)
        attn_rect.next_to(stack_group, UP, buff=0.5)

        # Step 5: Create the Concat rectangle
        concat_rect = self.create_rectangle_with_text("Concat", color=GOLD_B).scale(0.5)
        concat_rect.next_to(attn_rect, UP, buff=0.5)
        
        # Step 5: linear
        linear_rect = self.create_rectangle_with_text("Linear", color=MAROON_C).scale(0.5)
        linear_rect.next_to(concat_rect, UP, buff=0.5)

        # Step 6: Create arrows between elements
        arrow1 = Arrow(start=qkv_group.get_top(), end=split_rect.get_bottom(), buff=0.1)
        arrow2 = Arrow(start=split_rect.get_top(), end=stack_group.get_bottom(), buff=0.1)
        arrow3 = Arrow(start=stack_group.get_top(), end=attn_rect.get_bottom(), buff=0.1)
        arrow4 = Arrow(start=attn_rect.get_top(), end=concat_rect.get_bottom(), buff=0.1)
        arrow5 = Arrow(start=concat_rect.get_top(), end=linear_rect.get_bottom(), buff=0.1)
        
        # Adjusting position of braces
        brace1.scale(0.5).next_to(v_stack.get_bottom(), RIGHT, buff=0.2).shift(UP*0.1)
        brace2.scale(0.5).next_to(attn_rect.get_bottom(), RIGHT, buff=0.2).shift(RIGHT*1.2, UP*0.1)

        # Step 7: Add elements to the scene
        self.add(qkv_group, split_rect, stack_group, attn_rect, concat_rect, linear_rect,
                 arrow1, arrow2, arrow3, arrow4, arrow5, brace1, brace2)

    def create_rectangle_with_text(self, text, color=WHITE, stack=False):
        """Creates a rectangle with a given text label and a 3D stack effect."""
        # Create label and rectangle with original dimensions
        label = Text(text)
        rect = Rectangle(width=label.width + 0.5, height=label.height + 0.5)
        rect.set_fill(color, opacity=0.8)
        rect.set_stroke(WHITE, width=1)
        rect.move_to(label.get_center())
        rect_text = VGroup(rect, label)

        if stack:
            stack_group = VGroup(rect_text)
            # Create stack layers with small offsets for a 3D effect
            for i in range(1, 3):
                layer = rect.copy()
                layer.shift(UP * i * 0.3 + RIGHT * i * 0.3)  # Shift slightly up and to the right
                layer.set_z_index(-i)  # Use the z-index specified in your code
                layer.set_opacity(0.5 - i * 0.1)
                stack_group.add(layer)

            # Calculate points for the brace between the corners
            top_right_corner = rect_text.get_corner(DR)  # Down-right corner of the top layer
            bottom_right_corner = stack_group[-1].get_corner(DR)  # Down-right corner of the last layer

            # Create a diagonal brace between the calculated points
            brace = BraceBetweenPoints(top_right_corner, bottom_right_corner)
            brace_text = MathTex(r"n_{heads}").next_to(brace, RIGHT, buff=0.5)
            brace_group = VGroup(brace, brace_text)

            return stack_group, brace_group

        return rect_text

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = MultiHeadAttn()
        scene.render()