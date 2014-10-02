#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012, Wolf Vollprecht <w.vollprecht@gmail.com>
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
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build uberwriter you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(libdir, values = {}):

    filename = os.path.join(libdir, 'uberwriter_lib/uberwriterconfig.py')
    oldvalues = {}
    try:
        fin = open(filename, 'r', encoding="utf-8")
        fout = open(filename + '.new', 'w', encoding="utf-8")

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError) as e:
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)
    return oldvalues


def move_desktop_file(root, target_data, prefix):
    # The desktop file is rightly installed into install_data.  But it should
    # always really be installed into prefix, because while we can install
    # normal data files anywhere we want, the desktop file needs to exist in
    # the main system to be found.  Only actually useful for /opt installs.
    print("renaming desktop file")
    print(root, target_data, prefix)
    if(root == '/'): root = ''
    old_desktop_path = os.path.normpath(root + target_data +
                                        '/share/applications')
    old_desktop_file = old_desktop_path + '/uberwriter.desktop'
    desktop_path = os.path.normpath(root + prefix + '/share/applications')
    desktop_file = desktop_path + '/uberwriter.desktop'

    if not os.path.exists(old_desktop_file):
        print ("ERROR: Can't find", old_desktop_file)
        sys.exit(1)
    elif target_data != prefix + '/':
        # This is an /opt install, so rename desktop file to use extras-
        desktop_file = desktop_path + '/extras-uberwriter.desktop'
        print(desktop_file, desktop_path)
        try:
            # os.makedirs(desktop_path)
            print('renaming to: %s' % desktop_file)
            os.rename(old_desktop_file, desktop_file)
            os.rmdir(old_desktop_path)
        except OSError as e:
            print ("ERROR: Can't rename", old_desktop_file, ":", e)
            sys.exit(1)

    return desktop_file

def update_desktop_file(filename, target_pkgdata, target_scripts):
    print("updateing deskop file: %s" % filename)
    try:
        fin = open(filename, 'r', encoding="utf-8")
        fout = open(filename + '.new', 'w', encoding="utf-8")

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (target_pkgdata + 'media/uberwriter.svg')
            elif 'Exec=' in line:
                cmd = line.split("=")[1].split(None, 1)
                line = "Exec=%s" % (target_scripts + 'uberwriter')
                if len(cmd) > 1:
                    line += " %s" % cmd[1].strip()  # Add script arguments back
                line += "\n"
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)

    except (OSError, IOError) as e:
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)

def compile_schemas(root, target_data):
    schemadir = os.path.normpath('usr/share/glib-2.0/schemas')
    if (os.path.isdir(schemadir) and
            os.path.isfile('/usr/bin/glib-compile-schemas')):
        os.system('/usr/bin/glib-compile-schemas "%s"' % schemadir)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        DistUtilsExtra.auto.install_auto.run(self)

        target_data = '/' + os.path.relpath(self.install_data, self.root) + '/'
        target_pkgdata = target_data + 'share/uberwriter/'
        target_scripts = '/' + os.path.relpath(self.install_scripts, self.root) + '/'

        values = {'__uberwriter_data_directory__': "'%s'" % (target_pkgdata),
                  '__version__': "'%s'" % self.distribution.get_version()}
        update_config(self.install_lib, values)

        desktop_file = move_desktop_file(self.root, target_data, self.prefix)
        update_desktop_file(desktop_file, target_pkgdata, target_scripts)
        compile_schemas(self.root, target_data)

        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='uberwriter',
    version='1.0',
    license='GPL-3',
    author='Wolf Vollprecht',
    author_email='w.vollprecht@gmail.com',
    description='A beautiful, simple and distraction free markdown editor.',
    long_description="UberWriter, beautiful distraction free writing \
 With UberWriter you get only one thing: An empty textbox, that is to \
 fill with your ideas. There are no settings, you don't have to choose a \
 font, it is only for writing.You can use markdown for all your markup \
 needs. PDF, RTF and HTML are generated with pandoc. For PDF generation it \
 is also required that you choose to install the texlive-luatex package.",
    url='https://launchpad.com/uberwriter',
    cmdclass={'install': InstallAndUpdateDataDirectory},
    package_dir = {
        'gtkspellcheck': 'uberwriter_lib/gtkspellcheck',
        'pylocales': 'uberwriter_lib/pylocales'
    },
    packages=[
        "uberwriter_lib.gtkspellcheck",
        "uberwriter_lib.pylocales",
        "uberwriter_lib",
        "uberwriter"
    ],
    package_data={
        'uberwriter_lib.pylocales' : ['locales.db']
    },
    data_files=[
        ('uberwriter_lib/pylocales', ['uberwriter_lib/pylocales/locales.db']), 
        ('/usr/share/glib-2.0/schemas', ['data/glib-2.0/schemas/net.launchpad.uberwriter.gschema.xml'])]
)