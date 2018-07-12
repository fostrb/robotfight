import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo
import signal
import time
import threading
import math



class CairoDisplay(object):
    def __init__(self, bout=None):
        self.bout = bout
        self.window = Gtk.Window()
        self.window.set_decorated(False)
        self.window.resize(self.bout.arena[0], self.bout.arena[1])
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.window.set_visual(visual)
        self.window.set_app_paintable(True)
        self.window.connect('draw', self.update)
        self.window.connect('destroy', Gtk.main_quit)
        self.window.show_all()

        self.scanner_events = []

        t = threading.Thread(target=self.update_loop)
        t.daemon = True
        t.start()

    def update_loop(self):
        while True:
            time.sleep(.03)
            self.bout.update()
            self.window.queue_draw()

    def update(self, widget, ctx):
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_source_rgba(0, 0, 0, .8)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.fill()
        self.draw_entities(ctx)
        self.draw_boundary(ctx)

    def draw_entities(self, ctx):
        for rob in self.bout.robs:
            if rob.alive:
                rob.draw(ctx)

        for p in self.bout.projectiles:
            p.draw(ctx)
        self.draw_scans(ctx)

    def draw_scans(self, ctx):
        for scan in self.bout.scanner_events:
            pos = scan[0]
            angle = scan[1]
            arc_width = scan[2]
            arc_len = scan[3]
            color = scan[4]
            t = scan[5]

            a_start = (math.radians(angle-arc_width/2))
            a_end = (math.radians(math.degrees(a_start)+arc_width))

            t_val = time.time() - t
            t_val = (1-t_val)*.5
            if t_val < 1:
                ctx.new_path()
                color = [*color] + [t_val]
                ctx.set_source_rgba(*color)
                ctx.move_to(pos[0], pos[1])
                ctx.arc(pos[0], pos[1], arc_len, a_start, a_end)
                ctx.move_to(pos[0], pos[1])
                ctx.fill()
                '''
            

                ctx.set_source_rgba(0,1,0,t_val)
                ctx.line_to(pos[0], pos[1])
                ctx.arc(pos[0], pos[1], arc_len, a_start, a_end)
                ctx.line_to(pos[0], pos[1])
                ctx.stroke()
                ctx.new_path()
                '''
            else:
                self.bout.scanner_events.remove(scan)
                

    def draw_boundary(self, ctx):
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_line_width(2)
        ctx.set_source_rgba(0, 1, 0)
        ctx.rectangle(0, 0, *self.bout.arena)
        ctx.stroke()

    def scanner_draw(self, pos, angle, arc_width, arc_len, color):
        self.scanner_events.append [pos, angle, arc_width, arc_len, color, time.time()]


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    c = CairoDisplay()
    Gtk.main()
    exit()

