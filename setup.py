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


##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################
from setuptools import setup
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

extra_files_ui = package_files('./data/ui')
extra_files_media = package_files('./data/media')
from pprint import pprint
pprint(extra_files_ui)
pprint(extra_files_media)

if os.environ.get('IN_FLATPAK'):
    app_prefix = '/app/'
else:
    app_prefix = ''

setup(
    name='uberwriter',
    version='1.0',
    license='GPL-3',
    author='Wolf Vollprecht',
    author_email='w.vollprecht@gmail.com',
    description='A beautiful, simple and distraction free markdown editor.',
    long_description="""UberWriter, beautiful distraction free writing
 With UberWriter you get only one thing: An empty textbox, that is to 
 fill with your ideas. There are no settings, you don't have to choose a 
 font, it is only for writing.You can use markdown for all your markup 
 needs. PDF, RTF and HTML are generated with pandoc. For PDF generation it 
 is also required that you choose to install the texlive-luatex package.""",
    url='https://github.com/wolfv/uberwriter/',
    # cmdclass={'install': InstallAndUpdateDataDirectory},
    package_dir = {
        # "": '/opt/uberwriter/'
    },
    packages=[
        "uberwriter_lib.gtkspellcheck",
        "uberwriter_lib.pylocales",
        # "uberwriter_lib.pressagio",
        "uberwriter_lib",
        "uberwriter",
        "po"
        # "uberwriter.plugins"
        # "uberwriter.plugins.bibtex"
    ],
    include_package_data=True,

    package_data={
        'uberwriter_lib.pylocales' : ['locales.db'],
    },
    data_files=[
        (app_prefix + '/bin/', ['bin/uberwriter']),
        (app_prefix + '/share/glib-2.0/schemas', ['data/glib-2.0/schemas/net.launchpad.uberwriter.gschema.xml']),
        (app_prefix + '/share/glib-2.0/schemas', ['data/de.wolfvollprecht.UberWriter']),
        (app_prefix + '/share/icons/hicolor/scalable/apps', ['data/media/uberwriter.svg']),
        (app_prefix + '/share/applications', ['de.wolfvollprecht.UberWriter.desktop']),
        (app_prefix + '/opt/uberwriter/data/ui', extra_files_ui),
        (app_prefix + '/opt/uberwriter/data/media', extra_files_media)
    ]
)
