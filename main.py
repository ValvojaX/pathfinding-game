from math import sqrt
import tkinter as tk
from tkinter import messagebox

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
        
        game_event = MouseEvent(pos_x=event.x, pos_y=event.y, button=self.__button, dragging=self.__dragging)
        self.callback(game_event)

    def on_mouse_release(self, event:tk.Event) -> None:
        self.__dragging = False

class Pathfinding:
    def __init__(self) -> None:
        pass

    def search_a_star(self) -> None:
        pass
    
    def search_depth(self) -> None:
        pass

    def search_breadth(self) -> None:
        pass

class Game(tk.Tk):
    def __init__(self, window_width:int=960, window_height:int=720) -> None:
        super().__init__()

        # variables
        self.input_handler = InputHandler(self.on_game_event)
        self.window_width = window_width
        self.window_height = window_height
        self.control_panel_size = 0.15
        self.rect_count = 500
        self.rectid_arr = []
        self.start_rect = None
        self.end_rect = None

        # window objects
        self.canvas = None
        self.start_button = None
        self.start_rect_text = None
        self.end_rect_text = None

        # initialize
        self.__initialize()

        # callbacks
        self.bind("<Configure>", self.on_window_update)

    def on_game_event(self, event:GameEvent) -> None:
        if type(event) == MouseEvent:
            if not event.dragging:
                return
            
            rect_id, = self.canvas.find_closest(event.pos_x, event.pos_y)
            if event.button == InputEvent.MOUSE_LEFT:
                if rect_id in [self.start_rect, self.end_rect, self.start_rect_text, self.end_rect_text]:
                    return

                if self.start_rect is None:
                    self.canvas.itemconfig(rect_id, fill="green")
                    self.start_rect = rect_id
                    
                    # add text
                    x0, y0, x1, y1 = self.canvas.coords(rect_id)
                    center = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
                    font_size = min((x1 - x0), (y1 - y0)) / 2
                    self.start_rect_text = self.canvas.create_text(center[0], center[1], text="S", fill="black", font=('Helvetica', str(int(font_size)), 'bold'))
                    return

                if self.end_rect is None:
                    self.canvas.itemconfig(rect_id, fill="green")
                    self.end_rect = rect_id

                    # add text
                    x0, y0, x1, y1 = self.canvas.coords(rect_id)
                    center = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
                    font_size = min((x1 - x0), (y1 - y0)) / 2
                    self.end_rect_text = self.canvas.create_text(center[0], center[1], text="E", fill="black", font=('Helvetica', str(int(font_size)), 'bold'))
                    return

                self.canvas.itemconfig(rect_id, fill="red")

            if event.button == InputEvent.MOUSE_RIGHT:
                if rect_id in [self.start_rect, self.start_rect_text]:
                    self.canvas.delete(self.start_rect_text)
                    self.canvas.itemconfig(self.start_rect, fill="white")

                    self.start_rect = None
                    self.start_rect_text = None
                    

                if rect_id in [self.end_rect, self.end_rect_text]:
                    self.canvas.delete(self.end_rect_text)
                    self.canvas.itemconfig(self.end_rect, fill="white")

                    self.end_rect = None
                    self.end_rect_text = None

                self.canvas.itemconfig(rect_id, fill="white")

    def on_window_update(self, event:tk.Event) -> None:
        # filter other events
        if event.widget != self:
            return

        # optimize updating
        min_pixel_diff = 5
        if abs(self.window_height - event.height) < min_pixel_diff and abs(self.window_width - event.width) < min_pixel_diff:
            return
        
        # update window size
        self.window_width = event.width
        self.window_height = event.height

        # calculate space for controls
        canvas_width = self.window_width
        canvas_height = self.window_height - (self.window_height * self.control_panel_size)

        # change canvas size
        self.canvas.config(width=canvas_width, height=canvas_height)

        # calculate row and column count
        rects_per_side = int(sqrt(len(self.rectid_arr)))

        # calculate rectangle size
        rect_width = canvas_width / rects_per_side
        rect_height = canvas_height / rects_per_side

        # update grid
        for row in range(rects_per_side):
            for col in range(rects_per_side):
                rect_id = self.rectid_arr[rects_per_side * col + row]
                self.canvas.coords(rect_id, rect_width * row, rect_height * col, rect_width * (row + 1), rect_height * (col + 1))

        # calculate new position for start button
        self.start_button.width = 0.3 * self.window_width
        self.start_button.height = 0.08 * self.window_height
        start_button_pos_x = self.window_width / 2 - self.start_button.width / 2
        start_button_pos_y = self.window_height - self.window_height * self.control_panel_size / 2 - self.start_button.height / 2
        self.start_button.place(x=start_button_pos_x, y=start_button_pos_y, height=self.start_button.height, width=self.start_button.width)

        # calculate new position and size for start and end texts
        if self.start_rect_text is not None:
            x0, y0, x1, y1 = self.canvas.coords(self.start_rect)
            center = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
            font_size = min((x1 - x0), (y1 - y0)) / 2

            self.canvas.coords(self.start_rect_text, center[0], center[1])
            self.canvas.itemconfig(self.start_rect_text, text="S", fill="black", font=('Helvetica', str(int(font_size)), 'bold'))

        if self.end_rect_text is not None:
            x0, y0, x1, y1 = self.canvas.coords(self.end_rect)
            center = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
            font_size = min((x1 - x0), (y1 - y0)) / 2

            self.canvas.coords(self.end_rect_text, center[0], center[1])
            self.canvas.itemconfig(self.end_rect_text, text="E", fill="black", font=('Helvetica', str(int(font_size)), 'bold'))

    def __initialize(self) -> None:
        # get screen size
        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
    
        # calculate center
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)
        
        # resize window
        super().geometry(f"{self.window_width}x{self.window_height}+{center_x}+{center_y}")

        # calculate space for controls
        canvas_width = self.window_width
        canvas_height = self.window_height - (self.window_height * self.control_panel_size)

        # create canvas
        self.canvas = tk.Canvas(self, bg="black", width=canvas_width, height=canvas_height)
        
        # calculate row and column count
        rects_per_side = int(sqrt(self.rect_count))

        # calculate rectangle size
        rect_width = canvas_width / rects_per_side
        rect_height = canvas_height / rects_per_side

        # create grid
        for col in range(rects_per_side):
            for row in range(rects_per_side):
                rect_id = self.canvas.create_rectangle(rect_width * row, rect_height * col, rect_width * (row + 1), rect_height * (col + 1), fill="white")
                self.rectid_arr.append(rect_id)

        # bind input callbacks
        self.canvas.bind("<Motion>", self.input_handler.on_mouse_move)
        self.canvas.bind("<Button>", self.input_handler.on_mouse_down)
        self.canvas.bind("<ButtonRelease>", self.input_handler.on_mouse_release)

        # create start button
        self.start_button = tk.Button(self, text="START", command=self.start_game)

        # calculate size and position, add button
        self.start_button.width = 0.3 * self.window_width
        self.start_button.height = 0.08 * self.window_height
        start_button_pos_x = self.window_width / 2 - self.start_button.width / 2
        start_button_pos_y = self.window_height - self.window_height * self.control_panel_size / 2 - self.start_button.height / 2
        self.start_button.place(x=start_button_pos_x, y=start_button_pos_y, height=self.start_button.height, width=self.start_button.width)

        # pack canvas
        self.canvas.pack()

    def start_game(self) -> None:
        if self.start_rect is None or self.end_rect is None:
            messagebox.showerror("Game error", "Please select a starting point and an ending point by right clicking empty rectangles.")

    def run(self) -> None:
        super().mainloop()

if __name__ == "__main__":
    game = Game(window_width=600, window_height=700)
    game.run()