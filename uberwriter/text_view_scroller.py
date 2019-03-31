from gi.repository import Gtk


class Scroller:
    def __init__(self):
        super().__init__()

        self.smooth_scroll_starttime = 0
        self.smooth_scroll_endtime = 0
        self.smooth_scroll_acttarget = 0
        self.smooth_scroll_data = {
            'target_pos': -1,
            'source_pos': -1,
            'duration': 0
        }
        self.smooth_scroll_tickid = -1

    def scroll_to(self, text_view, mark=None, center=False):
        """Scrolls if needed to ensure mark is visible.

        If mark is unspecified, the cursor is used."""

        margin = 80
        scrolled_window = text_view.get_ancestor(Gtk.ScrolledWindow.__gtype__)
        va = scrolled_window.get_vadjustment()
        if va.props.page_size < margin * 2:
            return

        text_buffer = text_view.get_buffer()
        if mark:
            ins_it = text_buffer.get_iter_at_mark(mark)
        else:
            ins_it = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        loc_rect = text_view.get_iter_location(ins_it)

        pos_y = loc_rect.y + loc_rect.height + text_view.props.top_margin
        pos = pos_y - va.props.value
        target_pos = -1
        if center:
            if pos != (va.props.page_size * 0.5):
                target_pos = pos_y - (va.props.page_size * 0.5)
        elif pos > va.props.page_size - margin:
            target_pos = pos_y - va.props.page_size + margin
        elif pos < margin:
            target_pos = pos_y - margin
        self.smooth_scroll_data = {
            'target_pos': target_pos,
            'source_pos': va.props.value,
            'duration': 2000
        }
        if self.smooth_scroll_tickid == -1:
            self.smooth_scroll_tickid = scrolled_window.add_tick_callback(self.on_tick)

    def on_tick(self, widget, frame_clock, _data=None):
        if self.smooth_scroll_data['target_pos'] == -1:
            return True

        def ease_out_cubic(value):
            return pow(value - 1, 3) + 1

        now = frame_clock.get_frame_time()
        if self.smooth_scroll_acttarget != self.smooth_scroll_data['target_pos']:
            self.smooth_scroll_starttime = now
            self.smooth_scroll_endtime = now + self.smooth_scroll_data['duration'] * 100
            self.smooth_scroll_acttarget = self.smooth_scroll_data['target_pos']

        if now < self.smooth_scroll_endtime:
            time = float(now - self.smooth_scroll_starttime) / float(
                self.smooth_scroll_endtime - self.smooth_scroll_starttime)
        else:
            time = 1
            pos = self.smooth_scroll_data['source_pos'] \
                + (time * (self.smooth_scroll_data['target_pos']
                           - self.smooth_scroll_data['source_pos']))
            widget.get_vadjustment().props.value = pos
            self.smooth_scroll_data['target_pos'] = -1
            return True

        time = ease_out_cubic(time)
        pos = self.smooth_scroll_data['source_pos'] \
            + (time * (self.smooth_scroll_data['target_pos']
                       - self.smooth_scroll_data['source_pos']))
        widget.get_vadjustment().props.value = pos
        return True
