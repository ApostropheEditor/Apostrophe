from gi.repository import Gtk

from apostrophe.settings import Settings
from apostrophe.helpers import get_css_path


class Theme:
    """
    The Theme enum lists all supported themes using their "gtk-theme-name" value.

    The light variant is listed first, followed by the dark variant, if any.
    """

    previous = None
    settings = Settings.new()

    def __init__(self, name, web_css_path, is_dark, inverse_name):
        self.name = name
        self.web_css_path = web_css_path
        self.is_dark = is_dark
        self.inverse_name = inverse_name

    @classmethod
    def get_for_name(cls, name, default=None):
        current_theme = default or defaultThemes[0]
        for theme in defaultThemes:
            if name == theme.name:
                current_theme = theme
        return current_theme

    @classmethod
    def get_current_changed(cls):
        theme_name = Gtk.Settings.get_default().get_property('gtk-theme-name')
        dark_mode = cls.settings.get_boolean('dark-mode')
        current_theme = cls.get_for_name(theme_name)
        if dark_mode != current_theme.is_dark and current_theme.inverse_name:
            current_theme = cls.get_for_name(current_theme.inverse_name, current_theme.name)
        changed = current_theme != cls.previous
        cls.previous = current_theme
        return current_theme, changed

    @classmethod
    def get_current(cls):
        current_theme, _ = cls.get_current_changed()
        return current_theme

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.name == other.name and \
               self.web_css_path == other.web_css_path and \
               self.is_dark == other.is_dark and \
               self.inverse_name == other.inverse_name


defaultThemes = [
    # https://gitlab.gnome.org/GNOME/gtk/tree/master/gtk/theme/Adwaita
    Theme('Adwaita', get_css_path('web/adwaita.css'), False, 'Adwaita-dark'),
    Theme('Adwaita-dark', get_css_path('web/adwaita.css'), True, 'Adwaita'),
    # https://github.com/NicoHood/arc-theme/tree/master/common/gtk-3.0/3.20/sass
    Theme('Arc', get_css_path('web/arc.css'), False, 'Arc-Dark'),
    Theme('Arc-Darker', get_css_path('web/arc.css'), False, 'Arc-Dark'),
    Theme('Arc-Dark', get_css_path('web/arc.css'), True, 'Arc'),
    # https://gitlab.gnome.org/GNOME/gtk/tree/master/gtk/theme/HighContrast
    Theme('HighContrast', get_css_path('web/highcontrast.css'), False, 'HighContrastInverse'),
    Theme('HighContrastInverse', get_css_path('web/highcontrast_inverse.css'), True, 'HighContrast')
]
