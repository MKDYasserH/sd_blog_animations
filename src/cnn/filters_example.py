from manim import *
from PIL import Image

SHARPEN_KERNEL = np.array([
                    [0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]
                ])

GAUSSIAN_KERNEL = np.array([
                    [1, 2, 1],
                    [2,  4, 2],
                    [1, 2, 1]
                ])
    

class ImageFilterConvolution(Scene):
    def construct(self):
        # Input Image
        input_image = Image.open("assets/conv_attn/no_filter.jpg")
        input_image = ImageMobject(input_image).scale(2).to_edge(DOWN, buff=0.3) # Slightly smaller image
        input_image.shift(LEFT*3)
        output_image = Image.open("assets/conv_attn/gaussian_blur.png")
        output_gaussian_image = ImageMobject(output_image).scale(2).next_to(input_image, UP, buff=0.7)
        
        header_text = Text("Blurring").scale(0.4).next_to(output_gaussian_image, UP, buff=0.3)
        
        # Create the grid overlay
        # Define grid size
        grid_rows, grid_cols = 6, 6  # Example grid size (can adjust)
        
        # Create the grid overlay
        grid = self.create_grid(input_image, grid_rows, grid_cols, input_image.height, input_image.width)
        

        cell_height, cell_width = self.get_grid_cell_height(grid, grid_rows), self.get_grid_cell_width(grid, grid_rows)
        
        # Create and add the kernel matrix (Emboss kernel)
        kernel_matrix = self.create_kernel_matrix(GAUSSIAN_KERNEL)
        kernel_size = 3  # 3x3 kernel size
        
        kernel_matrix.scale_to_fit_height(kernel_size * cell_height)  # Make kernel cover 3x3 cells
        kernel_matrix.scale_to_fit_width(kernel_size * cell_width) # Make kernel
        kernel_matrix.move_to(self.get_grid_corner(grid, grid_rows, cell_height, cell_width, kernel_size))
        
        # Create the grid for the output image
        output_cols = self.get_output_size(grid_cols, kernel_size)
        output_rows = self.get_output_size(grid_rows, kernel_size)
        output_grid = self.create_grid(output_gaussian_image, output_rows, output_cols, 
                                       output_gaussian_image.height, output_gaussian_image.width)
        
        output_cell_height = self.get_grid_cell_height(output_grid, output_rows) 
        output_cell_width = self.get_grid_cell_width(output_grid, output_cols) 
        
        output_mask = self.create_mask(output_grid, output_rows, output_cols, output_cell_width, output_cell_height)
        
        # Meta Data
        input_size_text = MathTex(r"(6\times 6)").scale(0.45).next_to(grid, RIGHT, buff=0.5)
        output_size_text = MathTex(r"(4\times 4)").scale(0.45).next_to(input_size_text, UP, buff=3)
        
        # Arrow
        io_arrow = Arrow(input_image.get_top(), output_gaussian_image.get_bottom(), stroke_width=6)
        
        kernel_matrix_text = Text("Gaussian Blur Filter").scale(0.3).next_to(kernel_matrix, LEFT, buff=0.3)
        
        all_elements = Group(input_image, output_gaussian_image, grid, output_mask, output_grid, input_size_text, output_size_text, header_text)
        all_elements.scale(1)
        

        
        ## SHARPEN
        # Input Image
        sharpen_input_image = Image.open("assets/conv_attn/no_filter.jpg")
        sharpen_input_image = ImageMobject(sharpen_input_image).scale(2).next_to(input_image, RIGHT, buff=3) # Slightly smaller image
        sharpen_output_image = Image.open("assets/conv_attn/sharpen.png")
        sharpen_output_image = ImageMobject(sharpen_output_image).scale(2).next_to(sharpen_input_image, UP, buff=0.7)
        
        sharpen_header_text = Text("Sharpening").scale(0.4).next_to(sharpen_output_image, UP, buff=0.3)
        
        # Create the grid overlay
        # Define grid size
        grid_rows, grid_cols = 6, 6  # Example grid size (can adjust)
        
        # Create the grid overlay
        sharpen_grid = self.create_grid(sharpen_input_image, grid_rows, grid_cols, sharpen_input_image.height, sharpen_input_image.width)
        

        sharpen_cell_height, sharpen_cell_width = self.get_grid_cell_height(sharpen_grid, grid_rows), self.get_grid_cell_width(sharpen_grid, grid_rows)
        
        # Create and add the kernel matrix (Emboss kernel)
        sharpen_kernel_matrix = self.create_kernel_matrix(SHARPEN_KERNEL, v_buff=1)
        sharpen_kernel_size = 3  # 3x3 kernel size
        
        sharpen_kernel_matrix.scale_to_fit_height(sharpen_kernel_size * sharpen_cell_height)  # Make kernel cover 3x3 cells
        sharpen_kernel_matrix.scale_to_fit_width(sharpen_kernel_size * sharpen_cell_width) # Make kernel
        sharpen_kernel_matrix.move_to(self.get_grid_corner(sharpen_grid, grid_rows, sharpen_cell_height, sharpen_cell_width, sharpen_kernel_size))
        
        # Create the grid for the output image
        sharpen_output_cols = self.get_output_size(grid_cols, sharpen_kernel_size)
        sharpen_output_rows = self.get_output_size(grid_rows, sharpen_kernel_size)
        sharpen_output_grid = self.create_grid(sharpen_output_image, sharpen_output_rows, sharpen_output_cols, 
                                       sharpen_output_image.height, sharpen_output_image.width)
        
        sharpen_output_cell_height = self.get_grid_cell_height(sharpen_output_grid, sharpen_output_rows) 
        sharpen_output_cell_width = self.get_grid_cell_width(sharpen_output_grid, sharpen_output_cols) 
        
        sharpen_output_mask = self.create_mask(sharpen_output_grid, sharpen_output_rows, sharpen_output_cols, sharpen_output_cell_width, sharpen_output_cell_height)
        
        # Meta Data
        sharpen_input_size_text = MathTex(r"(6\times 6)").scale(0.45).next_to(sharpen_grid, RIGHT, buff=0.5)
        sharpen_output_size_text = MathTex(r"(4\times 4)").scale(0.45).next_to(sharpen_input_size_text, UP, buff=3)
        
        # Arrow
        sharpen_io_arrow = Arrow(sharpen_input_image.get_top(), sharpen_output_image.get_bottom(), stroke_width=6)
        
        sharpen_kernel_matrix_text = Text("Sharpening Filter").scale(0.3).next_to(sharpen_kernel_matrix, LEFT, buff=0.3)
        
        sharpen_all_elements = Group(sharpen_input_image, sharpen_output_image, sharpen_grid, sharpen_output_mask, 
                                     sharpen_output_grid, sharpen_input_size_text, sharpen_output_size_text, sharpen_header_text)
        sharpen_all_elements.scale(1)
        
        self.add(all_elements, sharpen_all_elements)
        self.play(ReplacementTransform(kernel_matrix_text, kernel_matrix), GrowArrow(io_arrow),
                  ReplacementTransform(sharpen_kernel_matrix_text, sharpen_kernel_matrix), GrowArrow(sharpen_io_arrow), run_time=1)
        # Animate the sliding of the kernel across the grid
        self.animate_kernels_in_parallel(
            kernel_matrix_1=kernel_matrix, 
            kernel_matrix_2=sharpen_kernel_matrix,
            params_1=(grid_rows, grid_cols, cell_height, cell_width, output_mask, output_grid, kernel_size),
            params_2=(grid_rows, grid_cols, sharpen_cell_height, sharpen_cell_width, sharpen_output_mask, sharpen_output_grid, sharpen_kernel_size)
        )

    def create_grid(self, img, rows, cols, height, width):
        """Create a grid on top of the image."""
        grid = VGroup()
        for i in range(rows + 1):
            h_line = Line(
                start=img.get_corner(UP + LEFT) + DOWN * height * i / rows,
                end=img.get_corner(UP + RIGHT) + DOWN * height * i / rows
            )
            grid.add(h_line)

        for j in range(cols + 1):
            v_line = Line(
                start=img.get_corner(UP + LEFT) + RIGHT * width * j / cols,
                end=img.get_corner(DOWN + LEFT) + RIGHT * width * j / cols
            )
            grid.add(v_line)

        return grid
    
    def create_mask(self, grid, rows, cols, width, height):
        mask = VGroup()
        start_pos = self.get_grid_corner(grid, rows, height, width, 1)
        for row in range(rows):
            for col in range(cols):
                cell_mask = Rectangle(width=width, height=height, color=BLACK, fill_opacity=1)
                cell_mask.move_to(start_pos + np.array([col * width, row * height, 0]))
                mask.add(cell_mask)
        return mask

    def create_kernel_matrix(self, kernel, v_buff=0.8):
        """Create a 3x3 kernel matrix with values displayed."""
        kernel_table = MathTable(kernel, v_buff=v_buff, include_outer_lines=True)
        kernel_table.get_horizontal_lines()[:4].set_color(ORANGE)
        kernel_table.get_vertical_lines()[:4].set_color(ORANGE)
        
        cells = kernel_table.get_entries()
        for cell in cells:
            cell.scale(2)
            cell.set_color(ORANGE)
        
        return kernel_table

    def get_grid_corner(self, grid, row, cell_height, cell_width, kernel_size):
        """Get the center position of a specific grid cell."""
        x_spacing = cell_width * kernel_size / 2 #(grid[row+2].get_start()[0] - grid[row+1].get_start()[0]) / 2
        y_spacing = cell_height * kernel_size / 2 #(grid[3].get_start()[1] - grid[0].get_start()[1]) / 2
        return grid[row].get_start() + np.array([x_spacing, y_spacing, 0])

    def get_grid_cell_height(self, grid, rows):
        """Get the height of a single grid cell."""
        return (grid[rows-1].get_start()[1] - grid[rows].get_start()[1]) #/ rows
    
    def get_grid_cell_width(self, grid, rows):
        """ Get the width of a single grid cell"""
        return (grid[rows+2].get_start()[0] - grid[rows+1].get_start()[0])

    def animate_kernel_slide(self, kernel_matrix, rows, cols, cell_height, cell_width, output_mask, output_grid, kernel_size=3):
        """Animate the sliding of the kernel over the grid with stride 1."""
        animations = []
        starting_pos = kernel_matrix.get_center()
        y_spacing = 0
        output_cell_height = self.get_grid_cell_height(output_grid, rows - kernel_size + 1) 
        output_cell_width = self.get_grid_cell_width(output_grid, rows - kernel_size + 1) 
        
        for row in range(rows - kernel_size + 1):
            x_spacing = 0
            for col in range(cols - kernel_size + 1):
                new_position = starting_pos + np.array([x_spacing, y_spacing, 0])
                # Gradually reveal part of the output image
                mask_index = row * (rows - kernel_size + 1) + col
                kernel_matrix.generate_target()
                kernel_matrix.target.move_to(new_position)
                animations.append([MoveToTarget(kernel_matrix),
                                   FadeOut(output_mask[mask_index])])
                x_spacing += cell_width
                
            y_spacing += cell_height
        return animations

    def animate_kernels_in_parallel(self, kernel_matrix_1, kernel_matrix_2, params_1, params_2):
        """Run two kernel animations in parallel."""
        rows_1, cols_1, cell_height_1, cell_width_1, output_mask_1, output_grid_1, kernel_size_1 = params_1
        rows_2, cols_2, cell_height_2, cell_width_2, output_mask_2, output_grid_2, kernel_size_2 = params_2
        
        animations1 = self.animate_kernel_slide(kernel_matrix_1, rows_1, cols_1, cell_height_1, cell_width_1, 
                                        output_mask_1, output_grid_1, kernel_size_1)
        animations2 = self.animate_kernel_slide(kernel_matrix_2, rows_2, cols_2, cell_height_2, 
                                        cell_width_2, output_mask_2, output_grid_2, kernel_size_2)
        for i in range(len(animations1)):
            self.play(animations1[i][0], animations1[i][1], animations2[i][0], animations2[i][1], run_time=0.3)

            
    def get_output_size(self, dim, kernel_size, padding=0, stride=1):
        output_dim = (dim + 2 * padding - kernel_size) / stride + 1
        return int(output_dim)

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": False}):
        scene = ImageFilterConvolution()
        scene.render()