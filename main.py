from math import sqrt
import time
import tkinter as tk
from tkinter import messagebox, ttk

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

class Stack:
    def __init__(self, arr_items:list=[]) -> None:
        self.array = arr_items

    def add(self, obj) -> None:
        self.array.insert(0, obj)

    def pop(self):
        return self.array.pop(0)

    def is_empty(self) -> bool:
        return len(self.array) == 0

class Queue:
    def __init__(self, arr_items:list=[]) -> None:
        self.array = arr_items

    def add(self, obj) -> None:
        self.array.append(obj)

    def pop(self):
        return self.array.pop(0)

    def is_empty(self) -> bool:
        return len(self.array) == 0

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = self.h = self.f = 0

    def __eq__(self, __o: object) -> bool:
        return self.position == __o.position

class Pathfinding:
    @staticmethod
    def search_a_star(start_index:int, end_index:int, arr_size:int, blacklist:list[int]) -> list[int]:
        start_node = Node(parent=None, position=start_index)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(parent=None, position=end_index)
        end_node.g = end_node.h = end_node.f = 0
        arr_side = int(sqrt(arr_size))

        # initialize open and closed list
        open_list = [start_node]
        closed_list = []

        # loop through open list
        while open_list:
            cur_node:Node = open_list[0]
            cur_node_index = 0

            # get last rect
            for index, node in enumerate(open_list):
                if node.f < cur_node.f: # closer to end rect -> closer to last rect
                    cur_node = node
                    cur_node_index = index

            # move to closed list
            open_list.pop(cur_node_index)
            closed_list.append(cur_node)

            # found last rect
            if cur_node == end_node:
                result = []
                parent = cur_node
                while parent is not None:
                    result.append(parent.position)
                    parent =  parent.parent

                # reverse path
                return result[::-1]

            # rects next to current rect
            children = []
            rect_right = cur_node.position + 1
            rect_left = cur_node.position - 1
            rect_up = cur_node.position - arr_side
            rect_down = cur_node.position + arr_side

            # move right
            on_right_side = float((cur_node.position) / (arr_side)).is_integer()
            if on_right_side == False and rect_right not in blacklist:
                children.append(Node(parent=cur_node, position=rect_right))

            # move left
            on_left_side = rect_left % arr_side == 0
            if on_left_side == False and rect_left not in blacklist:
                children.append(Node(parent=cur_node, position=rect_left))

            # move up
            on_up_side = cur_node.position < (arr_side - 1)
            if on_up_side == False and rect_up not in blacklist:
                children.append(Node(parent=cur_node, position=rect_up))

            # move down
            on_down_side = cur_node.position >= pow(arr_side, exp=2) - arr_side
            if on_down_side == False and rect_down not in blacklist:
                children.append(Node(parent=cur_node, position=rect_down))

            for child in children:
                if child in closed_list:
                    continue

                # calculate f, g, h
                child_row = int(child.position / arr_side)
                if float(child.position / arr_side).is_integer():
                    child_row -= 1
                child_col = (child.position - 1) % arr_side
                
                end_row = int(end_node.position / arr_side)
                if float(end_node.position / arr_side).is_integer():
                    end_row -= 1                
                end_col = (end_node.position - 1) % arr_side

                child.g = cur_node.g + 1
                child.h = ((child_row - end_row) ** 2) + ((child_col - end_col) ** 2)
                child.f = child.g + child.h

                # filter nodes already in open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)

        return []
    
    @staticmethod
    def search_depth(start_index:int, end_index:int, arr_size:int, blacklist:list[int]) -> list[int]:
        result = []
        arr = Stack([start_index])
        arr_side = int(sqrt(arr_size))

        while arr.is_empty() == False:
            index = arr.pop()
            if index in result:
                continue
            result.append(index)

            # rects next to current rect
            rect_right = index + 1
            rect_left = index - 1
            rect_up = index - arr_side
            rect_down = index + arr_side

            # move right
            on_right_side = float((index) / (arr_side)).is_integer()
            if on_right_side == False and rect_right not in blacklist:
                arr.add(rect_right)

            # move left
            on_left_side = rect_left % arr_side == 0
            if on_left_side == False and rect_left not in blacklist:
                arr.add(rect_left)

            # move up
            on_up_side = index < (arr_side - 1)
            if on_up_side == False and rect_up not in blacklist:
                arr.add(rect_up)

            # move down
            on_down_side = index >= pow(arr_side, exp=2) - arr_side
            if on_down_side == False and rect_down not in blacklist:
                arr.add(rect_down)

            if index == end_index:
                break

        return result

    @staticmethod
    def search_breadth(start_index:int, end_index:int, arr_size:int, blacklist:list[int]) -> list[int]:
        result = []
        arr = Queue([start_index])
        arr_side = int(sqrt(arr_size))

        while arr.is_empty() == False:
            index = arr.pop()
            if index in result:
                continue
            result.append(index)

            # rects next to current rect
            rect_right = index + 1
            rect_left = index - 1
            rect_up = index - arr_side
            rect_down = index + arr_side

            # move right
            on_right_side = float((index) / (arr_side)).is_integer()
            if on_right_side == False and rect_right not in blacklist:
                arr.add(rect_right)

            # move left
            on_left_side = rect_left % arr_side == 0
            if on_left_side == False and rect_left not in blacklist:
                arr.add(rect_left)

            # move up
            on_up_side = index < (arr_side - 1)
            if on_up_side == False and rect_up not in blacklist:
                arr.add(rect_up)

            # move down
            on_down_side = index >= pow(arr_side, exp=2) - arr_side
            if on_down_side == False and rect_down not in blacklist:
                arr.add(rect_down)

            if index == end_index:
                break

        return result

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
        self.is_searching = False
        self.start_rect = None
        self.end_rect = None

        # window objects
        self.canvas = None
        self.start_button = None
        self.algo_menu = None
        self.clear_button = None

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

            # stop searching if obstacles states are changed
            if event.button in [InputEvent.MOUSE_LEFT, InputEvent.MOUSE_RIGHT] and self.is_searching:
                self.is_searching = False
                for rect in self.rectid_arr:
                    color = self.canvas.itemconfig(rect)["fill"][4]
                    if color == "blue":
                        self.canvas.itemconfig(rect, fill="white")
                
                if self.start_rect is not None:
                    self.canvas.itemconfig(self.start_rect, fill="green")
                if self.end_rect is not None:
                    self.canvas.itemconfig(self.end_rect, fill="green")

            rect_id, = self.canvas.find_closest(event.pos_x, event.pos_y)
            if event.button == InputEvent.MOUSE_LEFT:
                if rect_id in [self.start_rect, self.end_rect, self.start_rect_text, self.end_rect_text]:
                    return

                # handle adding start rect
                if self.start_rect is None:
                    self.canvas.itemconfig(rect_id, fill="green")
                    self.start_rect = rect_id
                    
                    # add text
                    x0, y0, x1, y1 = self.canvas.coords(rect_id)
                    center = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
                    font_size = min((x1 - x0), (y1 - y0)) / 2
                    self.start_rect_text = self.canvas.create_text(center[0], center[1], text="S", fill="black", font=('Helvetica', str(int(font_size)), 'bold'))
                    return

                # handle adding end rect
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
                self.is_searching = False
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

        self.calculate_size_and_pos()

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

        # create menu items
        self.start_button = tk.Button(self, text="START", command=self.start_game)
        self.start_button.pack()

        menu_options = ["A*", "BFS", "DFS"]
        algo_menu_text = tk.StringVar()
        algo_menu_text.set(menu_options[0])
        self.algo_menu = tk.OptionMenu(self, algo_menu_text, *menu_options)
        self.algo_menu.text = algo_menu_text
        self.algo_menu.pack()

        self.speed_slider = ttk.Scale(self, from_=0.0, to=0.1, orient="horizontal")
        self.speed_slider.set(0.05)
        self.speed_slider.pack()

        self.clear_button = tk.Button(self, text="CLEAR", command=self.clear_game)
        self.clear_button.pack()

        self.calculate_size_and_pos()

        # pack canvas
        self.canvas.pack()

    def calculate_size_and_pos(self):
        # calculate size and position for items
        self.start_button.width = 0.3 * self.window_width
        self.start_button.height = 0.08 * self.window_height
        self.start_button.x = self.window_width / 5 - self.start_button.width / 2
        self.start_button.y = self.window_height - self.window_height * self.control_panel_size / 2 - self.start_button.height / 2

        self.algo_menu.width = 0.2 * self.window_width
        self.algo_menu.height = 0.04 * self.window_height
        self.algo_menu.x = self.window_width / 2 - self.algo_menu.width / 2
        self.algo_menu.y = self.start_button.y

        self.speed_slider.width = 0.2 * self.window_width
        self.speed_slider.height = 0.03 * self.window_height
        self.speed_slider.x = self.window_width / 2 - self.speed_slider.width / 2
        self.speed_slider.y = self.start_button.y + self.start_button.height / 2 + 5
        
        self.clear_button.width = 0.3 * self.window_width
        self.clear_button.height = 0.08 * self.window_height
        self.clear_button.x = self.window_width - self.window_width / 5 - self.clear_button.width / 2
        self.clear_button.y = self.start_button.y

        # place items
        self.start_button.place(x=self.start_button.x, y=self.start_button.y, height=self.start_button.height, width=self.start_button.width)
        self.algo_menu.place(x=self.algo_menu.x, y=self.algo_menu.y, height=self.algo_menu.height, width=self.algo_menu.width)
        self.speed_slider.place(x=self.speed_slider.x, y=self.speed_slider.y, height=self.speed_slider.height, width=self.speed_slider.width)
        self.clear_button.place(x=self.clear_button.x, y=self.clear_button.y, height=self.clear_button.height, width=self.clear_button.width)

    def clear_game(self) -> None:
        self.is_searching = False
        for item_id in self.rectid_arr:
            self.canvas.itemconfig(item_id, fill="white")

            if self.start_rect is not None:
                self.canvas.delete(self.start_rect_text)
                self.start_rect = None
                self.start_rect_text = None

            if self.end_rect is not None:
                self.canvas.delete(self.end_rect_text)
                self.end_rect = None
                self.end_rect_text = None
            
    def start_game(self) -> None:
        if self.start_rect is None or self.end_rect is None:
            messagebox.showerror("Game error", "Please select a starting point and an ending point by right clicking empty rectangles.")
            return

        if self.is_searching:
            return

        blacklist = []
        for item_id in self.rectid_arr:
            color = self.canvas.itemconfig(item_id)["fill"][4]
            if color == "red":
                blacklist.append(item_id)

            if color == "blue":
                self.canvas.itemconfig(item_id, fill="white")

        self.canvas.itemconfig(self.start_rect, fill="green")
        self.canvas.itemconfig(self.end_rect, fill="green")
        self.is_searching = True

        path = []
        if self.algo_menu.text.get() == "A*":
            path = Pathfinding.search_a_star(self.start_rect, self.end_rect, len(self.rectid_arr), blacklist)
        if self.algo_menu.text.get() == "BFS":
            path = Pathfinding.search_breadth(self.start_rect, self.end_rect, len(self.rectid_arr), blacklist)
        if self.algo_menu.text.get() == "DFS":
            path = Pathfinding.search_depth(self.start_rect, self.end_rect, len(self.rectid_arr), blacklist)
        
        for rect in path:
            if self.is_searching == False: # if clear is pressed or obstacles are changed, stop adding blue rects                    
                break
            
            self.canvas.itemconfig(rect, fill="blue")
            self.update()
            time.sleep(self.speed_slider.get())

        self.is_searching = False

    def run(self) -> None:
        super().mainloop()

if __name__ == "__main__":
    game = Game(window_width=600, window_height=700)
    game.run()