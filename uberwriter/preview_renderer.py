from gettext import gettext as _

from gi.repository import Gtk, Gio, GLib

from uberwriter.settings import Settings


class PreviewRenderer:
    """Renders the preview according to the user selected mode."""

    # Must match the order/index defined in gschema.xml
    FULL_WIDTH = 0
    HALF_WIDTH = 1
    HALF_HEIGHT = 2
    WINDOWED = 3

    def __init__(self, main_window, content, editor, text_view, preview, mode_button):
        self.content = content
        self.editor = editor
        self.text_view = text_view
        self.preview = preview
        self.mode_button = mode_button
        self.mode_button.connect("clicked", self.show_mode_popover)
        self.popover = None
        self.settings = Settings.new()
        self.main_window = main_window
        self.window = None
        self.mode = self.settings.get_enum("preview-mode")

    def show(self, web_view):
        self.preview.pack_start(web_view, True, True, 0)

        if self.mode == self.FULL_WIDTH:
            self.content.remove(self.editor)
            self.content.add(self.preview)

        elif self.mode == self.HALF_WIDTH:
            self.content.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.content.set_size_request(self.text_view.get_min_width() * 2, -1)
            self.content.add(self.preview)

        elif self.mode == self.HALF_HEIGHT:
            self.content.set_orientation(Gtk.Orientation.VERTICAL)
            self.content.set_size_request(-1, 800)
            self.content.add(self.preview)

        elif self.mode == self.WINDOWED:
            self.window = Gtk.Window(title=_("Preview"))
            self.window.set_application(self.main_window.get_application())
            self.window.set_default_size(
                self.main_window.get_allocated_width(), self.main_window.get_allocated_height())
            self.window.set_transient_for(self.main_window)
            self.window.set_modal(False)
            self.window.add(self.preview)
            self.window.connect("delete-event", self.on_window_closed)
            self.window.show()

        else:
            raise ValueError("Unknown preview mode {}".format(self.mode))

        web_view.show()

    def hide(self, web_view):
        if self.mode == self.FULL_WIDTH:
            self.content.remove(self.preview)
            self.content.add(self.editor)

        elif self.mode == self.HALF_WIDTH or self.mode == self.HALF_HEIGHT:
            self.content.remove(self.preview)
            self.content.set_size_request(-1, -1)

        elif self.mode == self.WINDOWED:
            self.window.remove(self.preview)
            self.window.destroy()
            self.window = None

        else:
            raise ValueError("Unknown preview mode {}".format(self.mode))

        self.preview.remove(web_view)

    def update_mode(self, web_view):
        mode = self.settings.get_enum("preview-mode")
        if mode != self.mode:
            if web_view:
                self.hide(web_view)
                self.mode = mode
                self.show(web_view)
            text = self.get_text_for_preview_mode(self.mode)
            self.mode_button.set_label(text)
            if self.popover:
                self.popover.popdown()

    def show_mode_popover(self, _button):
        self.mode_button.set_state_flags(Gtk.StateFlags.CHECKED, False)

        menu = Gio.Menu()
        modes = self.settings.props.settings_schema.get_key("preview-mode").get_range()[1]
        for i, mode in enumerate(modes):
            menu_item = Gio.MenuItem.new(self.get_text_for_preview_mode(i), None)
            menu_item.set_action_and_target_value("app.preview_mode", GLib.Variant.new_string(mode))
            menu.append_item(menu_item)
        self.popover = Gtk.Popover.new_from_model(self.mode_button, menu)
        self.popover.connect('closed', self.on_popover_closed)
        self.popover.popup()

    def on_popover_closed(self, _popover):
        self.mode_button.unset_state_flags(Gtk.StateFlags.CHECKED)

        self.popover = None
        self.text_view.grab_focus()

    def on_window_closed(self, window, _event):
        preview_action = window.get_application().lookup_action("preview")
        preview_action.change_state(GLib.Variant.new_boolean(False))

    def get_text_for_preview_mode(self, mode):
        if mode == self.FULL_WIDTH:
            return _("Full-Width")
        elif mode == self.HALF_WIDTH:
            return _("Half-Width")
        elif mode == self.HALF_HEIGHT:
            return _("Half-Height")
        elif mode == self.WINDOWED:
            return _("Windowed")
        else:
            raise ValueError("Unknown preview mode {}".format(mode))
