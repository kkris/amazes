#!/usr/bin/env python

from gi.repository import Gtk as gtk, GObject as gobject
import cairo
import time
from math import pi

from __init__ import Mazes

PADDING = 10
LINE_WIDTH = 2

TIMEOUT = 10
TIMES = 20

class MazeWidget(gtk.DrawingArea, gobject.GObject):

    __gsignals__ = {
        'step': (gobject.SignalFlags.RUN_LAST, None, (int,)),
        }

    def __init__(self):

        gtk.DrawingArea.__init__(self)
        gobject.GObject.__init__(self)

        self.cells = []

        self.connect('draw', self.draw_maze)

        self.runner_position = (0, 0) # the runner who runs through the maze
        self.stack = []


    def update(self, cells):

        self.cells = cells
        self.queue_draw()


    def solve(self, steps):

        class State(gobject.GObject):
            __gsignals__ = {
                'step': (gobject.SignalFlags.RUN_LAST, None, (int,)),
            }

            def __init__(self, steps):
                gobject.GObject.__init__(self)

                self.steps = steps
                self.step = steps.next()
                self.old_x, self.old_y = (0, 0)
                self.new_x, self.new_y = self.step.x, self.step.y
                self.counter = 0
                self.total_steps = 0

                self._x = 0
                self._y = 0

            def inc(self):
                if self.finished:
                    return True
                self.counter += 1
                self._x -= (self.old_x - self.new_x) / float(TIMES)
                self._y -= (self.old_y - self.new_y) / float(TIMES)
                if self.counter % TIMES == 0:
                    return self.reset()

            def reset(self):
                if self.finished:
                    return True
                self.counter = 0
                step = self.step
                self.step = next(self.steps, None)
                self.total_steps += 1
                self.emit('step', self.total_steps)

                if self.step is None:
                    self.counter = TIMES -1
                    return True


                self.old_x, self.old_y = self.new_x, self.new_y
                self.new_x, self.new_y = self.step.x, self.step.y

                self._x = self.old_x
                self._y = self.old_y

                return False

            @property
            def finished(self):
                return self.step is None and self.counter == TIMES


            @property
            def x(self):
                return round(self._x, 2)

            @property
            def y(self):
                return round(self._y, 2)


        def do(state):

            if state.finished:
                return False

            self.stack.append(self.runner_position)
            while len(self.stack) > 50:
                self.stack.pop(0)
            self.runner_position = (state.x, state.y)
            self.queue_draw()

            if state.inc():
                def f():
                    if self.stack:
                        self.stack.pop(0)
                    self.queue_draw()
                    if self.stack:
                        return True
                gobject.timeout_add(TIMEOUT, f)


            return True


        state = State(steps)
        state.connect('step', lambda w, s: self.emit('step', s))
        gobject.timeout_add(TIMEOUT, lambda: do(state))




    def draw_maze(self, widget, ctx):

        if not self.cells:
            return

        ctx.set_line_width(LINE_WIDTH)
        width = self.get_allocation().width - 2*PADDING
        height = self.get_allocation().height - 2*PADDING

        cell_width = width / float(len(self.cells[0]))
        cell_height = height / float(len(self.cells))

        ctx.set_operator(cairo.OPERATOR_OVER)

        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(PADDING, PADDING, width, height)
        ctx.stroke()

        def draw_line(ctx, x1, y1, x2, y2):
            ctx.move_to(int(x1), int(y1))
            ctx.line_to(int(x2), int(y2))
            ctx.stroke()

        drawn_cells = set()
        for row in self.cells:
            for cell in row:
                drawn_cells.add(cell)
                draw_right, draw_bottom = True, True
                cells = map(lambda c: c.cell1 if c.cell1 != cell else c.cell2, cell.connections)
                for neighbour_cell in cells:
                    if cell.x == neighbour_cell.x and cell.y < neighbour_cell.y:
                        draw_bottom = False

                    if cell.y == neighbour_cell.y and cell.x < neighbour_cell.x:
                        draw_right = False
                x = PADDING + cell.x * cell_width
                y = PADDING + cell.y * cell_height

                if draw_bottom:
                    y1 = y + cell_height
                    draw_line(ctx, x, y1, x+cell_width, y1)
                if draw_right:
                    x1 = x + cell_width
                    y1 = y + cell_height
                    draw_line(ctx, x1, y, x1, y1)


        start = self.cells[0][0]
        end = self.cells[-1][-1]
        ctx.set_source_rgba(0.5, 0, 0, 0.2)
        ctx.rectangle(PADDING + start.x*cell_width, PADDING + start.y*cell_height, cell_width, cell_height)
        ctx.fill()
        ctx.set_source_rgba(0, 0.5, 0, 0.2)
        ctx.rectangle(PADDING + end.x*cell_width, PADDING + end.y*cell_height, cell_width, cell_height)
        ctx.fill()

        x = PADDING + self.runner_position[0] * cell_width
        y = PADDING + self.runner_position[1] * cell_height

        ctx.set_source_rgba(0.4, 0.5, 0.6, 0.5)
        ctx.rectangle(x, y, cell_width, cell_height)
        ctx.fill()

        #for i, (x, y) in enumerate(self.stack):
         #   ctx.set_source_rgba(0.4, 0.5, 0.6, 0.1 + (i / len(self.stack)))
          #  x = PADDING + x * cell_width
           # y = PADDING + y * cell_height
           # ctx.rectangle(x, y, cell_width, cell_height)
            #ctx.fill()


class Window(object):

    def __init__(self):
        self.size = 5 # TODO
        self.mazes = Mazes(self.size)

        self.generation_method = 'depth_first'
        self.solve_method = 'random_mouse'

        self.window = gtk.Window()
        self.window.set_default_size(600, 600)
        self.window.set_title('Maze')
        self.window.connect('delete-event', lambda *x: gtk.main_quit())
        self.maze_widget = MazeWidget()
        self.maze_widget.connect('step', self.on_step)

        self.side_box = gtk.VBox()


        self.generation_box = gtk.VBox()

        depth_first = gtk.RadioButton.new_with_label(None, 'Depth First')
        depth_first.connect('clicked', self.on_generation_method_change)

        aldous_broder = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Aldous Broder')
        aldous_broder.connect('clicked', self.on_generation_method_change)

        wilsons = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Wilsons')
        wilsons.connect('clicked', self.on_generation_method_change)

        binary_tree = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Binary Tree')
        binary_tree.connect('clicked', self.on_generation_method_change)

        sidewinder = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Sidewinder')
        sidewinder.connect('clicked', self.on_generation_method_change)

        hunt_and_kill = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Hunt and Kill')
        hunt_and_kill.connect('clicked', self.on_generation_method_change)

        recursive_backtracker = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Recursive Backtracker')
        recursive_backtracker.connect('clicked', self.on_generation_method_change)

        prims = gtk.RadioButton.new_with_label_from_widget(depth_first, 'Prims')
        prims.connect('clicked', self.on_generation_method_change)

        self.generation_box.pack_start(depth_first, False, False, 0)
        self.generation_box.pack_start(aldous_broder, False, False, 0)
        self.generation_box.pack_start(wilsons, False, False, 0)
        self.generation_box.pack_start(binary_tree, False, False, 0)
        self.generation_box.pack_start(sidewinder, False, False, 0)
        self.generation_box.pack_start(hunt_and_kill, False, False, 0)
        self.generation_box.pack_start(recursive_backtracker, False, False, 0)
        self.generation_box.pack_start(prims, False, False, 0)

        self.size_widget = gtk.SpinButton.new_with_range(3, 100, 1.0)
        self.size_widget.set_value(self.size)
        self.size_widget.connect('value-changed', self.on_size_change)
        self.generation_box.pack_start(self.size_widget, False, False, 5)


        self.generate_maze = gtk.Button.new_with_label('Generate')
        self.generate_maze.connect('clicked', self.on_generate)
        self.generation_box.pack_start(self.generate_maze, False, False, 10)

        self.side_box.add(self.generation_box)


        self.solve_box = gtk.VBox()

        self.total_steps = gtk.Label('test')

        random_mouse = gtk.RadioButton.new_with_label(None, 'Random Mouse')
        random_mouse.connect('clicked', self.on_solve_method_change)

        wall_follower = gtk.RadioButton.new_with_label_from_widget(random_mouse, 'Wall Follower')
        wall_follower.connect('clicked', self.on_solve_method_change)

        tremaux = gtk.RadioButton.new_with_label_from_widget(random_mouse, 'Tremaux')
        tremaux.connect('clicked', self.on_solve_method_change)

        tremaux_shortest = gtk.RadioButton.new_with_label_from_widget(random_mouse, 'Tremaux Shortest')
        tremaux_shortest.connect('clicked', self.on_solve_method_change)

        flooding = gtk.RadioButton.new_with_label_from_widget(random_mouse, 'Flooding')
        flooding.connect('clicked', self.on_solve_method_change)


        self.solve_box.pack_start(random_mouse, False, False, 0)
        self.solve_box.pack_start(wall_follower, False, False, 0)
        self.solve_box.pack_start(tremaux, False, False, 0)
        self.solve_box.pack_start(tremaux_shortest, False, False, 0)
        self.solve_box.pack_start(flooding, False, False, 0)

        self.solve = gtk.Button.new_with_label('Solve')
        self.solve.connect('clicked', self.solve_maze)
        self.solve_box.pack_start(self.solve, False, False, 5)

        self.solve_box.pack_start(self.total_steps, True, False, 0)

        self.side_box.add(self.solve_box)

        self.box = gtk.HBox()

        self.box.pack_start(self.maze_widget, True, True, 0)
        self.box.pack_start(self.side_box, False, False, 0)

        self.window.add(self.box)



    def on_generation_method_change(self, widget):
        if widget.get_active():
            self.generation_method = widget.get_label().replace(' ', '_').lower()


    def on_solve_method_change(self, widget):
        if widget.get_active():
            self.solve_method = widget.get_label().replace(' ', '_').lower()


    def on_generate(self, widget):
        self.cells = self.mazes.generate(self.generation_method)
        self.maze_widget.update(self.cells)


    def on_step(self, widget, steps):
        self.total_steps.set_text('Steps: {0}'.format(steps))


    def on_size_change(self, widget):
        self.size = int(widget.get_value())
        self.mazes.size = self.size

    def solve_maze(self, widget):

        if hasattr(self, 'cells'):
            steps = self.mazes.solve(self.solve_method, self.cells)
            self.maze_widget.solve(steps)



    def show(self):
        self.window.show_all()
        gtk.main()



if __name__ == '__main__':
    win = Window()
    win.show()
