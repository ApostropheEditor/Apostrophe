project(
  'uberwriter',
  version: '2.2.0',
  license: 'GPL2+',
  meson_version: '>= 0.50.0'
)

if get_option('profile') == 'development'
  profile = 'Devel'
  name_suffix = ' (Development)'
  vcs_tag = run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
  if vcs_tag == ''
    version_suffix = '-devel'
  else
    version_suffix = '-@0@'.format (vcs_tag)
  endif
else
  profile = ''
  name_suffix = ''
  version_suffix = ''
endif
application_id = 'de.wolfvollprecht.UberWriter@0@'.format(profile)


# This doesn't work yet. It's doesn't find the python3 from the sandboxed env first
# python = import('python')
# python3 = python.find_installation('python3')
python = import('python3')
python3 = python.find_python()
if not python3.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif
gnome  = import('gnome')
i18n   = import('i18n')


dependency('glib-2.0')
dependency('gobject-2.0')
dependency('gobject-introspection-1.0')
dependency('gtk+-3.0')

find_program('glib-compile-schemas', required: true)
find_program('gtk-update-icon-cache', required: false)
find_program('update-desktop-database', required: false)

gettext_package = meson.project_name()
localedir = get_option('prefix') / get_option('localedir')
pythondir = get_option('prefix') / python.sysconfig_path('purelib')
datadir = get_option('prefix') / get_option('datadir')
pkgdatadir = datadir / meson.project_name()
podir = meson.source_root() / 'po'

subdir('bin')
subdir('data')
subdir('help')
subdir('po')

meson.add_install_script('build-aux/meson_post_install.py')
