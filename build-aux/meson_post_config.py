#!/usr/bin/env python3

import os
import subprocess

build_root = os.environ.get('MESON_BUILD_ROOT')
source_root = os.environ.get('MESON_SOURCE_ROOT')

print('Install schemas in build dir...')
subprocess.call(['glib-compile-schemas', source_root + '/data/'])
subprocess.call(['mkdir', '-p', build_root + '/data/glib-2.0/schemas'])
subprocess.call(['mv', source_root + '/data/gschemas.compiled', build_root + '/data/glib-2.0/schemas'])
