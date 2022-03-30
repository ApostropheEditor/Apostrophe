project(
  'apostrophe',
  version: '2.6.2',
  meson_version: '>= 0.50.0'
)

# Importing modules

gnome  = import('gnome')
i18n   = import('i18n')
python = import('python')

py_installation = python.find_installation('python3')
python_version = py_installation.language_version()
python_version_req = '>=3.8'
if not py_installation.found()
    error('No valid python3 binary found')
endif
if not python_version.version_compare(python_version_req)
  error('Requires Python @0@, @1@ found.'.format(python_version_req, python_version))
endif

# Handling of devel versions

if get_option('profile') == 'development'
  message('devel version')
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
application_id = 'org.gnome.gitlab.somas.Apostrophe@0@'.format(profile)

# Dependencies

dependency('glib-2.0')
dependency('gobject-2.0')
dependency('gobject-introspection-1.0')
dependency('gtk+-3.0')
dependency('libhandy-1')

find_program('glib-compile-schemas', required: true)
find_program('gtk-update-icon-cache', required: false)
find_program('update-desktop-database', required: false)

gettext_package = meson.project_name()
localedir = get_option('prefix') / get_option('localedir')
pythondir = py_installation.get_path('purelib')
datadir = get_option('prefix') / get_option('datadir')
pkgdatadir = datadir / meson.project_name()
#bindir = join_paths(get_option('prefix'), get_option('bindir'))
podir = meson.source_root() / 'po'


subdir('data')
#subdir('help')
subdir('po')

install_subdir(
  'apostrophe',
  install_dir: py_installation.get_install_dir()
)

# System installation

conf = configuration_data()
conf.set('PACKAGE_URL', 'https://apps.gnome.org/app/org.gnome.gitlab.somas.Apostrophe/')
conf.set('DATA_DIR', datadir)
conf.set('PKGDATA_DIR', pkgdatadir)
conf.set('LOCALE_DIR', join_paths(datadir, 'locale'))
conf.set('PYTHON_DIR', pythondir)
conf.set('VERSION', meson.project_version())
conf.set('LOCAL_BUILD', 'False')

conf.set('PROFILE', profile)
conf.set('APP_ID', application_id)

configure_file(
  input: 'apostrophe.in',
  output: 'apostrophe',
  configuration: conf,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'config.py.in',
  output: 'config.py',
  configuration: conf,
  install_dir: py_installation.get_install_dir() / 'apostrophe'
)

# Local installation

local_config = configuration_data()
local_config.set('DATA_DIR', join_paths(meson.build_root(), 'data'))
local_config.set('PKGDATA_DIR', join_paths(meson.build_root(), 'data'))
local_config.set('PACKAGE_URL', 'https://apps.gnome.org/app/org.gnome.gitlab.somas.Apostrophe/')
local_config.set('LOCALE_DIR', join_paths(datadir, 'locale'))
local_config.set('PYTHON_DIR', meson.source_root())
local_config.set('PROFILE', profile)
local_config.set('APP_ID', application_id)

local_config.set('SCHEMAS_DIR', join_paths(meson.build_root(), 'data'))
local_config.set('LOCAL_BUILD', 'True')

configure_file(
  input: 'apostrophe.in',
  output: 'local-apostrophe',
  configuration: local_config
)

meson.add_install_script('build-aux/meson_post_install.py')
meson.add_install_script('build-aux/meson_post_config.py')

