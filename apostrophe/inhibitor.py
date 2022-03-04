# Copyright (C) 2022 Manuel Genovés <manuel.genoves@gmail.com>
# Copyright (C) 2017 Jason Gray <jasonlevigray3@gmail.com>
# Copyright (C) 2017 Franz Dietrich <dietrich@teilgedanken.de>
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

from gettext import gettext as _

from apostrophe.helpers import App


class Inhibitor:

    def __init__(self):
        self.__cookie = 0

    def inhibit(self, flags):
        """
            Disable flags
            @param flags as Gtk.ApplicationInhibitFlags
        """
        if not self.__cookie:
            self.__cookie = App().inhibit(
                App().get_active_window(),
                flags,
                _("Unsaved documents"))

    def uninhibit(self):
        """
            Remove all the powermanagement settings
        """
        if self.__cookie:
            App().uninhibit(self.__cookie)
            self.__cookie = 0
