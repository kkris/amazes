#!/usr/bin/env python

import cairo

from gi.repository import Gtk as gtk

from amazes.generator import *
from amazes.solver import *
from amazes.utils import flatten
from amazes.ui.runner import MazeRunner

PADDING = 10
LINE_WIDTH = 2
TIMEOUT = 10

generators = {}
for generator in MazeGenerator.__subclasses__():
    generators[generator.name] = generator

solvers = {}
for solver in MazeSolver.__subclasses__():
    solvers[solver.name] = solver


def draw_line(ctx, x1, y1, x2, y2):
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.move_to(int(x1), int(y1))
    ctx.line_to(int(x2), int(y2))
    ctx.stroke()


class Maze(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)


        self.maze = None
        self.runner = None

        self.connect('draw', self.draw)

    def draw_maze(self, graph):

        self.maze = graph
        self.runner = None
        self.queue_draw()


    def solve_maze(self, steps):

        self.runner = MazeRunner(steps)
        self.runner.connect('step', lambda *x: self.queue_draw())
        self.runner.run()


    def draw(self, widget, ctx):

        if not self.maze:
            return

        ctx.set_line_width(LINE_WIDTH)
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_font_size(10)

        width = self.get_allocation().width - 2*PADDING
        height = self.get_allocation().height - 2*PADDING

        node_width = width / float(len(self.maze.nodes[0]))
        node_height = height / float(len(self.maze.nodes))

        # paint outline
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(PADDING, PADDING, width, height)
        ctx.stroke()

        for node in flatten(self.maze.nodes):
            x = PADDING + node.x * node_width
            y = PADDING + node.y * node_height
            x1 = x + node_width
            y1 = y + node_height

            right = bottom = True
            for neighbour in node.connected_nodes:
                if node.x == neighbour.x and node.y < neighbour.y:
                    bottom = False
                if node.y == neighbour.y and node.x < neighbour.x:
                    right = False

            if bottom and node.y < len(self.maze.nodes) - 1:
                draw_line(ctx, x, y1, x1, y1)
            if right and node.x < len(self.maze.nodes[0]) - 1:
                draw_line(ctx, x1, y, x1, y1)

            if node.value is not None:
                value = str(node.value)
                ctx.move_to(x + node_width / 2, y + node_height / 2)
                ctx.show_text(value)

            if self.runner and node in self.runner.path:
                ctx.set_source_rgba(0.8, 0.0, 0.0, 0.2)
                ctx.rectangle(x, y, node_width, node_height)
                ctx.fill()


        # Draw runner
        if not self.runner: return

        x = PADDING + self.runner.x * node_width
        y = PADDING + self.runner.y * node_height

        ctx.set_source_rgba(0.9, 0.0, 0.0, 0.6)
        ctx.rectangle(x, y, node_width, node_height)
        ctx.fill()



class Window(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_default_size(600, 600)
        self.set_title('Maze')
        self.connect('delete-event', lambda *x: gtk.main_quit())

        self.graph = None

        self.maze = Maze()
        self.generator = generators.values()[0] # TODO
        self.solver = solvers.values()[0]

        content = gtk.HBox()
        sidebar = gtk.VBox()
        generator_box = gtk.VBox()
        solver_box = gtk.VBox()

        button = None
        for name in generators.iterkeys():
            button = gtk.RadioButton.new_with_label_from_widget(button, name)
            button.connect('clicked', self.on_generation_method_change)

            generator_box.pack_start(button, False, False, 0)

        self.size_widget = gtk.SpinButton.new_with_range(2, 100, 1.0)
        generator_box.pack_start(self.size_widget, False, False, 5)

        generate_button = gtk.Button.new_with_label('Generate')
        generate_button.connect('clicked', self.on_generate)
        generator_box.pack_start(generate_button, False, False, 10)

        sidebar.add(generator_box)


        button = None
        for name in solvers.iterkeys():
            button = gtk.RadioButton.new_with_label_from_widget(button, name)
            button.connect('clicked', self.on_solver_method_change)

            solver_box.pack_start(button, False, False, 0)

        solve_button = gtk.Button.new_with_label('Solver')
        solve_button.connect('clicked', self.on_solve)
        solver_box.pack_start(solve_button, False, False, 10)

        sidebar.add(solver_box)


        content.pack_start(self.maze, True, True, 0)
        content.pack_start(sidebar, False, False, 10)

        self.add(content)
        self.show_all()


    def on_generation_method_change(self, button):

        if button.get_active():
            self.generator = generators[button.get_label()]


    def on_solver_method_change(self, button):

        if button.get_active():
            self.solver = solvers[button.get_label()]



    def on_generate(self, *args):

        size = int(self.size_widget.get_value())
        self.graph = self.generator().generate(size, size)
        self.maze.draw_maze(self.graph)


    def on_solve(self, *args):

        steps = self.solver().solve(self.graph)
        self.maze.solve_maze(steps)


if __name__ == '__main__':
    window = Window()
    gtk.main()
