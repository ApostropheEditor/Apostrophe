class TextViewScroller:
    def __init__(self, text_view, scrolled_window):
        super().__init__()

        self.text_view = text_view
        self.scrolled_window = scrolled_window
        self.smooth_scroller = None

    def get_scroll_scale(self):
        vap = self.scrolled_window.get_vadjustment().props
        if vap.upper > vap.page_size:
            return vap.value / (vap.upper - vap.page_size)
        else:
            return 0

    def set_scroll_scale(self, scale):
        vap = self.scrolled_window.get_vadjustment().props
        vap.value = (vap.upper - vap.page_size) * scale

    def scroll_to_mark(self, mark, center):
        """Scrolls until mark is visible, if needed."""

        target_pos = self.get_target_pos_for_mark(mark, center)
        if target_pos:
            self.scrolled_window.get_vadjustment().set_value(target_pos)

    def smooth_scroll_to_mark(self, mark, center):
        """Smoothly scrolls until mark is visible, if needed."""

        if self.smooth_scroller and self.smooth_scroller.is_started:
            self.smooth_scroller.end()

        target_pos = self.get_target_pos_for_mark(mark, center)
        if target_pos:
            source_pos = self.scrolled_window.get_vadjustment().props.value
            self.smooth_scroller = SmoothScroller(self.scrolled_window, source_pos, target_pos)
            self.smooth_scroller.start()

    def get_target_pos_for_mark(self, mark, center):
        margin = 32

        mark_iter = self.text_view.get_buffer().get_iter_at_mark(mark)
        mark_rect = self.text_view.get_iter_location(mark_iter)

        vap = self.scrolled_window.get_vadjustment().props

        pos_y = mark_rect.y + mark_rect.height + self.text_view.props.top_margin
        pos_viewport_y = pos_y - vap.value
        target_pos = None
        if center:
            if pos_viewport_y != vap.page_size / 2:
                target_pos = pos_y - (vap.page_size / 2)
        elif pos_viewport_y > vap.page_size - margin:
            target_pos = pos_y - vap.page_size + margin
        elif pos_viewport_y < margin:
            target_pos = pos_y - margin - mark_rect.height

        return target_pos


class SmoothScroller:
    def __init__(self, scrolled_window, source_pos, target_pos):
        super().__init__()

        self.scrolled_window = scrolled_window
        self.source_pos = source_pos
        self.target_pos = target_pos
        self.duration = max(100, (target_pos - source_pos) / 50) * 1000

        self.is_started = False
        self.is_setup = False
        self.start_time = 0
        self.end_time = 0
        self.tick_callback_id = 0

    def start(self):
        self.is_started = True
        self.tick_callback_id = self.scrolled_window.add_tick_callback(self.on_tick)

    def end(self):
        self.scrolled_window.remove_tick_callback(self.tick_callback_id)
        self.is_started = False

    def setup(self, time):
        self.start_time = time
        self.end_time = time + self.duration
        self.is_setup = True

    def on_tick(self, widget, frame_clock):
        def ease_out_cubic(value):
            return pow(value - 1, 3) + 1

        now = frame_clock.get_frame_time()
        if not self.is_setup:
            self.setup(now)

        if now < self.end_time:
            time = float(now - self.start_time) / float(self.end_time - self.start_time)
        else:
            time = 1
            self.end()

        time = ease_out_cubic(time)
        pos = self.source_pos + (time * (self.target_pos - self.source_pos))
        widget.get_vadjustment().props.value = pos
        return True
