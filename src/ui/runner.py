from gi.repository import GObject as gobject

TIMEOUT = 100

class MazeRunner(gobject.GObject):

    __gsignals__ = {'step': (gobject.SignalFlags.RUN_LAST, None, [])}

    def __init__(self, steps):

        gobject.GObject.__init__(self)

        self.steps = steps
        self.path = set()
        self.x = 0
        self.y = 0


    def run(self):

        gobject.timeout_add(TIMEOUT, self.step)


    def step(self):

        step, primary = next(self.steps, (None, None))
        if step:
            if primary:
                self.path.add(step)
                self.x = step.x
                self.y = step.y

            self.emit('step')
            gobject.timeout_add(TIMEOUT, self.step)
