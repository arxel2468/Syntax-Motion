from manim import *

class DataGraphScene(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 25, 5],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [5, 10, 15, 20]},
        )
        
        # Add labels
        x_label = Text("Time (s)", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Value", font_size=24).next_to(axes.y_axis, LEFT)
        
        # Graph labels
        title = Text("Data Visualization", font_size=42)
        title.to_edge(UP)
        
        # Create graph
        graph = axes.plot(lambda x: x**2, color=YELLOW)
        graph_label = Text("f(x) = x²", font_size=24, color=YELLOW)
        graph_label.move_to(axes.c2p(4, 20))
        
        # Create dot on graph
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(3, 9))
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        self.play(Create(graph), Write(graph_label))
        self.wait(0.5)
        
        # Animate dot tracing along the graph
        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(axes.c2p(0, 0)))
        self.wait(0.5)
        
        # Show dot moving along curve
        self.play(
            MoveAlongPath(
                dot, 
                axes.plot(lambda x: x**2, color=YELLOW), 
                rate_func=linear
            ),
            run_time=3
        )
        self.wait(2)

# This can be used to test the animation locally
if __name__ == "__main__":
    scene = DataGraphScene()
    scene.render() 