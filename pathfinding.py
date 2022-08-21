from math import sqrt

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