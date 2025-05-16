from manim import *

class BasicShapesScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE, fill_opacity=0.5)
        circle.shift(LEFT*3)
        
        # Create a square
        square = Square(color=RED, fill_opacity=0.5)
        
        # Create a triangle
        triangle = Triangle(color=GREEN, fill_opacity=0.5)
        triangle.shift(RIGHT*3)
        
        # Title
        title = Text("Basic Shapes", font_size=42)
        title.to_edge(UP)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(Create(circle))
        self.wait(0.5)
        self.play(Create(square))
        self.wait(0.5)
        self.play(Create(triangle))
        self.wait(0.5)
        
        # Animate transformations
        self.play(
            circle.animate.scale(0.5),
            square.animate.rotate(PI/4),
            triangle.animate.shift(UP)
        )
        self.wait(0.5)
        
        # Animate colors
        self.play(
            circle.animate.set_color(PURPLE),
            square.animate.set_color(YELLOW),
            triangle.animate.set_color(ORANGE)
        )
        self.wait(2)

# This can be used to test the animation locally
if __name__ == "__main__":
    scene = BasicShapesScene()
    scene.render() 