from manim import *

class ClientServerScene(Scene):
    def construct(self):
        # Create the client square
        client_square = Square(side_length=1).shift(LEFT * 2)
        client_text = Text("Client", font_size=24).move_to(client_square.get_center())
        client_group = VGroup(client_square, client_text)

        # Create the server square
        server_square = Square(side_length=1).shift(RIGHT * 2)
        server_text = Text("Server", font_size=24).move_to(server_square.get_center())
        server_group = VGroup(server_square, server_text)

        # Create the request arrow
        request_arrow = Arrow(client_square.get_right(), server_square.get_left(), buff=0.2)
        request_text = Text("Request", font_size=18).next_to(request_arrow, UP)

        # Create the response arrow
        response_arrow = Arrow(server_square.get_left(), client_square.get_right(), buff=0.2)
        response_text = Text("Response", font_size=18).next_to(response_arrow, UP)

        # Animate the scene
        self.play(
            Create(client_group),
            Create(server_group)
        )
        
        self.wait(0.5)
        
        self.play(
            Create(request_arrow),
            Write(request_text)
        )
        
        self.wait(1)
        
        self.play(
            Create(response_arrow),
            Write(response_text)
        )
        
        self.wait(2)

if __name__ == "__main__":
    scene = ClientServerScene()
    scene.render() 