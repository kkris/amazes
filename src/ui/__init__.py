#!/usr/bin/env python

import time
import cairo

from gi.repository import Gtk as gtk, GObject as gobject

from amazes.generator import *
from amazes.utils import flatten

PADDING = 10
LINE_WIDTH = 2

generators = {}
for generator in MazeGenerator.__subclasses__():
    generators[generator.name] = generator


def draw_line(ctx, x1, y1, x2, y2):
    ctx.move_to(int(x1), int(y1))
    ctx.line_to(int(x2), int(y2))
    ctx.stroke()


class Maze(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)


        self.maze = None

        self.connect('draw', self.draw)

    def draw_maze(self, graph):

        self.maze = graph
        self.queue_draw()


    def draw(self, widget, ctx):

        if not self.maze:
            return

        ctx.set_line_width(LINE_WIDTH)
        ctx.set_operator(cairo.OPERATOR_OVER)

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

            if bottom:
                draw_line(ctx, x, y1, x1, y1)
            if right:
                draw_line(ctx, x1, y, x1, y1)

        # Draw entry and exit
        ctx.set_source_rgb(0.8, 0.1, 0.3)
        draw_line(ctx, PADDING, PADDING, PADDING + node_width, PADDING)
        ctx.set_source_rgb(0.1, 0.8, 0.1)
        draw_line(ctx, width+PADDING, height-node_height+PADDING, width+PADDING,height+PADDING)



class Window(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_default_size(600, 600)
        self.set_title('Maze')
        self.connect('delete-event', lambda *x: gtk.main_quit())

        self.maze = Maze()
        self.generator = generators.values()[0] # TODO

        content = gtk.HBox()
        sidebar = gtk.VBox()
        generator_box = gtk.VBox()

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

        content.pack_start(self.maze, True, True, 0)
        content.pack_start(sidebar, False, False, 10)

        self.add(content)
        self.show_all()


    def on_generation_method_change(self, button):

        if button.get_active():
            self.generator = generators[button.get_label()]



    def on_generate(self, *args):

        size = int(self.size_widget.get_value())
        graph = self.generator().generate(size, size)
        self.maze.draw_maze(graph)


if __name__ == '__main__':
    window = Window()
    gtk.main()
