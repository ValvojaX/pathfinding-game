from math import sqrt
import tkinter as tk

class InputEvent:
    MOUSE_LEFT = 1
    MOUSE_RIGHT = 3

class GameEvent:
    def __init__(self) -> None:
        pass

class MouseEvent(GameEvent):
    def __init__(self, pos_x:int=None, pos_y:int=None, button:int=None, dragging:bool=None) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.button = button
        self.dragging = dragging

class InputHandler:
    def __init__(self, callback) -> None:
        self.__dragging = False
        self.__button = None
        self.callback = callback

    def on_mouse_move(self, event:tk.Event) -> None:
        game_event = MouseEvent(pos_x=event.x, pos_y=event.y, button=self.__button, dragging=self.__dragging)
        self.callback(game_event)

    def on_mouse_down(self, event:tk.Event) -> None:
        self.__button = event.num
        self.__dragging = True

    def on_mouse_release(self, event:tk.Event) -> None:
        self.__dragging = False

class Game(tk.Tk):
    def __init__(self, window_width:int=960, window_height:int=720) -> None:
        super().__init__()

        # variables
        self.input_handler = InputHandler(self.on_game_event)
        self.window_width = window_width
        self.window_height = window_height
        self.rect_count = 500
        self.canvas = None
        self.rectid_arr = []

        # initialize
        self.__initialize()

        # callbacks
        self.bind("<Configure>", self.on_window_update)

    def on_game_event(self, event:GameEvent):
        if type(event) == MouseEvent:
            if not event.dragging:
                return
            
            rect_id, = self.canvas.find_closest(event.pos_x, event.pos_y)
            
            if event.button == InputEvent.MOUSE_LEFT:
                self.canvas.itemconfig(rect_id, fill="red")

            if event.button == InputEvent.MOUSE_RIGHT:
                self.canvas.itemconfig(rect_id, fill="white")

    def on_window_update(self, event:tk.Event):
        self.window_width = event.width
        self.window_height = event.height

        # change canvas size
        self.canvas.config(width=self.window_width, height=self.window_height)

        # calculate row and column count
        rects_per_side = int(sqrt(len(self.rectid_arr)))

        # calculate rectangle size
        rect_width = self.window_width / rects_per_side
        rect_height = self.window_height / rects_per_side

        # update grid
        for row in range(rects_per_side):
            for col in range(rects_per_side):
                rect_id = self.rectid_arr[rects_per_side * row + col]
                self.canvas.coords(rect_id, rect_width * row, rect_height * col, rect_width * (row + 1), rect_height * (col + 1))

    def __initialize(self):
        # get screen size
        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
    
        # calculate center
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)
        
        # resize window
        super().geometry(f"{self.window_width}x{self.window_height}+{center_x}+{center_y}")

        # create canvas
        self.canvas = tk.Canvas(self, bg="black", width=self.window_width, height=self.window_height)
        
        # calculate row and column count
        rects_per_side = int(sqrt(self.rect_count))

        # calculate rectangle size
        rect_width = self.window_width / rects_per_side
        rect_height = self.window_height / rects_per_side

        # create grid
        for row in range(rects_per_side):
            for col in range(rects_per_side):
                rect_id = self.canvas.create_rectangle(rect_width * row, rect_height * col, rect_width * (row + 1), rect_height * (col + 1), fill="white")
                self.rectid_arr.append(rect_id)

        # bind input callbacks
        self.canvas.bind("<Motion>", self.input_handler.on_mouse_move)
        self.canvas.bind("<Button>", self.input_handler.on_mouse_down)
        self.canvas.bind("<ButtonRelease>", self.input_handler.on_mouse_release)

        # pack canvas
        self.canvas.pack()

    def run(self) -> None:
        super().mainloop()

if __name__ == "__main__":
    game = Game(window_width=800, window_height=600)
    game.run()