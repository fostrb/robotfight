import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo
import signal
import time
import threading



class CairoDisplay(object):
    def __init__(self, bout=None):
        self.bout = bout
        self.window = Gtk.Window()
        self.window.set_decorated(False)
        self.window.resize(*self.bout.arena)
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.window.set_visual(visual)
        self.window.set_app_paintable(True)
        self.window.connect('draw', self.update)
        self.window.connect('destroy', Gtk.main_quit)
        self.window.show_all()

        t = threading.Thread(target=self.update_loop)
        t.daemon = True
        t.start()
        #self.update_loop()

    def update_loop(self):
        while True:
            time.sleep(.03)
            self.bout.update_bots()
            self.window.queue_draw()

    def update(self, widget, ctx):
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_source_rgba(0, 0, 0, .8)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.fill()
        self.draw_entities(ctx)

    def draw_entities(self, ctx):
        #ctx.set_operator(cairo.OPERATOR_OVER)
        for rob in self.bout.robs:
            rob.draw(ctx)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    c = CairoDisplay()
    Gtk.main()
    exit()

