from manim import *

class MultiHeadAttn(Scene):
    def construct(self):
        # Step 1: Create Q, K, and V rectangles
        q_rect = self.create_rectangle_with_text("Q", color=BLUE, stack=True)
        k_rect = self.create_rectangle_with_text("K", color=GREEN)
        v_rect = self.create_rectangle_with_text("V", color=RED)

        # Arrange Q, K, and V horizontally
        qkv_group = VGroup(q_rect, k_rect, v_rect).arrange(RIGHT, buff=0.5)
        qkv_group.to_edge(LEFT)  # Position Q, K, V at the left

        # Step 2: Create the Split rectangle
        split_rect = self.create_rectangle_with_text("Split", color=YELLOW)
        split_rect.next_to(qkv_group, RIGHT, buff=1)

        # Step 3: Create a stack of Q, K, V rectangles after split
        q_stack = self.create_rectangle_with_text("Q", color=BLUE)
        k_stack = self.create_rectangle_with_text("K", color=GREEN)
        v_stack = self.create_rectangle_with_text("V", color=RED)
        stack_group = VGroup(q_stack, k_stack, v_stack).arrange(DOWN, buff=0.1)
        stack_group.next_to(split_rect, RIGHT, buff=1)

        # Step 4: Create Scaled Dot-Product Attention rectangle
        attn_rect = self.create_rectangle_with_text("Scaled Dot-Product\nAttention", color=PURPLE)
        attn_rect.next_to(stack_group, RIGHT, buff=1)

        # Step 5: Create the Concat rectangle
        concat_rect = self.create_rectangle_with_text("Concat", color=ORANGE)
        concat_rect.next_to(attn_rect, RIGHT, buff=1.5)

        # Step 6: Create arrows between elements
        arrow1 = Arrow(start=qkv_group.get_right(), end=split_rect.get_left(), buff=0.1)
        arrow2 = Arrow(start=split_rect.get_right(), end=stack_group.get_left(), buff=0.1)
        arrow3 = Arrow(start=stack_group.get_right(), end=attn_rect.get_left(), buff=0.1)
        arrow4 = Arrow(start=attn_rect.get_right(), end=concat_rect.get_left(), buff=0.1)

        # Step 7: Add elements to the scene
        self.add(qkv_group, split_rect, stack_group, attn_rect, concat_rect, arrow1, arrow2, arrow3, arrow4)

    def create_rectangle_with_text(self, text, color=WHITE, stack=False):
        """Creates a rectangle with a given text label and a 3D stack effect."""
        rect = Rectangle(width=2, height=1.2)
        rect.set_fill(color, opacity=0.5)
        rect.set_stroke(color, width=1)
        label = Text(text).move_to(rect.get_center())
        rect_text = VGroup(rect, label)

        if stack:
            stack_group = VGroup()
            # Create multiple layers with small offsets for a 3D effect
            for i in range(3):
                layer = rect_text.copy()
                layer.shift(UP * i * 0.1 + RIGHT * i * 0.1)  # Shift slightly up and to the right
                layer.set_z_index(i)  # Ensure correct layering order
                layer[0].set_opacity(0.5 - i * 0.1)  # Adjust opacity for depth perception
                stack_group.add(layer)
            return stack_group

        return rect_text