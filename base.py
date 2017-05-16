__author__ = 'ilija'

from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXSyntaxError
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import Image, ImageTk
from time import sleep
import os.path

def move_command_processor(move_cmd):
    if move_cmd.steps == 0:
        move_cmd.steps = 1


class AnElement(object):
    def __init__(self, elm):
        self.element_name = elm.element
        self.x = elm.x
        self.y = elm.y

class AnObstacle(object):
    def __init__(self, elm):
        self.element_name = elm.element_name
        self.x = elm.x
        self.y = elm.y

class Level(object):

    def __init__(self):
        self.elements = []
        self.obstacles = []
        self.is_there_a_switch = False

    def interpret(self, model):

        for c in model.commands:
            if c.__class__.__name__ == "PlaceElement":
                print("{} is at the position {}, {}".format(c.element, c.x, c.y))

                if c.x < 0 or c.y < 0 or c.x > 9 or c.y > 9:
                    app.output += 'You are trying to put an element {} outside the board!\n'.format(c.element)
                    app.text_dis.insert(END, app.output)
                    root.update_idletasks()
                else:

                    i = int(str(c.y) + str(c.x))
                    board.cell[i] = os.path.join('images', '{}' + '.png').format(c.element)

                    an_element = AnElement(c)
                    self.elements.append(an_element)

        first_robot = True
        first_switch = True
        first_door = True
        for e in self.elements:
            n = 0
            for elm in self.elements:
                if e.element_name == 'robot_kid' and e.element_name == elm.element_name:
                    if first_robot is False:
                        app.output += 'You are trying to put more than one {} on the board!\n'.format(e.element_name)
                        app.text_dis.insert(END, app.output)
                        root.update_idletasks()
                        i = int(str(elm.y) + str(elm.x))
                        board.cell[i] = os.path.join('images', 'empty.png')
                        del self.elements[n]
                        n += -1
                    first_robot = False
                if e.element_name == 'switch' and e.element_name == elm.element_name:
                    if first_switch is False:
                        app.output += 'You are trying to put more than one {} on the board!\n'.format(e.element_name)
                        app.text_dis.insert(END, app.output)
                        root.update_idletasks()
                        i = int(str(elm.y) + str(elm.x))
                        board.cell[i] = os.path.join('images', 'empty.png')
                        del self.elements[n]
                        n += -1
                    first_switch = False
                if e.element_name == 'door' and e.element_name == elm.element_name:
                    if first_door is False:
                        app.output += 'You are trying to put more than one {} on the board!\n'.format(e.element_name)
                        app.text_dis.insert(END, app.output)
                        root.update_idletasks()
                        i = int(str(elm.y) + str(elm.x))
                        board.cell[i] = os.path.join('images', 'empty.png')
                        del self.elements[n]
                        n += -1
                    first_door = False
                n += 1

        for e in self.elements:
            n = 0
            for elm in self.elements:
                if e.x == elm.x and e.y == elm.y and e.element_name != elm.element_name:
                    app.output += 'You are trying to put {} on top of {}!\n'.format(elm.element_name, e.element_name)
                    app.text_dis.insert(END, app.output)
                    root.update_idletasks()
                    i = int(str(elm.y) + str(elm.x))
                    board.cell[i] = os.path.join('images', 'empty.png')
                    del self.elements[n]
                    n += -1
                n += 1

        for e in self.elements:
            if e.element_name == 'switch':
                self.is_there_a_switch = True

        if self.is_there_a_switch is False:
            n = 0
            for cl in board.cell:
                if cl == os.path.join('images', 'door.png'):
                    board.cell[n] = os.path.join('images', 'door_opened.png')
                n += 1

        for e in self.elements:
            if e.element_name == 'movable_block' or e.element_name == 'unmovable_block' or e.element_name == 'mine':
                an_obstacle = AnObstacle(e)
                self.obstacles.append(an_obstacle)


class RobotPath(object):
    def __init__(self, rk_x, rk_y, rk_last_x, rk_last_y):
        self.x = rk_x
        self.y = rk_y
        self.last_x = rk_last_x
        self.last_y = rk_last_y
        self.success = True
        self.encountered_element = 'nothing'


class RobotAction(object):
    def __init__(self, rk_x, rk_y):
        self.x = rk_x
        self.y = rk_y
        self.used = False


class Robot(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.action = []
        self.path = []
        self.increment_x = 0
        self.increment_y = 0
        for obj in level.elements:
            if obj.element_name == "robot_kid":
                self.x = obj.x
                self.y = obj.y
                self.last_x = self.x
                self.last_y = self.y
                level.elements.remove(obj)

    def __str__(self):
        return "Robot position is {}, {}.".format(self.x, self.y)

    def interpret(self, model):

        for c in model.commands:

            if c.__class__.__name__ == "MoveCommand":
                dir = c.direction
                print("Going {} for {} step(s).".format(dir, c.steps))

                move = {
                    "up": (0, 1),
                    "down": (0, -1),
                    "left": (-1, 0),
                    "right": (1, 0)
                }[dir]

                self.last_x = self.x
                self.last_y = self.y

                self.x += c.steps * move[0]
                self.y += c.steps * move[1]

                a_step = RobotPath(self.x, self.y, self.last_x, self.last_y)
                self.path.append(a_step)

            else:
                an_action = RobotAction(self.x, self.y)
                self.action.append(an_action)

            print(self)


class Range(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Obstacle(object):

    def __init__(self):
        self.range_list = []

    def __str__(self):
        return "Obstacles are being taken into account"

    def interpret(self, obj, rbt, lvl):
        if obj.x > obj.last_x:
            n = obj.x
            while n >= obj.last_x:
                range_xy = Range(n, obj.y)
                n -= 1
                self.range_list.append(range_xy)
        elif obj.x < obj.last_x:
            n = obj.last_x
            while n >= obj.x:
                range_xy = Range(n, obj.y)
                n -= 1
                self.range_list.append(range_xy)
        elif obj.y > obj.last_y:
            n = obj.y
            while n >= obj.last_y:
                range_xy = Range(obj.x, n)
                n -= 1
                self.range_list.append(range_xy)
        elif obj.y < obj.last_y:
            n = obj.last_y
            while n >= obj.y:
                range_xy = Range(obj.x, n)
                n -= 1
                self.range_list.append(range_xy)
        else:
            range_xy = Range(obj.x, obj.y)
            self.range_list.append(range_xy)
        if len(self.range_list) >= 3:
            del self.range_list[0]
            del self.range_list[-1]
            for obs in lvl.obstacles:
                for rl in self.range_list:
                    if rl.x == obs.x and rl.y == obs.y:
                        extra_x = 0
                        extra_y = 0
                        if obs.element_name == 'mine':
                            obj.encountered_element = obs.element_name
                            extra_x = 1
                            extra_y = 1
                        else:
                            obj.encountered_element = 'obstacle'
                        if obj.last_x < obj.x:
                            rbt.increment_x += -(obj.x - rl.x + 1 - extra_x)
                        elif obj.last_x > obj.x:
                            rbt.increment_x += rl.x - obj.x + 1 - extra_x
                        if obj.last_y < obj.y:
                            rbt.increment_y += -(obj.y - rl.y + 1 - extra_y)
                        elif obj.last_y > obj.y:
                            rbt.increment_y += rl.y - obj.y + 1 - extra_y
                        obj.success = False
                        obj.x += rbt.increment_x
                        obj.y += rbt.increment_y
                        print("Because of an Obstacle {}, new Robot is {}, {}.".format(obs.element_name, obj.x, obj.y))
                        app.output += "Robot ran into an Obstacle {}, and was interrupted.\n".format(obs.element_name)
        print(self)


class UnmovableBlock(object):

    def __init__(self, lvl):
        self.x = lvl.x
        self.y = lvl.y

    def __str__(self):
        return "UnmovableBlock position is {}, {}.".format(self.x, self.y)

    def interpret(self, obj, rbt):
        if obj.last_x < obj.x:
            rbt.increment_x += -1
        elif obj.last_x > obj.x:
            rbt.increment_x += 1
        if obj.last_y < obj.y:
            rbt.increment_y += -1
        elif obj.last_y > obj.y:
            rbt.increment_y += 1
        obj.success = False
        obj.x += rbt.increment_x
        obj.y += rbt.increment_y
        print("Because of Unmovable Block, new Robot position is {}, {}.".format(obj.x, obj.y))
        app.output += "Because of Unmovable Block, Robot's path was interrupted.\n"
        print(self)


class MovableBlock(object):

    def __init__(self, lvl):
        self.x = lvl.x
        self.y = lvl.y
        self.last_x = self.x
        self.last_y = self.y
        self.mb_action = False
        self.obstacle = False
        self.message = ''

    def __str__(self):
        return "MovableBlock position is {}, {}.".format(self.x, self.y)

    def interpret(self, obj, rbt, act, lvl):
        self.mb_action = act
        if self.mb_action is True:
            if obj.last_x < self.x:
                self.x += 1
                if self.x > 9:
                    self.x += -1
                    rbt.increment_x += -1
                    self.obstacle = True
                else:
                    for o in lvl.elements:
                        if o.x == self.x and o.y == self.y:
                            self.x += -1
                            rbt.increment_x += -1
                            self.obstacle = True
            elif obj.last_x > self.x:
                self.x += -1
                if self.x < 0:
                    self.x += 1
                    rbt.increment_x += 1
                    self.obstacle = True
                else:
                    for o in lvl.elements:
                        if o.x == self.x and o.y == self.y:
                            self.x += 1
                            rbt.increment_x += 1
                            self.obstacle = True
            if obj.last_y < self.y:
                self.y += 1
                if self.y > 10:
                    self.y += -1
                    rbt.increment_y += -1
                    self.obstacle = True
                else:
                    for o in lvl.elements:
                        if o.x == self.x and o.y == self.y:
                            self.y += -1
                            rbt.increment_y += -1
                            self.obstacle = True
            elif obj.last_y > self.y:
                self.y += -1
                if self.y < 0:
                    self.y += 1
                    rbt.increment_y += 1
                    self.obstacle = True
                else:
                    for o in lvl.elements:
                        if o.x == self.x and o.y == self.y:
                            self.y += 1
                            rbt.increment_y += 1
                            self.obstacle = True
            if self.obstacle is True:
                self.message = "There is an obstacle behind the Movable Block"
                obj.success = False
            else:
                self.message = "Robot moved the Movable Block"
        elif self.mb_action is False:
            if obj.last_x < obj.x:
                rbt.increment_x += -1
            elif obj.last_x > obj.x:
                rbt.increment_x += 1
            if obj.last_y < obj.y:
                rbt.increment_y += -1
            elif obj.last_y > obj.y:
                rbt.increment_y += 1
            self.message = "Robot didn't move the Movable Block"
            obj.success = False
        obj.x += rbt.increment_x
        obj.y += rbt.increment_y
        for e in lvl.elements:
            if e.x == self.last_x and e.y == self.last_y:
                e.x = self.x
                e.y = self.y
        for o in lvl.obstacles:
            if o.x == self.last_x and o.y == self.last_y:
                o.x = self.x
                o.y = self.y
        print("Because {}, new Robot position is {}, {}.".format(self.message, obj.x, obj.y))
        app.output += "{}!\n".format(self.message)
        print(self)


class Switch(object):

    def __init__(self, lvl):
        self.x = lvl.x
        self.y = lvl.y
        self.sw_action = False
        self.activated = False

    def __str__(self):
        return "Switch position is {}, {}.".format(self.x, self.y)

    def interpret(self, obj, act):
        self.sw_action = act
        if self.sw_action is True:
            self.activated = True
            print("Robot Kid has flipped the switch!")
            app.output += "Robot Kid has flipped the switch!\n"
        else:
            obj.success = False
        print(self)


class Door(object):

    def __init__(self, lvl):
        self.x = lvl.x
        self.y = lvl.y

    def __str__(self):
        return "Door position is {}, {}.".format(self.x, self.y)

    def interpret(self, obj, swi):
        if swi is True:
            print("Robot Kid is trough the door!")
            app.output += "Robot Kid is trough the door!\n"
        else:
            obj.success = False
        print(self)


class Mine(object):

    def __init__(self, lvl):
        self.x = lvl.x
        self.y = lvl.y

    def __str__(self):
        return "Mine position is {}, {}.".format(self.x, self.y)

    def interpret(self, obj):
        obj.success = False
        print("Because of Mine, Robot has exploded.")
        app.output += "Because of Mine, Robot has exploded.\n"
        print(self)


class Board(object):
    def __init__(self):
        self.cell = []
        i = 0
        while i < 100:
            self.cell.append(os.path.join('images', 'empty.png'))
            i += 1
        self.last_cell = os.path.join('images', 'empty.png')
        self.temp_cell = ''
        self.game_over = False

    def __str__(self):
        return "Board is being made"

    def restart(self):
        del level.elements[:]
        del level.obstacles[:]
        if program.is_there_robot is True:
            del program.robot.path[:]
            del program.robot.action[:]
        del self.cell[:]
        i = 0
        while i < 100:
            self.cell.append(os.path.join('images', 'empty.png'))
            i += 1
        self.last_cell = os.path.join('images', 'empty.png')
        self.temp_cell = ''
        self.game_over = False

    def interpret(self, obj):
        if obj.encountered_element == 'nothing' or obj.encountered_element == 'obstacle':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            if obj.last_x < obj.x:
                self.cell[i] = os.path.join('images', 'rk_right.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'empty.png')
            elif obj.last_x > obj.x:
                self.cell[i] = os.path.join('images', 'rk_left.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'empty.png')
            elif obj.last_y < obj.y:
                self.cell[i] = os.path.join('images', 'rk_up.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'empty.png')
            elif obj.last_y > obj.y:
                self.cell[i] = os.path.join('images', 'rk_down.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'empty.png')
            else:
                self.cell[i] = os.path.join('images', 'rk_down.png')
                self.last_cell = os.path.join('images', 'empty.png')
        elif obj.encountered_element == 'movable_block':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            if obj.success is True:
                if obj.last_x < obj.x:
                    self.cell[i] = os.path.join('images', 'rk_right.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = os.path.join('images', 'empty.png')
                    temp_i = int(str(obj.y) + str(obj.x + 1))
                    self.cell[temp_i] = os.path.join('images', 'movable_block.png')
                elif obj.last_x > obj.x:
                    self.cell[i] = os.path.join('images', 'rk_left.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = os.path.join('images', 'empty.png')
                    temp_i = int(str(obj.y) + str(obj.x - 1))
                    self.cell[temp_i] = os.path.join('images', 'movable_block.png')
                if obj.last_y < obj.y:
                    self.cell[i] = os.path.join('images', 'rk_up.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = os.path.join('images', 'empty.png')
                    temp_i = int(str(obj.y + 1) + str(obj.x))
                    self.cell[temp_i] = os.path.join('images', 'movable_block.png')
                elif obj.last_y > obj.y:
                    self.cell[i] = os.path.join('images', 'rk_down.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = os.path.join('images', 'empty.png')
                    temp_i = int(str(obj.y - 1) + str(obj.x))
                    self.cell[temp_i] = os.path.join('images', 'movable_block.png')
            else:
                self.temp_cell = self.cell[i]
                if obj.last_x < obj.x:
                    if self.cell[i] == os.path.join('images', 'switch.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                    elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                    elif self.cell[i] == os.path.join('images', 'door.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                    elif self.cell[i] == os.path.join('images', 'door_open.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_open.png')
                        self.game_over = True
                    else:
                        self.cell[i] = os.path.join('images', 'rk_right.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = self.temp_cell
                elif obj.last_x > obj.x:
                    if self.cell[i] == os.path.join('images', 'switch.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                    elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                    elif self.cell[i] == os.path.join('images', 'door.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                    elif self.cell[i] == os.path.join('images', 'door_open.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_open.png')
                        self.game_over = True
                    else:
                        self.cell[i] = os.path.join('images', 'rk_left.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = self.temp_cell
                if obj.last_y < obj.y:
                    if self.cell[i] == os.path.join('images', 'switch.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                    elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                    elif self.cell[i] == os.path.join('images', 'door.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                    elif self.cell[i] == os.path.join('images', 'door_open.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_open.png')
                        self.game_over = True
                    else:
                        self.cell[i] = os.path.join('images', 'rk_up.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = self.temp_cell
                elif obj.last_y > obj.y:
                    if self.cell[i] == os.path.join('images', 'switch.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                    elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                        self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                    elif self.cell[i] == os.path.join('images', 'door.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                    elif self.cell[i] == os.path.join('images', 'door_open.png'):
                        self.cell[i] = os.path.join('images', 'rk_door_open.png')
                        self.game_over = True
                    else:
                        self.cell[i] = os.path.join('images', 'rk_down.png')
                    self.cell[last_i] = self.last_cell
                    self.last_cell = self.temp_cell
        elif obj.encountered_element == 'unmovable_block':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            self.temp_cell = self.cell[i]
            if obj.last_x < obj.x:
                if self.cell[i] == os.path.join('images', 'switch.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                elif self.cell[i] == os.path.join('images', 'door.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                elif self.cell[i] == os.path.join('images', 'door_open.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_open.png')
                    self.game_over = True
                else:
                    self.cell[i] = os.path.join('images', 'rk_right.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = self.temp_cell
            elif obj.last_x > obj.x:
                if self.cell[i] == os.path.join('images', 'switch.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                elif self.cell[i] == os.path.join('images', 'door.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                elif self.cell[i] == os.path.join('images', 'door_open.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_open.png')
                    self.game_over = True
                else:
                    self.cell[i] = os.path.join('images', 'rk_left.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = self.temp_cell
            if obj.last_y < obj.y:
                if self.cell[i] == os.path.join('images', 'switch.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                elif self.cell[i] == os.path.join('images', 'door.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                elif self.cell[i] == os.path.join('images', 'door_open.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_open.png')
                    self.game_over = True
                else:
                    self.cell[i] = os.path.join('images', 'rk_up.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = self.temp_cell
            elif obj.last_y > obj.y:
                if self.cell[i] == os.path.join('images', 'switch.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                    self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                elif self.cell[i] == os.path.join('images', 'door.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                elif self.cell[i] == os.path.join('images', 'door_open.png'):
                    self.cell[i] = os.path.join('images', 'rk_door_open.png')
                    self.game_over = True
                else:
                    self.cell[i] = os.path.join('images', 'rk_down.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = self.temp_cell
        elif obj.encountered_element == 'switch':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            if obj.success is True:
                self.cell[i] = os.path.join('images', 'rk_switch_on.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'switch_on.png')
                n = 0
                for cl in self.cell:
                    if cl == os.path.join('images', 'door.png'):
                        self.cell[n] = os.path.join('images', 'door_opened.png')
                    n += 1
            elif self.cell[i] == os.path.join('images', 'switch_on.png'):
                self.cell[i] = os.path.join('images', 'rk_switch_on_casual.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'switch_on.png')
            else:
                self.cell[i] = os.path.join('images', 'rk_switch_off.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'switch.png')
        elif obj.encountered_element == 'door':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            if obj.success is True:
                self.cell[i] = os.path.join('images', 'rk_door_open.png')
                self.cell[last_i] = self.last_cell
                self.game_over = True
            else:
                self.cell[i] = os.path.join('images', 'rk_door_closed.png')
                self.cell[last_i] = self.last_cell
                self.last_cell = os.path.join('images', 'door.png')
        elif obj.encountered_element == 'mine':
            i = int(str(obj.y) + str(obj.x))
            last_i = int(str(obj.last_y) + str(obj.last_x))
            self.cell[i] = os.path.join('images', 'explosion.png')
            self.cell[last_i] = self.last_cell
            self.game_over = True
        sleep(1)
        print(self)


class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.output = ''
        self.grid()
        self.create_widgets()

    def save_level(event):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".lvl", initialdir='levels')
        if f is None:
            return
        f.write(str(app.text_lvl.get(1.0, END)))
        file_name = f.name
        f.close()
        level_model = level_mm.model_from_file(os.path.join('levels', file_name))
        file_name = file_name.replace(".lvl", "")
        model_export(level_model, os.path.join('levels graphics', file_name + '.dot'))

    def open_level(event):
        f = filedialog.askopenfile(mode='r', defaultextension=".lvl", initialdir='levels')
        if f is None:
            return
        lvl_file = open(os.path.join('app files', program.lvl_file_name + '.lvl'), 'w')
        app.text_lvl.delete('1.0', END)
        app.text_lvl.insert(END, f.read())
        lvl_file.write(f.read())
        f.close()
        lvl_file.close()

    def load_level(event):
        board.restart()
        app.text_dis.delete('1.0', END)
        app.output = ''
        lvl_file = open(os.path.join('app files', program.lvl_file_name + '.lvl'), 'w')
        lvl_file.write(app.text_lvl.get("1.0", 'end-1c'))
        lvl_file.close()
        try:
            program.interpret_lvl()
        except IndexError as e:
            print(str(e))
            print('You are trying to place an element outside the board!')
            app.output += 'You are trying to place an element outside the board!\n'
            app.text_dis.insert(END, app.output)
            root.update_idletasks()
            program.is_there_level = False
        if program.is_there_robot_element is False:
            app.output += 'You do not have Robot Kid on the board!\n'
            app.text_dis.insert(END, app.output)
            root.update_idletasks()
        app.load_table()

    def save_play(event):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".rbt", initialdir='robots')
        if f is None:
            return
        f.write(str(app.text_rbt.get(1.0, END)))
        file_name = f.name
        f.close()
        robot_model = robot_mm.model_from_file(os.path.join('robots', file_name))
        file_name = file_name.replace(".rbt", "")
        model_export(robot_model, os.path.join('robots graphics', file_name + '.dot'))

    def open_play(event):
        f = filedialog.askopenfile(mode='r', defaultextension=".rbt", initialdir='robots')
        if f is None:
            return
        rbt_file = open(os.path.join('app files', program.rbt_file_name + '.rbt'), 'w')
        app.text_rbt.delete('1.0', END)
        app.text_rbt.insert(END, f.read())
        rbt_file.write(f.read())
        f.close()
        rbt_file.close()

    def play_level(event):
        if program.is_there_level is True and program.is_there_robot_element is True:
            rbt_file = open(os.path.join('app files', program.rbt_file_name + '.rbt'), 'w')
            rbt_file.write(app.text_rbt.get("1.0",'end-1c'))
            rbt_file.close()
            program.interpret_rbt()
            try:
                app.change_table()
            except ValueError as e:
                app.output += 'You are trying to move an object outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
            except IndexError as e:
                app.output += 'You are trying to move outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
            program.is_there_level = False

    def load_table(self):
        #panel 9

        self.r_90 = ImageTk.PhotoImage(Image.open(board.cell[90]))
        self.img_90.configure(image=self.r_90)

        self.r_91 = ImageTk.PhotoImage(Image.open(board.cell[91]))
        self.img_91.configure(image=self.r_91)

        self.r_92 = ImageTk.PhotoImage(Image.open(board.cell[92]))
        self.img_92.configure(image=self.r_92)

        self.r_93 = ImageTk.PhotoImage(Image.open(board.cell[93]))
        self.img_93.configure(image=self.r_93)

        self.r_94 = ImageTk.PhotoImage(Image.open(board.cell[94]))
        self.img_94.configure(image=self.r_94)

        self.r_95 = ImageTk.PhotoImage(Image.open(board.cell[95]))
        self.img_95.configure(image=self.r_95)

        self.r_96 = ImageTk.PhotoImage(Image.open(board.cell[96]))
        self.img_96.configure(image=self.r_96)

        self.r_97 = ImageTk.PhotoImage(Image.open(board.cell[97]))
        self.img_97.configure(image=self.r_97)

        self.r_98 = ImageTk.PhotoImage(Image.open(board.cell[98]))
        self.img_98.configure(image=self.r_98)

        self.r_99 = ImageTk.PhotoImage(Image.open(board.cell[99]))
        self.img_99.configure(image=self.r_99)

        #panel 8

        self.r_80 = ImageTk.PhotoImage(Image.open(board.cell[80]))
        self.img_80.configure(image=self.r_80)

        self.r_81 = ImageTk.PhotoImage(Image.open(board.cell[81]))
        self.img_81.configure(image=self.r_81)

        self.r_82 = ImageTk.PhotoImage(Image.open(board.cell[82]))
        self.img_82.configure(image=self.r_82)

        self.r_83 = ImageTk.PhotoImage(Image.open(board.cell[83]))
        self.img_83.configure(image=self.r_83)

        self.r_84 = ImageTk.PhotoImage(Image.open(board.cell[84]))
        self.img_84.configure(image=self.r_84)

        self.r_85 = ImageTk.PhotoImage(Image.open(board.cell[85]))
        self.img_85.configure(image=self.r_85)

        self.r_86 = ImageTk.PhotoImage(Image.open(board.cell[86]))
        self.img_86.configure(image=self.r_86)

        self.r_87 = ImageTk.PhotoImage(Image.open(board.cell[87]))
        self.img_87.configure(image=self.r_87)

        self.r_88 = ImageTk.PhotoImage(Image.open(board.cell[88]))
        self.img_88.configure(image=self.r_88)

        self.r_89 = ImageTk.PhotoImage(Image.open(board.cell[89]))
        self.img_89.configure(image=self.r_89)

        #panel 7

        self.r_70 = ImageTk.PhotoImage(Image.open(board.cell[70]))
        self.img_70.configure(image=self.r_70)

        self.r_71 = ImageTk.PhotoImage(Image.open(board.cell[71]))
        self.img_71.configure(image=self.r_71)

        self.r_72 = ImageTk.PhotoImage(Image.open(board.cell[72]))
        self.img_72.configure(image=self.r_72)

        self.r_73 = ImageTk.PhotoImage(Image.open(board.cell[73]))
        self.img_73.configure(image=self.r_73)

        self.r_74 = ImageTk.PhotoImage(Image.open(board.cell[74]))
        self.img_74.configure(image=self.r_74)

        self.r_75 = ImageTk.PhotoImage(Image.open(board.cell[75]))
        self.img_75.configure(image=self.r_75)

        self.r_76 = ImageTk.PhotoImage(Image.open(board.cell[76]))
        self.img_76.configure(image=self.r_76)

        self.r_77 = ImageTk.PhotoImage(Image.open(board.cell[77]))
        self.img_77.configure(image=self.r_77)

        self.r_78 = ImageTk.PhotoImage(Image.open(board.cell[78]))
        self.img_78.configure(image=self.r_78)

        self.r_79 = ImageTk.PhotoImage(Image.open(board.cell[79]))
        self.img_79.configure(image=self.r_79)

        #panel 6

        self.r_60 = ImageTk.PhotoImage(Image.open(board.cell[60]))
        self.img_60.configure(image=self.r_60)

        self.r_61 = ImageTk.PhotoImage(Image.open(board.cell[61]))
        self.img_61.configure(image=self.r_61)

        self.r_62 = ImageTk.PhotoImage(Image.open(board.cell[62]))
        self.img_62.configure(image=self.r_62)

        self.r_63 = ImageTk.PhotoImage(Image.open(board.cell[63]))
        self.img_63.configure(image=self.r_63)

        self.r_64 = ImageTk.PhotoImage(Image.open(board.cell[64]))
        self.img_64.configure(image=self.r_64)

        self.r_65 = ImageTk.PhotoImage(Image.open(board.cell[65]))
        self.img_65.configure(image=self.r_65)

        self.r_66 = ImageTk.PhotoImage(Image.open(board.cell[66]))
        self.img_66.configure(image=self.r_66)

        self.r_67 = ImageTk.PhotoImage(Image.open(board.cell[67]))
        self.img_67.configure(image=self.r_67)

        self.r_68 = ImageTk.PhotoImage(Image.open(board.cell[68]))
        self.img_68.configure(image=self.r_68)

        self.r_69 = ImageTk.PhotoImage(Image.open(board.cell[69]))
        self.img_69.configure(image=self.r_69)

        #panel 5

        self.r_50 = ImageTk.PhotoImage(Image.open(board.cell[50]))
        self.img_50.configure(image=self.r_50)

        self.r_51 = ImageTk.PhotoImage(Image.open(board.cell[51]))
        self.img_51.configure(image=self.r_51)

        self.r_52 = ImageTk.PhotoImage(Image.open(board.cell[52]))
        self.img_52.configure(image=self.r_52)

        self.r_53 = ImageTk.PhotoImage(Image.open(board.cell[53]))
        self.img_53.configure(image=self.r_53)

        self.r_54 = ImageTk.PhotoImage(Image.open(board.cell[54]))
        self.img_54.configure(image=self.r_54)

        self.r_55 = ImageTk.PhotoImage(Image.open(board.cell[55]))
        self.img_55.configure(image=self.r_55)

        self.r_56 = ImageTk.PhotoImage(Image.open(board.cell[56]))
        self.img_56.configure(image=self.r_56)

        self.r_57 = ImageTk.PhotoImage(Image.open(board.cell[57]))
        self.img_57.configure(image=self.r_57)

        self.r_58 = ImageTk.PhotoImage(Image.open(board.cell[58]))
        self.img_58.configure(image=self.r_58)

        self.r_59 = ImageTk.PhotoImage(Image.open(board.cell[59]))
        self.img_59.configure(image=self.r_59)

        #panel 4

        self.r_40 = ImageTk.PhotoImage(Image.open(board.cell[40]))
        self.img_40.configure(image=self.r_40)

        self.r_41 = ImageTk.PhotoImage(Image.open(board.cell[41]))
        self.img_41.configure(image=self.r_41)

        self.r_42 = ImageTk.PhotoImage(Image.open(board.cell[42]))
        self.img_42.configure(image=self.r_42)

        self.r_43 = ImageTk.PhotoImage(Image.open(board.cell[43]))
        self.img_43.configure(image=self.r_43)

        self.r_44 = ImageTk.PhotoImage(Image.open(board.cell[44]))
        self.img_44.configure(image=self.r_44)

        self.r_45 = ImageTk.PhotoImage(Image.open(board.cell[45]))
        self.img_45.configure(image=self.r_45)

        self.r_46 = ImageTk.PhotoImage(Image.open(board.cell[46]))
        self.img_46.configure(image=self.r_46)

        self.r_47 = ImageTk.PhotoImage(Image.open(board.cell[47]))
        self.img_47.configure(image=self.r_47)

        self.r_48 = ImageTk.PhotoImage(Image.open(board.cell[48]))
        self.img_48.configure(image=self.r_48)

        self.r_49 = ImageTk.PhotoImage(Image.open(board.cell[49]))
        self.img_49.configure(image=self.r_49)

        #panel 3

        self.r_30 = ImageTk.PhotoImage(Image.open(board.cell[30]))
        self.img_30.configure(image=self.r_30)

        self.r_31 = ImageTk.PhotoImage(Image.open(board.cell[31]))
        self.img_31.configure(image=self.r_31)

        self.r_32 = ImageTk.PhotoImage(Image.open(board.cell[32]))
        self.img_32.configure(image=self.r_32)

        self.r_33 = ImageTk.PhotoImage(Image.open(board.cell[33]))
        self.img_33.configure(image=self.r_33)

        self.r_34 = ImageTk.PhotoImage(Image.open(board.cell[34]))
        self.img_34.configure(image=self.r_34)

        self.r_35 = ImageTk.PhotoImage(Image.open(board.cell[35]))
        self.img_35.configure(image=self.r_35)

        self.r_36 = ImageTk.PhotoImage(Image.open(board.cell[36]))
        self.img_36.configure(image=self.r_36)

        self.r_37 = ImageTk.PhotoImage(Image.open(board.cell[37]))
        self.img_37.configure(image=self.r_37)

        self.r_38 = ImageTk.PhotoImage(Image.open(board.cell[38]))
        self.img_38.configure(image=self.r_38)

        self.r_39 = ImageTk.PhotoImage(Image.open(board.cell[39]))
        self.img_39.configure(image=self.r_39)

        #panel 2

        self.r_20 = ImageTk.PhotoImage(Image.open(board.cell[20]))
        self.img_20.configure(image=self.r_20)

        self.r_21 = ImageTk.PhotoImage(Image.open(board.cell[21]))
        self.img_21.configure(image=self.r_21)

        self.r_22 = ImageTk.PhotoImage(Image.open(board.cell[22]))
        self.img_22.configure(image=self.r_22)

        self.r_23 = ImageTk.PhotoImage(Image.open(board.cell[23]))
        self.img_23.configure(image=self.r_23)

        self.r_24 = ImageTk.PhotoImage(Image.open(board.cell[24]))
        self.img_24.configure(image=self.r_24)

        self.r_25 = ImageTk.PhotoImage(Image.open(board.cell[25]))
        self.img_25.configure(image=self.r_25)

        self.r_26 = ImageTk.PhotoImage(Image.open(board.cell[26]))
        self.img_26.configure(image=self.r_26)

        self.r_27 = ImageTk.PhotoImage(Image.open(board.cell[27]))
        self.img_27.configure(image=self.r_27)

        self.r_28 = ImageTk.PhotoImage(Image.open(board.cell[28]))
        self.img_28.configure(image=self.r_28)

        self.r_29 = ImageTk.PhotoImage(Image.open(board.cell[29]))
        self.img_29.configure(image=self.r_29)

        #panel 1

        self.r_10 = ImageTk.PhotoImage(Image.open(board.cell[10]))
        self.img_10.configure(image=self.r_10)

        self.r_11 = ImageTk.PhotoImage(Image.open(board.cell[11]))
        self.img_11.configure(image=self.r_11)

        self.r_12 = ImageTk.PhotoImage(Image.open(board.cell[12]))
        self.img_12.configure(image=self.r_12)

        self.r_13 = ImageTk.PhotoImage(Image.open(board.cell[13]))
        self.img_13.configure(image=self.r_13)

        self.r_14 = ImageTk.PhotoImage(Image.open(board.cell[14]))
        self.img_14.configure(image=self.r_14)

        self.r_15 = ImageTk.PhotoImage(Image.open(board.cell[15]))
        self.img_15.configure(image=self.r_15)

        self.r_16 = ImageTk.PhotoImage(Image.open(board.cell[16]))
        self.img_16.configure(image=self.r_16)

        self.r_17 = ImageTk.PhotoImage(Image.open(board.cell[17]))
        self.img_17.configure(image=self.r_17)

        self.r_18 = ImageTk.PhotoImage(Image.open(board.cell[18]))
        self.img_18.configure(image=self.r_18)

        self.r_19 = ImageTk.PhotoImage(Image.open(board.cell[19]))
        self.img_19.configure(image=self.r_19)

        #panel 0

        self.r_00 = ImageTk.PhotoImage(Image.open(board.cell[0]))
        self.img_00.configure(image=self.r_00)

        self.r_01 = ImageTk.PhotoImage(Image.open(board.cell[1]))
        self.img_01.configure(image=self.r_01)

        self.r_02 = ImageTk.PhotoImage(Image.open(board.cell[2]))
        self.img_02.configure(image=self.r_02)

        self.r_03 = ImageTk.PhotoImage(Image.open(board.cell[3]))
        self.img_03.configure(image=self.r_03)

        self.r_04 = ImageTk.PhotoImage(Image.open(board.cell[4]))
        self.img_04.configure(image=self.r_04)

        self.r_05 = ImageTk.PhotoImage(Image.open(board.cell[5]))
        self.img_05.configure(image=self.r_05)

        self.r_06 = ImageTk.PhotoImage(Image.open(board.cell[6]))
        self.img_06.configure(image=self.r_06)

        self.r_07 = ImageTk.PhotoImage(Image.open(board.cell[7]))
        self.img_07.configure(image=self.r_07)

        self.r_08 = ImageTk.PhotoImage(Image.open(board.cell[8]))
        self.img_08.configure(image=self.r_08)

        self.r_09 = ImageTk.PhotoImage(Image.open(board.cell[9]))
        self.img_09.configure(image=self.r_09)

        self.text_dis.delete('1.0', END)
        self.text_dis.insert(END, app.output)

        root.update_idletasks()

    def change_table(self):
        for obj in program.robot.path:
            board.interpret(obj)

            app.load_table()

            if board.game_over is True:
                break

    def create_widgets(self):
        self.panel_left = PanedWindow(self, orient=VERTICAL)

        self.text_lvl = scrolledtext.ScrolledText(self, height=20, width=80)
        self.lvl_file = open(os.path.join('app files', program.lvl_file_name + '.lvl'), 'r')
        self.text_lvl.insert(END, self.lvl_file.read())
        self.panel_left.add(self.text_lvl)
        self.lvl_file.close()

        self.button_panel_lvl = PanedWindow(self, orient=HORIZONTAL)

        self.button_open_level = Button(self, text="Open Level", command=self.open_level)
        self.button_panel_lvl.add(self.button_open_level)

        self.button_save_level = Button(self, text="Save Level", command=self.save_level)
        self.button_panel_lvl.add(self.button_save_level)

        self.button_load_level = Button(self, text="Load Level", command=self.load_level)
        self.button_panel_lvl.add(self.button_load_level)

        self.panel_left.add(self.button_panel_lvl)

        self.text_rbt = scrolledtext.ScrolledText(self, height=20, width=80)
        self.rbt_file = open(os.path.join('app files', program.rbt_file_name + '.rbt'), 'r')
        self.text_rbt.insert(END, self.rbt_file.read())
        self.panel_left.add(self.text_rbt)
        self.rbt_file.close()

        self.button_panel_rbt = PanedWindow(self, orient=HORIZONTAL)

        self.button_open_play = Button(self, text="Open Play", command=self.open_play)
        self.button_panel_rbt.add(self.button_open_play)

        self.button_save_play = Button(self, text="Save Play", command=self.save_play)
        self.button_panel_rbt.add(self.button_save_play)

        self.button_play_level = Button(self, text="Play Level", command=self.play_level)
        self.button_panel_rbt.add(self.button_play_level)

        self.panel_left.add(self.button_panel_rbt)

        self.panel_left.grid(row=1, column=1, padx=5, pady=5, rowspan=2)

        self.panel_right = PanedWindow(self, orient=VERTICAL)

        self.panel_board_wide = PanedWindow(self, orient=HORIZONTAL)

        self.panel_y = PanedWindow(self, orient=VERTICAL)

        self.y_none_9 = Label(text=" ", font='Helvetica 5')
        self.y_none_8 = Label(text=" ", font='10')
        self.y_none_7 = Label(text=" ", font='Helvetica 9')
        self.y_none_6 = Label(text=" ", font='10')
        self.y_none_5 = Label(text=" ", font='Helvetica 9')
        self.y_none_4 = Label(text=" ", font='10')
        self.y_none_3 = Label(text=" ", font='Helvetica 9')
        self.y_none_2 = Label(text=" ", font='10')
        self.y_none_1 = Label(text=" ", font='Helvetica 9')
        self.y_none_0 = Label(text=" ", font='10')

        self.y_9 = Label(text="9", font='10')
        self.panel_y.add(self.y_none_9)
        self.panel_y.add(self.y_9)
        self.y_8 = Label(text="8", font='10')
        self.panel_y.add(self.y_none_8)
        self.panel_y.add(self.y_8)
        self.y_7 = Label(text="7", font='10')
        self.panel_y.add(self.y_none_7)
        self.panel_y.add(self.y_7)
        self.y_6 = Label(text="6", font='10')
        self.panel_y.add(self.y_none_6)
        self.panel_y.add(self.y_6)
        self.y_5 = Label(text="5", font='10')
        self.panel_y.add(self.y_none_5)
        self.panel_y.add(self.y_5)
        self.y_4 = Label(text="4", font='10')
        self.panel_y.add(self.y_none_4)
        self.panel_y.add(self.y_4)
        self.y_3 = Label(text="3", font='10')
        self.panel_y.add(self.y_none_3)
        self.panel_y.add(self.y_3)
        self.y_2 = Label(text="2", font='10')
        self.panel_y.add(self.y_none_2)
        self.panel_y.add(self.y_2)
        self.y_1 = Label(text="1", font='10')
        self.panel_y.add(self.y_none_1)
        self.panel_y.add(self.y_1)
        self.y_0 = Label(text="0", font='10')
        self.panel_y.add(self.y_none_0)
        self.panel_y.add(self.y_0)

        self.panel_board_wide.add(self.panel_y)

        self.panel_board = PanedWindow(self, orient=VERTICAL)

        self.panel_9 = PanedWindow(self, height=50, width=568)
        self.panel_8 = PanedWindow(self, height=50, width=568)
        self.panel_7 = PanedWindow(self, height=50, width=568)
        self.panel_6 = PanedWindow(self, height=50, width=568)
        self.panel_5 = PanedWindow(self, height=50, width=568)
        self.panel_4 = PanedWindow(self, height=50, width=568)
        self.panel_3 = PanedWindow(self, height=50, width=568)
        self.panel_2 = PanedWindow(self, height=50, width=568)
        self.panel_1 = PanedWindow(self, height=50, width=568)
        self.panel_0 = PanedWindow(self, height=50, width=568)

        #panel 9

        self.r_90 = ImageTk.PhotoImage(Image.open(board.cell[90]))
        self.img_90 = Label(image=self.r_90)
        self.panel_9.add(self.img_90)

        self.r_91 = ImageTk.PhotoImage(Image.open(board.cell[91]))
        self.img_91 = Label(image=self.r_91)
        self.panel_9.add(self.img_91)

        self.r_92 = ImageTk.PhotoImage(Image.open(board.cell[92]))
        self.img_92 = Label(image=self.r_92)
        self.panel_9.add(self.img_92)

        self.r_93 = ImageTk.PhotoImage(Image.open(board.cell[93]))
        self.img_93 = Label(image=self.r_93)
        self.panel_9.add(self.img_93)

        self.r_94 = ImageTk.PhotoImage(Image.open(board.cell[94]))
        self.img_94 = Label(image=self.r_94)
        self.panel_9.add(self.img_94)

        self.r_95 = ImageTk.PhotoImage(Image.open(board.cell[95]))
        self.img_95 = Label(image=self.r_95)
        self.panel_9.add(self.img_95)

        self.r_96 = ImageTk.PhotoImage(Image.open(board.cell[96]))
        self.img_96 = Label(image=self.r_96)
        self.panel_9.add(self.img_96)

        self.r_97 = ImageTk.PhotoImage(Image.open(board.cell[97]))
        self.img_97 = Label(image=self.r_97)
        self.panel_9.add(self.img_97)

        self.r_98 = ImageTk.PhotoImage(Image.open(board.cell[98]))
        self.img_98 = Label(image=self.r_98)
        self.panel_9.add(self.img_98)

        self.r_99 = ImageTk.PhotoImage(Image.open(board.cell[99]))
        self.img_99 = Label(image=self.r_99)
        self.panel_9.add(self.img_99)

        #panel 8

        self.r_80 = ImageTk.PhotoImage(Image.open(board.cell[80]))
        self.img_80 = Label(image=self.r_80)
        self.panel_8.add(self.img_80)

        self.r_81 = ImageTk.PhotoImage(Image.open(board.cell[81]))
        self.img_81 = Label(image=self.r_81)
        self.panel_8.add(self.img_81)

        self.r_82 = ImageTk.PhotoImage(Image.open(board.cell[82]))
        self.img_82 = Label(image=self.r_82)
        self.panel_8.add(self.img_82)

        self.r_83 = ImageTk.PhotoImage(Image.open(board.cell[83]))
        self.img_83 = Label(image=self.r_83)
        self.panel_8.add(self.img_83)

        self.r_84 = ImageTk.PhotoImage(Image.open(board.cell[84]))
        self.img_84 = Label(image=self.r_84)
        self.panel_8.add(self.img_84)

        self.r_85 = ImageTk.PhotoImage(Image.open(board.cell[85]))
        self.img_85 = Label(image=self.r_85)
        self.panel_8.add(self.img_85)

        self.r_86 = ImageTk.PhotoImage(Image.open(board.cell[86]))
        self.img_86 = Label(image=self.r_86)
        self.panel_8.add(self.img_86)

        self.r_87 = ImageTk.PhotoImage(Image.open(board.cell[87]))
        self.img_87 = Label(image=self.r_87)
        self.panel_8.add(self.img_87)

        self.r_88 = ImageTk.PhotoImage(Image.open(board.cell[88]))
        self.img_88 = Label(image=self.r_88)
        self.panel_8.add(self.img_88)

        self.r_89 = ImageTk.PhotoImage(Image.open(board.cell[89]))
        self.img_89 = Label(image=self.r_89)
        self.panel_8.add(self.img_89)

        #panel 7

        self.r_70 = ImageTk.PhotoImage(Image.open(board.cell[70]))
        self.img_70 = Label(image=self.r_70)
        self.panel_7.add(self.img_70)

        self.r_71 = ImageTk.PhotoImage(Image.open(board.cell[71]))
        self.img_71 = Label(image=self.r_71)
        self.panel_7.add(self.img_71)

        self.r_72 = ImageTk.PhotoImage(Image.open(board.cell[72]))
        self.img_72 = Label(image=self.r_72)
        self.panel_7.add(self.img_72)

        self.r_73 = ImageTk.PhotoImage(Image.open(board.cell[73]))
        self.img_73 = Label(image=self.r_73)
        self.panel_7.add(self.img_73)

        self.r_74 = ImageTk.PhotoImage(Image.open(board.cell[74]))
        self.img_74 = Label(image=self.r_74)
        self.panel_7.add(self.img_74)

        self.r_75 = ImageTk.PhotoImage(Image.open(board.cell[75]))
        self.img_75 = Label(image=self.r_75)
        self.panel_7.add(self.img_75)

        self.r_76 = ImageTk.PhotoImage(Image.open(board.cell[76]))
        self.img_76 = Label(image=self.r_76)
        self.panel_7.add(self.img_76)

        self.r_77 = ImageTk.PhotoImage(Image.open(board.cell[77]))
        self.img_77 = Label(image=self.r_77)
        self.panel_7.add(self.img_77)

        self.r_78 = ImageTk.PhotoImage(Image.open(board.cell[78]))
        self.img_78 = Label(image=self.r_78)
        self.panel_7.add(self.img_78)

        self.r_79 = ImageTk.PhotoImage(Image.open(board.cell[79]))
        self.img_79 = Label(image=self.r_79)
        self.panel_7.add(self.img_79)

        #panel 6

        self.r_60 = ImageTk.PhotoImage(Image.open(board.cell[60]))
        self.img_60 = Label(image=self.r_60)
        self.panel_6.add(self.img_60)

        self.r_61 = ImageTk.PhotoImage(Image.open(board.cell[61]))
        self.img_61 = Label(image=self.r_61)
        self.panel_6.add(self.img_61)

        self.r_62 = ImageTk.PhotoImage(Image.open(board.cell[62]))
        self.img_62 = Label(image=self.r_62)
        self.panel_6.add(self.img_62)

        self.r_63 = ImageTk.PhotoImage(Image.open(board.cell[63]))
        self.img_63 = Label(image=self.r_63)
        self.panel_6.add(self.img_63)

        self.r_64 = ImageTk.PhotoImage(Image.open(board.cell[64]))
        self.img_64 = Label(image=self.r_64)
        self.panel_6.add(self.img_64)

        self.r_65 = ImageTk.PhotoImage(Image.open(board.cell[65]))
        self.img_65 = Label(image=self.r_65)
        self.panel_6.add(self.img_65)

        self.r_66 = ImageTk.PhotoImage(Image.open(board.cell[66]))
        self.img_66 = Label(image=self.r_66)
        self.panel_6.add(self.img_66)

        self.r_67 = ImageTk.PhotoImage(Image.open(board.cell[67]))
        self.img_67 = Label(image=self.r_67)
        self.panel_6.add(self.img_67)

        self.r_68 = ImageTk.PhotoImage(Image.open(board.cell[68]))
        self.img_68 = Label(image=self.r_68)
        self.panel_6.add(self.img_68)

        self.r_69 = ImageTk.PhotoImage(Image.open(board.cell[69]))
        self.img_69 = Label(image=self.r_69)
        self.panel_6.add(self.img_69)

        #panel 5

        self.r_50 = ImageTk.PhotoImage(Image.open(board.cell[50]))
        self.img_50 = Label(image=self.r_50)
        self.panel_5.add(self.img_50)

        self.r_51 = ImageTk.PhotoImage(Image.open(board.cell[51]))
        self.img_51 = Label(image=self.r_51)
        self.panel_5.add(self.img_51)

        self.r_52 = ImageTk.PhotoImage(Image.open(board.cell[52]))
        self.img_52 = Label(image=self.r_52)
        self.panel_5.add(self.img_52)

        self.r_53 = ImageTk.PhotoImage(Image.open(board.cell[53]))
        self.img_53 = Label(image=self.r_53)
        self.panel_5.add(self.img_53)

        self.r_54 = ImageTk.PhotoImage(Image.open(board.cell[54]))
        self.img_54 = Label(image=self.r_54)
        self.panel_5.add(self.img_54)

        self.r_55 = ImageTk.PhotoImage(Image.open(board.cell[55]))
        self.img_55 = Label(image=self.r_55)
        self.panel_5.add(self.img_55)

        self.r_56 = ImageTk.PhotoImage(Image.open(board.cell[56]))
        self.img_56 = Label(image=self.r_56)
        self.panel_5.add(self.img_56)

        self.r_57 = ImageTk.PhotoImage(Image.open(board.cell[57]))
        self.img_57 = Label(image=self.r_57)
        self.panel_5.add(self.img_57)

        self.r_58 = ImageTk.PhotoImage(Image.open(board.cell[58]))
        self.img_58 = Label(image=self.r_58)
        self.panel_5.add(self.img_58)

        self.r_59 = ImageTk.PhotoImage(Image.open(board.cell[59]))
        self.img_59 = Label(image=self.r_59)
        self.panel_5.add(self.img_59)

        #panel 4

        self.r_40 = ImageTk.PhotoImage(Image.open(board.cell[40]))
        self.img_40 = Label(image=self.r_40)
        self.panel_4.add(self.img_40)

        self.r_41 = ImageTk.PhotoImage(Image.open(board.cell[41]))
        self.img_41 = Label(image=self.r_41)
        self.panel_4.add(self.img_41)

        self.r_42 = ImageTk.PhotoImage(Image.open(board.cell[42]))
        self.img_42 = Label(image=self.r_42)
        self.panel_4.add(self.img_42)

        self.r_43 = ImageTk.PhotoImage(Image.open(board.cell[43]))
        self.img_43 = Label(image=self.r_43)
        self.panel_4.add(self.img_43)

        self.r_44 = ImageTk.PhotoImage(Image.open(board.cell[44]))
        self.img_44 = Label(image=self.r_44)
        self.panel_4.add(self.img_44)

        self.r_45 = ImageTk.PhotoImage(Image.open(board.cell[45]))
        self.img_45 = Label(image=self.r_45)
        self.panel_4.add(self.img_45)

        self.r_46 = ImageTk.PhotoImage(Image.open(board.cell[46]))
        self.img_46 = Label(image=self.r_46)
        self.panel_4.add(self.img_46)

        self.r_47 = ImageTk.PhotoImage(Image.open(board.cell[47]))
        self.img_47 = Label(image=self.r_47)
        self.panel_4.add(self.img_47)

        self.r_48 = ImageTk.PhotoImage(Image.open(board.cell[48]))
        self.img_48 = Label(image=self.r_48)
        self.panel_4.add(self.img_48)

        self.r_49 = ImageTk.PhotoImage(Image.open(board.cell[49]))
        self.img_49 = Label(image=self.r_49)
        self.panel_4.add(self.img_49)

        #panel 3

        self.r_30 = ImageTk.PhotoImage(Image.open(board.cell[30]))
        self.img_30 = Label(image=self.r_30)
        self.panel_3.add(self.img_30)

        self.r_31 = ImageTk.PhotoImage(Image.open(board.cell[31]))
        self.img_31 = Label(image=self.r_31)
        self.panel_3.add(self.img_31)

        self.r_32 = ImageTk.PhotoImage(Image.open(board.cell[32]))
        self.img_32 = Label(image=self.r_32)
        self.panel_3.add(self.img_32)

        self.r_33 = ImageTk.PhotoImage(Image.open(board.cell[33]))
        self.img_33 = Label(image=self.r_33)
        self.panel_3.add(self.img_33)

        self.r_34 = ImageTk.PhotoImage(Image.open(board.cell[34]))
        self.img_34 = Label(image=self.r_34)
        self.panel_3.add(self.img_34)

        self.r_35 = ImageTk.PhotoImage(Image.open(board.cell[35]))
        self.img_35 = Label(image=self.r_35)
        self.panel_3.add(self.img_35)

        self.r_36 = ImageTk.PhotoImage(Image.open(board.cell[36]))
        self.img_36 = Label(image=self.r_36)
        self.panel_3.add(self.img_36)

        self.r_37 = ImageTk.PhotoImage(Image.open(board.cell[37]))
        self.img_37 = Label(image=self.r_37)
        self.panel_3.add(self.img_37)

        self.r_38 = ImageTk.PhotoImage(Image.open(board.cell[38]))
        self.img_38 = Label(image=self.r_38)
        self.panel_3.add(self.img_38)

        self.r_39 = ImageTk.PhotoImage(Image.open(board.cell[39]))
        self.img_39 = Label(image=self.r_39)
        self.panel_3.add(self.img_39)

        #panel 2

        self.r_20 = ImageTk.PhotoImage(Image.open(board.cell[20]))
        self.img_20 = Label(image=self.r_20)
        self.panel_2.add(self.img_20)

        self.r_21 = ImageTk.PhotoImage(Image.open(board.cell[21]))
        self.img_21 = Label(image=self.r_21)
        self.panel_2.add(self.img_21)

        self.r_22 = ImageTk.PhotoImage(Image.open(board.cell[22]))
        self.img_22 = Label(image=self.r_22)
        self.panel_2.add(self.img_22)

        self.r_23 = ImageTk.PhotoImage(Image.open(board.cell[23]))
        self.img_23 = Label(image=self.r_23)
        self.panel_2.add(self.img_23)

        self.r_24 = ImageTk.PhotoImage(Image.open(board.cell[24]))
        self.img_24 = Label(image=self.r_24)
        self.panel_2.add(self.img_24)

        self.r_25 = ImageTk.PhotoImage(Image.open(board.cell[25]))
        self.img_25 = Label(image=self.r_25)
        self.panel_2.add(self.img_25)

        self.r_26 = ImageTk.PhotoImage(Image.open(board.cell[26]))
        self.img_26 = Label(image=self.r_26)
        self.panel_2.add(self.img_26)

        self.r_27 = ImageTk.PhotoImage(Image.open(board.cell[27]))
        self.img_27 = Label(image=self.r_27)
        self.panel_2.add(self.img_27)

        self.r_28 = ImageTk.PhotoImage(Image.open(board.cell[28]))
        self.img_28 = Label(image=self.r_28)
        self.panel_2.add(self.img_28)

        self.r_29 = ImageTk.PhotoImage(Image.open(board.cell[29]))
        self.img_29 = Label(image=self.r_29)
        self.panel_2.add(self.img_29)

        #panel 1

        self.r_10 = ImageTk.PhotoImage(Image.open(board.cell[10]))
        self.img_10 = Label(image=self.r_10)
        self.panel_1.add(self.img_10)

        self.r_11 = ImageTk.PhotoImage(Image.open(board.cell[11]))
        self.img_11 = Label(image=self.r_11)
        self.panel_1.add(self.img_11)

        self.r_12 = ImageTk.PhotoImage(Image.open(board.cell[12]))
        self.img_12 = Label(image=self.r_12)
        self.panel_1.add(self.img_12)

        self.r_13 = ImageTk.PhotoImage(Image.open(board.cell[13]))
        self.img_13 = Label(image=self.r_13)
        self.panel_1.add(self.img_13)

        self.r_14 = ImageTk.PhotoImage(Image.open(board.cell[14]))
        self.img_14 = Label(image=self.r_14)
        self.panel_1.add(self.img_14)

        self.r_15 = ImageTk.PhotoImage(Image.open(board.cell[15]))
        self.img_15 = Label(image=self.r_15)
        self.panel_1.add(self.img_15)

        self.r_16 = ImageTk.PhotoImage(Image.open(board.cell[16]))
        self.img_16 = Label(image=self.r_16)
        self.panel_1.add(self.img_16)

        self.r_17 = ImageTk.PhotoImage(Image.open(board.cell[17]))
        self.img_17 = Label(image=self.r_17)
        self.panel_1.add(self.img_17)

        self.r_18 = ImageTk.PhotoImage(Image.open(board.cell[18]))
        self.img_18 = Label(image=self.r_18)
        self.panel_1.add(self.img_18)

        self.r_19 = ImageTk.PhotoImage(Image.open(board.cell[19]))
        self.img_19 = Label(image=self.r_19)
        self.panel_1.add(self.img_19)

        #panel 0

        self.r_00 = ImageTk.PhotoImage(Image.open(board.cell[0]))
        self.img_00 = Label(image=self.r_00)
        self.panel_0.add(self.img_00)

        self.r_01 = ImageTk.PhotoImage(Image.open(board.cell[1]))
        self.img_01 = Label(image=self.r_01)
        self.panel_0.add(self.img_01)

        self.r_02 = ImageTk.PhotoImage(Image.open(board.cell[2]))
        self.img_02 = Label(image=self.r_02)
        self.panel_0.add(self.img_02)

        self.r_03 = ImageTk.PhotoImage(Image.open(board.cell[3]))
        self.img_03 = Label(image=self.r_03)
        self.panel_0.add(self.img_03)

        self.r_04 = ImageTk.PhotoImage(Image.open(board.cell[4]))
        self.img_04 = Label(image=self.r_04)
        self.panel_0.add(self.img_04)

        self.r_05 = ImageTk.PhotoImage(Image.open(board.cell[5]))
        self.img_05 = Label(image=self.r_05)
        self.panel_0.add(self.img_05)

        self.r_06 = ImageTk.PhotoImage(Image.open(board.cell[6]))
        self.img_06 = Label(image=self.r_06)
        self.panel_0.add(self.img_06)

        self.r_07 = ImageTk.PhotoImage(Image.open(board.cell[7]))
        self.img_07 = Label(image=self.r_07)
        self.panel_0.add(self.img_07)

        self.r_08 = ImageTk.PhotoImage(Image.open(board.cell[8]))
        self.img_08 = Label(image=self.r_08)
        self.panel_0.add(self.img_08)

        self.r_09 = ImageTk.PhotoImage(Image.open(board.cell[9]))
        self.img_09 = Label(image=self.r_09)
        self.panel_0.add(self.img_09)

        self.panel_board.add(self.panel_9)
        self.panel_board.add(self.panel_8)
        self.panel_board.add(self.panel_7)
        self.panel_board.add(self.panel_6)
        self.panel_board.add(self.panel_5)
        self.panel_board.add(self.panel_4)
        self.panel_board.add(self.panel_3)
        self.panel_board.add(self.panel_2)
        self.panel_board.add(self.panel_1)
        self.panel_board.add(self.panel_0)

        self.panel_board_wide.add(self.panel_board)

        self.panel_right.add(self.panel_board_wide)

        self.panel_x = PanedWindow(self, orient=HORIZONTAL)

        self.x_none_0 = Label(text=" ", font='10')
        self.x_none_1 = Label(text="        ", font='10')
        self.x_none_2 = Label(text="       ", font='10')
        self.x_none_3 = Label(text="        ", font='10')
        self.x_none_4 = Label(text="       ", font='10')
        self.x_none_5 = Label(text="        ", font='10')
        self.x_none_6 = Label(text="       ", font='10')
        self.x_none_7 = Label(text="        ", font='10')
        self.x_none_8 = Label(text="       ", font='10')
        self.x_none_9 = Label(text="        ", font='10')
        self.x_none_10 = Label(text=" ", font='10')

        self.x_xy = Label(text="y/x", font='5')
        self.panel_x.add(self.x_xy)
        self.panel_x.add(self.x_none_0)
        self.x_0 = Label(text="0", font='10')
        self.panel_x.add(self.x_0)
        self.panel_x.add(self.x_none_1)
        self.x_1 = Label(text="1", font='10')
        self.panel_x.add(self.x_1)
        self.panel_x.add(self.x_none_2)
        self.x_2 = Label(text="2", font='10')
        self.panel_x.add(self.x_2)
        self.panel_x.add(self.x_none_3)
        self.x_3 = Label(text="3", font='10')
        self.panel_x.add(self.x_3)
        self.panel_x.add(self.x_none_4)
        self.x_4 = Label(text="4", font='10')
        self.panel_x.add(self.x_4)
        self.panel_x.add(self.x_none_5)
        self.x_5 = Label(text="5", font='10')
        self.panel_x.add(self.x_5)
        self.panel_x.add(self.x_none_6)
        self.x_6 = Label(text="6", font='10')
        self.panel_x.add(self.x_6)
        self.panel_x.add(self.x_none_7)
        self.x_7 = Label(text="7", font='10')
        self.panel_x.add(self.x_7)
        self.panel_x.add(self.x_none_8)
        self.x_8 = Label(text="8", font='10')
        self.panel_x.add(self.x_8)
        self.panel_x.add(self.x_none_9)
        self.x_9 = Label(text="9", font='10')
        self.panel_x.add(self.x_9)
        self.panel_x.add(self.x_none_10)

        self.panel_right.add(self.panel_x)

        self.text_dis = scrolledtext.ScrolledText(self, height=10, width=60)
        self.text_dis.insert(END, self.output)
        self.panel_right.add(self.text_dis)

        self.panel_right.grid(row=1, column=2, padx=5, pady=5, rowspan=2)


class Program(object):

    def __init__(self):
        self.lvl_file_name = 'level'
        self.rbt_file_name = 'robot_kid'
        self.is_there_level = False
        self.is_there_robot = False
        self.is_there_robot_element = False

    def interpret_lvl(self):

        try:
            dummy_level_model = level_mm.model_from_file(os.path.join('app files', self.lvl_file_name + '.lvl'))
        except TextXSyntaxError as e:
            print(str(e))
            app.output += str(e) + '\n'
            app.text_dis.insert(END, app.output)
            root.update_idletasks()

        level_model = level_mm.model_from_file(os.path.join('app files', self.lvl_file_name + '.lvl'))
        model_export(level_model, os.path.join('app files', self.lvl_file_name + '.dot'))

        self.is_there_level = True
        level.interpret(level_model)

        self.is_there_robot_element = False
        for e in level.elements:
            if e.element_name == 'robot_kid':
                self.is_there_robot_element = True

    def interpret_rbt(self):

        try:
            dummy_robot_model = robot_mm.model_from_file(os.path.join('app files', self.rbt_file_name + '.rbt'))
        except TextXSyntaxError as e:
            print(str(e))
            app.output += str(e) + '\n'
            app.text_dis.insert(END, app.output)
            root.update_idletasks()

        robot_model = robot_mm.model_from_file(os.path.join('app files', self.rbt_file_name + '.rbt'))
        model_export(robot_model, os.path.join('app files', self.rbt_file_name + '.dot'))

        self.robot = Robot()
        self.is_there_robot = True
        self.robot.interpret(robot_model)
        self.s_act = False
        self.s_exs = False

        for r in self.robot.path:
            r.x += self.robot.increment_x
            r.y += self.robot.increment_y
            r.last_x += self.robot.increment_x
            r.last_y += self.robot.increment_y

            obstacle = Obstacle()
            obstacle.interpret(r, self.robot, level)

            if r.x > 10:
                app.output += 'You are trying to move outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
                r.x = 9
            elif r.x < 0:
                app.output += 'You are trying to move outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
                r.x = 0
            elif r.y > 10:
                app.output += 'You are trying to move outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
                r.y = 10
            elif r.y < 0:
                app.output += 'You are trying to move outside the board!\n'
                app.text_dis.insert(END, app.output)
                root.update_idletasks()
                r.y = 0

            for lvl in level.elements:
                if lvl.element_name == "mine":
                    if r.x == lvl.x and r.y == lvl.y:
                        r.encountered_element = lvl.element_name
                        mine = Mine(lvl)
                        mine.interpret(r)

                if lvl.element_name == "unmovable_block":
                    if r.x == lvl.x and r.y == lvl.y:
                        r.encountered_element = lvl.element_name
                        unmovable_block = UnmovableBlock(lvl)
                        unmovable_block.interpret(r, self.robot)

                if lvl.element_name == "movable_block":
                    if r.x == lvl.x and r.y == lvl.y:
                        self.a_mb = False
                        r.encountered_element = lvl.element_name
                        for act in self.robot.action:
                            if act.x == lvl.x and act.y == lvl.y:
                                if act.used is False:
                                    self.a_mb = True
                                    act.used = True
                                    break
                        movable_block = MovableBlock(lvl)
                        movable_block.interpret(r, self.robot, self.a_mb, level)

                if lvl.element_name == "switch":
                    self.s_exs = True
                    if r.x == lvl.x and r.y == lvl.y:
                        self.a_s = False
                        r.encountered_element = lvl.element_name
                        for act in self.robot.action:
                            if act.x == lvl.x and act.y == lvl.y:
                                if act.used is False:
                                    self.a_s = True
                                    act.used = True
                                    break
                        switch = Switch(lvl)
                        switch.interpret(r, self.a_s)
                        if switch.activated is True:
                            self.s_act = True

                if lvl.element_name == "door":
                    if r.x == lvl.x and r.y == lvl.y:
                        r.encountered_element = lvl.element_name
                        door = Door(lvl)
                        if self.s_exs is False:
                            self.s_act = True
                        door.interpret(r, self.s_act)


if __name__ == "__main__":

    level_mm = metamodel_from_file(os.path.join('app files', 'level.tx'), debug=False)
    metamodel_export(level_mm, os.path.join('app files', 'level_meta.dot'))

    robot_mm = metamodel_from_file(os.path.join('app files', 'robot_kid.tx'), debug=False)
    metamodel_export(robot_mm, os.path.join('app files', 'robot_meta.dot'))

    # Register object processor for MoveCommand
    robot_mm.register_obj_processors({'MoveCommand': move_command_processor})

    root = Tk()
    root.title("Robot Kid")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    board = Board()
    level = Level()
    program = Program()

    app = Application(root)
    app.grid()

    root.mainloop()
