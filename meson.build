project(
  'apostrophe',
  version: '2.2.0',
  meson_version: '>= 0.50.0'
)

if get_option('profile') == 'development'
  profile = '.Devel'
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
application_id = 'org.gnome.wolf.Apostrophe@0@'.format(profile)


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
pythondir = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
datadir = get_option('prefix') / get_option('datadir')
bindir = join_paths(get_option('prefix'), get_option('bindir'))
pkgdatadir = datadir / meson.project_name()
podir = meson.source_root() / 'po'

conf = configuration_data()
conf.set('PACKAGE_URL', 'https://somas.pages.gitlab.gnome.org/apostrophe/')
conf.set('DATA_DIR', datadir)
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
conf.set('PYTHON_DIR', pythondir)
conf.set('VERSION', meson.project_version())
conf.set('PYTHON', python3.path())


subdir('data')
#subdir('help')
subdir('po')

install_subdir(
  'apostrophe',
  install_dir: pythondir
)

message('Preparing init file')
configure_file(
  input: 'apostrophe.in',
  output: 'apostrophe',
  configuration: conf,
  install_dir: bindir
)

meson.add_install_script('build-aux/meson_post_install.py')

