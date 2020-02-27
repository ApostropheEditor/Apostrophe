from gettext import gettext as _

from gi.repository import Gtk, Gio, GLib

from uberwriter import headerbars
from uberwriter.settings import Settings
from uberwriter.styled_window import StyledWindow


class PreviewRenderer:
    """Renders the preview according to the user selected mode."""

    # Must match the order/index defined in gschema.xml
    FULL_WIDTH = 0
    HALF_WIDTH = 1
    HALF_HEIGHT = 2
    WINDOWED = 3

    def __init__(
            self, main_window, content, editor, text_view):
        self.main_window = main_window
        self.main_window.connect("delete-event", self.on_window_closed)
        self.content = content
        self.editor = editor
        self.text_view = text_view

        self.settings = Settings.new()
        self.popover = None
        self.window = None
        self.headerbar = None

        self.mode = self.settings.get_enum("preview-mode")
        self.update_mode()

    def show(self, web_view):
        """Show the preview, depending on the currently selected mode."""

        # Windowed preview: create a window and show the preview in it.
        if self.mode == self.WINDOWED:
            # Create transient window of the main window.
            self.window = StyledWindow(application=self.main_window.get_application())
            self.window.connect("delete-event", self.on_window_closed)

            # Create a custom header bar and move the mode button there.
            headerbar = headerbars.PreviewHeaderbar()
            self.headerbar = headerbar.hb
            self.headerbar.set_title(_("Preview"))
            self.window.set_titlebar(headerbar.hb_container)

            # Position it next to the main window.
            width, height = self.main_window.get_size()
            self.window.resize(width, height)
            x, y = self.main_window.get_position()
            if x is not None and y is not None:
                self.main_window.move(x, y)
                self.window.move(x + width + 16, y)

            # Add webview and show.
            self.window.add(web_view)
            self.window.show()

        else:
            self.content.pack_start(web_view, True, True, 0)

            # Full-width preview: swap editor with preview.
            if self.mode == self.FULL_WIDTH:
                self.content.remove(self.editor)

            # Half-width preview: set horizontal orientation and add the preview.
            # Ask for a minimum width that respects the editor's minimum requirements.
            elif self.mode == self.HALF_WIDTH:
                self.content.set_orientation(Gtk.Orientation.HORIZONTAL)
                self.content.set_size_request(self.text_view.get_min_width() * 2, -1)

            # Half-height preview: set vertical orientation and add the preview.
            # Ask for a minimum height that provides a comfortable experience.
            elif self.mode == self.HALF_HEIGHT:
                self.content.set_orientation(Gtk.Orientation.VERTICAL)
                self.content.set_size_request(-1, 768)

            else:
                raise ValueError("Unknown preview mode {}".format(self.mode))

        web_view.show()

    def hide(self, web_view):
        """Hide the preview, depending on the currently selected mode."""

        # Windowed preview: remove preview and destroy window.
        if self.mode == self.WINDOWED:
            self.main_window.present()
            self.headerbar = None
            self.window.remove(web_view)
            self.window.destroy()
            self.window = None

        else:
            self.content.remove(web_view)

            # Full-width preview: swap preview with editor.
            if self.mode == self.FULL_WIDTH:
                self.content.add(self.editor)

            # Half-width/height previews: remove preview and reset size requirements.
            elif self.mode == self.HALF_WIDTH or self.mode == self.HALF_HEIGHT:
                self.content.set_size_request(-1, -1)

            else:
                raise ValueError("Unknown preview mode {}".format(self.mode))

    def update_mode(self, web_view=None):
        """Update preview mode, adjusting the mode button and the preview itself."""

        mode = self.settings.get_enum("preview-mode")
        if web_view and mode != self.mode:
            self.hide(web_view)
            self.mode = mode
            self.show(web_view)
        else:
            self.mode = mode

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
