# FreeDesktop Desktop File
desktop_conf = configuration_data()
desktop_conf.set('icon', application_id)
desktop_file = i18n.merge_file(
  'desktop',
  input: configure_file(
    input: 'org.gnome.gitlab.somas.Apostrophe.desktop.in.in',
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

metainfo_configured = configure_file(
    input: 'org.gnome.gitlab.somas.Apostrophe.metainfo.xml.in',
    output: 'configured' + '@BASENAME@',
    configuration: appdata_conf
)

# merge NEWS into metainfo file
# TODO: uncomment when https://github.com/hughsie/appstream-glib/issues/369 is solved
# ascli_exe = find_program('appstreamcli')
# metainfo_with_relinfo = custom_target('gen-metainfo-rel',
#     input : ['../NEWS', metainfo_configured],
#     output : ['org.gnome.gitlab.somas.Apostrophe.metainfo.xml.in'],
#     command : [ascli_exe, 'news-to-metainfo', '--limit=2', '@INPUT0@', '@INPUT1@', '@OUTPUT@']
# )

appdata_file = i18n.merge_file(
  'appdata',
  input: metainfo_configured,
  output: '@0@.metainfo.xml'.format(application_id),
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
	'org.gnome.gitlab.somas.Apostrophe.gschema.xml',
	install_dir:  get_option('datadir') / 'glib-2.0' / 'schemas',
	rename: '@0@.gschema.xml'.format(application_id)
)

# Resources
ui_config = configuration_data()
ui_config.set('app-id', application_id)
ui_config.set('version', meson.project_version() + version_suffix)
ui_config.set('package_url', 'https://somas.pages.gitlab.gnome.org/apostrophe/')
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

message('datadir')
message(datadir)
subdir('icons')

install_subdir(
	'lua',
	install_dir: pkgdatadir
)

subdir('media/css/gtk')
install_subdir(
	'media',
  # exclude_directories: 'css/gtk'
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

resources = gnome.compile_resources(
  meson.project_name(),
  meson.project_name() + '.gresource.xml',
  gresource_bundle: true,
  install:true,
  install_dir: pkgdatadir,
  dependencies: [ui_dependencies, style_deps]
)
