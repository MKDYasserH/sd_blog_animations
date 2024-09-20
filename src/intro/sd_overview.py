from manim import *
from PIL import Image

def colorize_substring(text):
    parts = text.split("+")
    vg = VGroup(
        Text(parts[0], color=WHITE).scale(0.7),
        Text("+", color=ORANGE).scale(0.4).arrange(RIGHT, buff=0.1),
        Text(parts[1], color=ORANGE).scale(0.4)).arrange(RIGHT, buff=0.1)
    return vg

class SDIntroduction(Scene):
    def construct(self):
        # Input Image and Text
        image_array = np.uint8(Image.open("assets/intro/cat_orig.jpg"))
        image = ImageMobject(image_array).scale(0.35)  # Slightly smaller image
        text = Text("A cat with glasses").scale(0.28).next_to(image, DOWN, buff=1.5)  # Decrease buff

        # Create and Display Encoders (Trapezoids)
        position_list = [[-1, 0, 0], [1, 0.7, 0], [1, 1.4, 0], [-1, 2.1, 0]]
        image_encoder = Polygon(*position_list, color=BLUE, fill_opacity=0.5).scale(0.35)
        text_encoder = Polygon(*position_list, color=GREEN, fill_opacity=0.5).scale(0.35)

        image_encoder.next_to(image, RIGHT, buff=0.6)
        text_encoder.next_to(text, RIGHT, buff=0.6)

        image_encoder_label = Text("Image Encoder").scale(0.25).next_to(image_encoder, UP, buff=0.15)
        text_encoder_label = Text("CLIP Encoder").scale(0.25).next_to(text_encoder, UP, buff=0.15)

        # Input Image and Text into Matrix and Vector
        dummy_matrix = [[0.15, 0.23, 0.89], 
                        [0.75, 0.62, 0.56], 
                        [0.17, 0.34, 0.97]]
        image_matrix = Matrix(dummy_matrix).scale(0.4).next_to(image_encoder, RIGHT, buff=0.6)
        text_vector = Matrix([[0.71, 0.28, 0.43]]).scale(0.35).next_to(text_encoder, RIGHT, buff=0.6)

        # Animate Arrows from Image/Text to Encoders
        arrow_image = Arrow(image.get_right(), image_encoder.get_left(), buff=0.1, color=BLUE)
        arrow_text = Arrow(text.get_right(), text_encoder.get_left(), buff=0.1, color=GREEN)
        arrow_image_matrix = Arrow(image_encoder.get_right(), image_matrix.get_left(), buff=0.1, color=BLUE)
        arrow_text_vector = Arrow(text_encoder.get_right(), text_vector.get_left(), buff=0.1, color=GREEN)

        # Adding noise epsilon
        noise_text = Text("Adding noise").scale(0.35).next_to(image_matrix, UP, buff=0.3)
        
        # Updating the matrix values with noise
        noisy_matrix = [
            ['0.18', '0.29', '0.69'],
            ['0.79', '0.65', '0.50'],
            ['0.14', '0.33', '0.92']]
        
        # Create a new matrix with noise
        new_image_matrix = Matrix(noisy_matrix, element_to_mobject=lambda x: Text(x, color=ORANGE).scale(0.7)).scale(0.4).move_to(image_matrix)

        # Grouping all elements
        all_elements = Group(
            image, text, image_encoder, text_encoder, 
            image_encoder_label, text_encoder_label,
            image_matrix, text_vector, arrow_image, arrow_text, 
            arrow_image_matrix, arrow_text_vector, noise_text, new_image_matrix
        )
        
        
        # Scaling and shifting the group
        all_elements.scale(0.75)  # Scale down
        all_elements.to_corner(LEFT, buff=0.5)  # Move to the top-left corner

        # Adding UNET architecture and corresponding arrows
        unet_image_array = np.uint8(Image.open("assets/intro/unet_architecture.png"))
        unet_image = ImageMobject(unet_image_array).scale(1).next_to(new_image_matrix, RIGHT, buff=0.5).shift(DOWN)
        unet_label = Text("U-NET").scale(0.4).next_to(unet_image, DOWN, buff=0.1)
        text_vector_pos = text_vector.get_right()
        image_mat_pos = new_image_matrix.get_right()
        arrow_unet_tv = Arrow(text_vector_pos, [text_vector_pos[0]+0.7, text_vector_pos[1] + 1.5, 0], color=GREEN, buff=0.1,
                               max_stroke_width_to_length_ratio=1, max_tip_length_to_length_ratio=0.08)
        arrow_unet_mat = Arrow(image_mat_pos, [image_mat_pos[0]+0.7, image_mat_pos[1], 0], color=BLUE, buff=0.1) #

        # Adding time embedding and Scheduler elements
        scheduler_box = Rectangle(height=0.8, width=2.0, fill_color=RED_D, fill_opacity=0.5)
        scheduler_text = Text("Scheduler").scale(0.6).move_to(scheduler_box.get_center())
        scheduler = VGroup(scheduler_box, scheduler_text).scale(0.5).next_to(unet_image, UP, buff=0.6)
        
        timestep = Text("Timestep").scale(0.4).next_to(scheduler, DOWN, buff=0.5)
        timestep_array = Matrix([[0.24, 0.45, 0.76]]).scale(0.35).move_to(timestep)
        arrow_ts_sc = Arrow(scheduler.get_bottom(), timestep.get_top(), color=RED_A, buff=0.1)
        
        predicted_noise_1 = Text("Predicted noise").scale(0.4).next_to(unet_image, UP, buff=0.5).shift(RIGHT*1.35)
        predicted_noise_2 = Text("ε").scale(0.4).next_to(unet_image, UP, buff=0.5).shift(RIGHT*1.35).move_to(predicted_noise_1)
        
        noiseless_latent_1 = Text("Removing noise").scale(0.3).next_to(scheduler, LEFT, buff=0.5)
        noiseless_latent_2 = Text("L - ε").scale(0.4).next_to(scheduler, LEFT, buff=0.5).move_to(noiseless_latent_1)
        # Transform the matrix into the letter "L"
        l_shape = VGroup(Text("L")).scale(0.42).move_to([noiseless_latent_2.get_left()[0]+0.06, *noiseless_latent_2.get_left()[1:]])
        
        unet_left_pos = unet_image.get_left()
        unet_right_pos = unet_image.get_right()
        timestep_pos = timestep_array.get_center()
        arrow_pn_unet = Arrow([unet_right_pos[0]-0.9, unet_right_pos[1]+1.3, 0], predicted_noise_1.get_center(), color=RED_A)
        arrow_nl_scheduler = Arrow(scheduler.get_left(), noiseless_latent_1.get_right(), color=RED_A)
        arrow_scheduler_unet = CurvedArrow([unet_right_pos[0]-0.9, unet_right_pos[1]+1.3, 0], scheduler.get_right(), color=RED_A, stroke_width=1.5, tip_length=0.15)
        arrow_unet_scheduler = CurvedArrow(scheduler.get_left(), [unet_left_pos[0]+0.5, unet_left_pos[1]+1.5, 0], color=RED_A, stroke_width=1.5, tip_length=0.15)
        arrow_unet_timestep = Arrow(timestep_array.get_left(), [unet_left_pos[0]+0.4, timestep_pos[1], 0], color=RED_A,
                               max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.15)
        
        # Adding Decoder 
        latent_array = [['0.25 ', '0.33', '0.99'],
                        ['0.85', '0.72', '0.66'],
                        ['0.27', '0.44', '0.99']]
        latent = Matrix(latent_array).scale(0.3).next_to(unet_image, RIGHT, buff=0.5).shift(UP)
        image_decoder = Polygon(*[[0, 0.7, 0], [0, 1.4, 0], [2, 2.1, 0], [2, 0, 0]], color=BLUE, fill_opacity=0.5).scale(0.28)
        image_decoder.next_to(latent, RIGHT, buff=0.5)
        image_decoder_label = Text("Image Decoder").scale(0.2).next_to(image_decoder, UP, buff=0.15)
        output_image_array = np.uint8(Image.open("assets/intro/cat_output.png"))
        output_image = ImageMobject(output_image_array).scale(0.28).next_to(image_decoder, RIGHT, buff=0.5)
        
        arrow_latent_unet = Arrow([unet_image.get_right()[0], new_image_matrix.get_center()[1], 0], latent.get_left(), color=BLUE, buff=0.1)
        arrow_decoder_latent = Arrow(latent.get_right(), image_decoder.get_left(), color=BLUE, buff=0.1)
        arrow_output_decoder = Arrow(image_decoder.get_right(), output_image.get_left(), color=BLUE, buff=0.1)

        # Displaying Elements
        self.play(FadeIn(image), FadeIn(text))
        self.play(FadeIn(image_encoder), FadeIn(text_encoder), FadeIn(image_encoder_label), 
                  FadeIn(text_encoder_label), GrowArrow(arrow_image), GrowArrow(arrow_text),
                  FadeIn(image_matrix), FadeIn(text_vector), GrowArrow(arrow_image_matrix), GrowArrow(arrow_text_vector))

        self.play(FadeIn(noise_text), Transform(image_matrix, new_image_matrix))
        self.play(FadeOut(noise_text), FadeIn(unet_image), FadeIn(unet_label), GrowArrow(arrow_unet_tv), GrowArrow(arrow_unet_mat))
        self.play(GrowArrow(arrow_pn_unet), FadeIn(predicted_noise_1))
        
        self.play(Transform(predicted_noise_1, predicted_noise_2), FadeIn(scheduler), Transform(arrow_pn_unet, arrow_scheduler_unet))
        self.play(GrowArrow(arrow_nl_scheduler), FadeIn(noiseless_latent_1),
                  FadeIn(timestep), GrowArrow(arrow_ts_sc))
        self.play(Transform(noiseless_latent_1, noiseless_latent_2), ReplacementTransform(new_image_matrix, l_shape), 
                  Transform(arrow_nl_scheduler, arrow_unet_scheduler), Transform(timestep,timestep_array), GrowArrow(arrow_unet_timestep),
                  FadeOut(arrow_unet_mat))
        
        #self.play(FadeIn(scheduler), FadeIn(timestep), GrowArrow(arrow_ts_sc))
        #self.play(Create(arrow_scheduler_unet), Create(arrow_unet_scheduler) )
        self.play(FadeIn(latent), FadeIn(image_decoder), FadeIn(image_decoder_label), FadeIn(output_image),
                  GrowArrow(arrow_latent_unet), GrowArrow(arrow_decoder_latent), GrowArrow(arrow_output_decoder))
        self.wait(2)

