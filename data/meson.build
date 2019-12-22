# FreeDesktop Desktop File
desktop_conf = configuration_data()
desktop_conf.set('icon', application_id)
desktop_file = i18n.merge_file(
  'desktop',
  input: configure_file(
    input: 'de.wolfvollprecht.UberWriter.desktop.in.in',
    output: '@BASENAME@',
    configuration: desktop_conf
  ),
  output: '@0@.desktop'.format(application_id),
  po_dir: podir,
  type: 'desktop',
  install: true,
  install_dir: get_option('datadir') / 'applications'
)

# Validate Desktop File
desktop_file_validate = find_program('desktop-file-validate', required: false)
if desktop_file_validate.found()
  test (
    'Validate desktop file',
    desktop_file_validate,
    args: desktop_file.full_path()
  )
endif

# Freedesktop AppData File
appdata_conf = configuration_data()
appdata_conf.set('app-id', application_id)
appdata_conf.set('gettext-package', gettext_package)
appdata_file = i18n.merge_file(
  'appdata',
  input: configure_file(
    input: 'de.wolfvollprecht.UberWriter.appdata.xml.in.in',
    output: '@BASENAME@',
    configuration: appdata_conf
  ),
  output: '@0@.appdata.xml'.format(application_id),
  po_dir: podir,
  install: true,
  install_dir: get_option('datadir') / 'metainfo'
)
# Validate AppData File
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test (
    'Validate appdata file',
    appstream_util,
    args: ['validate-relax', '--nonet', appdata_file.full_path()]
  )
endif

# Gschema
install_data(
	'de.wolfvollprecht.UberWriter.gschema.xml',
	install_dir:  get_option('datadir') / 'glib-2.0' / 'schemas',
	rename: '@0@.gschema.xml'.format(application_id)
)

# Resources
ui_config = configuration_data()
ui_config.set('app-id', application_id)
ui_config.set('version', meson.project_version() + version_suffix)
ui_config.set('package_url', 'http://uberwriter.github.io/uberwriter/')
ui_preconfigured_files = files(
  'ui/About.ui.in'
)
ui_dependencies = []
foreach ui_file: ui_preconfigured_files
  ui_dependencies += configure_file(
    input:  ui_file,
    output: '@BASENAME@',
    configuration: ui_config
  )
endforeach

resources = gnome.compile_resources(
  meson.project_name(),
  meson.project_name() + '.gresource.xml',
  gresource_bundle: true,
  install:true,
  install_dir: join_paths(datadir, meson.project_name()),
  dependencies: ui_dependencies
)
message('datadir')
message(datadir)
subdir('icons')

install_subdir(
	'lua',
	install_dir: pkgdatadir
)
install_subdir(
	'media',
	install_dir: pkgdatadir
)
install_subdir(
	'ui',
	install_dir: pkgdatadir
)
install_subdir(
	'reference_files',
	install_dir: pkgdatadir
)
