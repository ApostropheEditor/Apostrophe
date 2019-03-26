from gi.repository import Gtk

from uberwriter.Settings import Settings
from uberwriter_lib.helpers import get_css_path


class Theme:
    """
    The Theme enum lists all supported themes using their "gtk-theme-name" value.

    The light variant is listed first, followed by the dark variant, if any.
    """

    settings = Settings.new()

    def __init__(self, name, gtk_css_path, web_css_path, is_dark, inverse_name):
        self.name = name
        self.gtk_css_path = gtk_css_path
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
    def get_current(cls):
        theme_name = Gtk.Settings.get_default().get_property('gtk-theme-name')
        dark_mode = cls.settings.get_value('dark-mode').get_boolean()
        current_theme = cls.get_for_name(theme_name)
        # Technically, we could very easily allow the user to force the light ui on a dark theme.
        # However, as there is no inverse of "gtk-application-prefer-dark-theme", we shouldn't do that.
        if dark_mode and not current_theme.is_dark and current_theme.inverse_name:
            current_theme = cls.get_for_name(current_theme.inverse_name, current_theme.name)
        return current_theme


defaultThemes = [
    # https://gitlab.gnome.org/GNOME/gtk/tree/master/gtk/theme/Adwaita
    Theme('Adwaita', get_css_path('gtk_adwaita.css'),
          get_css_path('web_adwaita.css'), False, 'Adwaita-dark'),
    Theme('Adwaita-dark', get_css_path('gtk_adwaita_dark.css'),
          get_css_path('web_adwaita_dark.css'), True, 'Adwaita'),
    # https://github.com/NicoHood/arc-theme/tree/master/common/gtk-3.0/3.20/sass
    Theme('Arc', get_css_path('gtk_arc.css'),
          get_css_path('web_arc.css'), False, 'Arc-Dark'),
    Theme('Arc-Darker', get_css_path('gtk_arc_darker.css'),
          get_css_path('web_arc_darker.css'), False, 'Arc-Dark'),
    Theme('Arc-Dark', get_css_path('gtk_arc_dark.css'),
          get_css_path('web_arc_dark.css'), True, 'Arc'),
]
