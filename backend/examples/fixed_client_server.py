from manim import *

class ClientServerScene(Scene):
    def construct(self):
        # Create client square
        sq1 = Square(side_length=1.5, color=BLUE, fill_opacity=0.5)
        sq1.shift(LEFT*2)
        client_text = Text("Client", font_size=30).move_to(sq1.get_center())
        client = VGroup(sq1, client_text)
        
        # Create server square
        sq2 = Square(side_length=1.5, color=RED, fill_opacity=0.5)
        sq2.shift(RIGHT*2)
        server_text = Text("Server", font_size=30).move_to(sq2.get_center())
        server = VGroup(sq2, server_text)
        
        # Create request arrow
        arrow1 = Arrow(sq1.get_right(), sq2.get_left(), buff=0.5, color=YELLOW)
        request = Text("Request", font_size=25).move_to(arrow1.get_center() + UP*0.5)
        
        # Create response arrow
        arrow2 = Arrow(sq2.get_left(), sq1.get_right(), buff=0.5, color=YELLOW)
        response = Text("Response", font_size=25).move_to(arrow2.get_center() + UP*0.5)
        
        # Animation sequence
        self.play(Create(sq1), Write(client_text))
        self.wait(0.5)
        self.play(Create(sq2), Write(server_text))
        self.wait(0.5)
        self.play(GrowArrow(arrow1), Write(request))
        self.wait(0.5)
        self.play(GrowArrow(arrow2), Write(response))
        self.wait(2)

# This can be used to test the animation locally
if __name__ == "__main__":
    scene = ClientServerScene()
    scene.render() 