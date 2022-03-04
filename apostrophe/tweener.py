# Copyright 2022, Manuel Genovés <manuel.genoves@gmail.com>
#                 Alexander Mikhaylenko
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE
#
# Based on code by Alexander Mikhaylenko

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import GObject, Handy


class Tweener(GObject.Object):

    def __init__(self, widget, setter, value_from, value_to, duration, offset=0, setter_args = None, callback=None, callback_arg = None):
        self.widget = widget
        self.value_from = value_from
        self.value_to = value_to
        self.duration = duration
        self.offset = offset
        self.setter_args = setter_args
        self.callback = callback
        self.callback_arg = callback_arg

        self.start_time = 0
        self.tick_cb_id = 0

        self.setter = setter

        self.current_value = 0

    def stop(self):
        if (self.tick_cb_id != 0):

            self.widget.remove_tick_callback(self.tick_cb_id)
            self.tick_cb_id = 0
            if self.callback is not None:
                self.callback(self.callback_arg)

    def start(self):
        if (not Handy.get_enable_animations(self.widget) or
                not self.widget.get_mapped() or
                self.duration < 0):

            return

        if (self.tick_cb_id != 0):
            self.widget.remove_tick_callback(self.tick_cb_id)
            self.tick_cb_id = 0

        self.setter(self.value_from, *self.setter_args)

        self.start_time = self.widget.get_frame_clock().get_frame_time() / 1000
        self.tick_cb_id = self.widget.add_tick_callback(self.__tick_cb)

    def __tick_cb(self, widget, frame_clock):
        frame_time = frame_clock.get_frame_time() / 1000
        t = (frame_time - self.start_time - self.offset) / self.duration

        if t >= 1:
            self.current_value = self.value_to
            self.stop()
            self.tick_cb_id = 0

            self.setter(self.current_value, *self.setter_args)

            return False

        if t < 0:
            return True

        self.current_value = self.value_from\
            + (self.value_to - self.value_from)\
            * Handy.ease_out_cubic(t)

        self.setter(self.current_value, *self.setter_args)
        self.widget.queue_draw()

        return True
