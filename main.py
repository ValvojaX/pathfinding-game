import tkinter as tk

class Game(tk.Tk):
    def __init__(self, window_width:int=960, window_height:int=720) -> None:
        super().__init__()
        
        # get screen size
        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
    
        # calculate center
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
        # resize window
        super().geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # create canvas
        self.canvas = tk.Canvas(self, bg="black", width=window_width, height=window_height)
        
        # calculate rectangle size
        rect_width = window_width / 10
        rect_height = window_height / 10

        # create grid
        for row in range(10):
            for col in range(10):
                self.canvas.create_rectangle(rect_width * row, rect_height * col, rect_width * (row + 1), rect_height * (col + 1), fill="red")

        # pack canvas
        self.canvas.pack()

    def run(self) -> None:
        super().mainloop()

if __name__ == "__main__":
    game = Game(window_width=800, window_height=600)
    game.run()