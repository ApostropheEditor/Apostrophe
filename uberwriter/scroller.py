class Scroller:
    def __init__(self, scrolled_window, source_pos, target_pos):
        super().__init__()

        self.scrolled_window = scrolled_window
        self.source_pos = source_pos
        self.target_pos = target_pos
        self.duration = max(200, (target_pos - source_pos) / 50) * 1000

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


