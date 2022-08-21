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
        
        game_event = MouseEvent(pos_x=event.x, pos_y=event.y, button=self.__button, dragging=self.__dragging)
        self.callback(game_event)

    def on_mouse_release(self, event:tk.Event) -> None:
        self.__dragging = False