class Scroller:
    def __init__(self, scrolled_window, target_pos, source_pos, duration=2000):
        super().__init__()

        self.scrolled_window = scrolled_window
        self.target_pos = target_pos
        self.source_pos = source_pos
        self.duration = duration

        self.is_started = False
        self.start_time = 0
        self.end_time = 0

        self.tick_callback_id = 0

    def start(self):
        self.tick_callback_id = self.scrolled_window.add_tick_callback(self.on_tick, self)

    def end(self):
        self.is_started = False
        self.scrolled_window.remove_tick_callback(self.tick_callback_id)

    def do_start(self, time):
        self.is_started = True
        self.start_time = time
        self.end_time = time + self.duration * 100

    @staticmethod
    def on_tick(widget, frame_clock, scroller):
        def ease_out_cubic(value):
            return pow(value - 1, 3) + 1

        now = frame_clock.get_frame_time()
        if not scroller.is_started:
            scroller.do_start(now)

        if now < scroller.end_time:
            time = float(now - scroller.start_time) / float(scroller.end_time - scroller.start_time)
        else:
            time = 1
            scroller.end()

        time = ease_out_cubic(time)
        pos = scroller.source_pos + (time * (scroller.target_pos - scroller.source_pos))
        widget.get_vadjustment().props.value = pos
        return True


