# BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
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

from gi.repository import Gio


class Settings(Gio.Settings):

    """
        Apostrophe Settings
    """

    def __init__(self):
        """
            Init Settings
        """
        Gio.Settings.__init__(self)

    @classmethod
    def new(cls):
        """
            Return a new Settings object
        """
        settings = Gio.Settings.new("org.gnome.gitlab.somas.Apostrophe")
        settings.__class__ = Settings
        return settings
