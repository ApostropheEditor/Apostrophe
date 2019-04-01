gnome = import('gnome')

message('Compiling resources')

# gnome.compile_resources(
#   meson.project_name(),
#   meson.project_name() + '.gresource.xml',
#   gresource_bundle: true,
#   source_dir: '.',
#   install_dir: DATA_DIR,
#   install: true,
#   dependencies: configure_file(
#     input: 'AboutDialog.ui.in',
#     output: 'AboutDialog.ui',
#     configuration: conf
#   )
# )

# Installing the schema file 
install_data(
  project_id + '.gschema.xml',
  install_dir: 'share/glib-2.0/schemas'
)

# Merging the translations with the desktop file
# i18n.merge_file(
#   output: project_id + '.desktop',
#   input: project_id + '.desktop.in',
#   po_dir: join_paths(meson.source_root(), 'subprojects/po'),
#   type: 'desktop',
#   install: true,
#   install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'applications')
# )

# Validating the desktop file
desktop_file_validate = find_program('desktop-file-validate', required:false)
if desktop_file_validate.found()
  test (
    'Validate desktop file',
    desktop_file_validate,
    args: join_paths(meson.current_build_dir (), project_id + '.desktop')
  )
  message(join_paths(meson.current_build_dir (), project_id + '.desktop'))
endif

# Merging the translations with the appdata file
# i18n.merge_file(
#   output: project_id + '.appdata.xml',
#   input: project_id + '.appdata.xml.in',
#   po_dir: join_paths(meson.source_root(), 'subprojects/po'),
#   install: true,
#   install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'metainfo')
# )

# Validating the appdata file
appstreamcli = find_program('appstream-util', required: false)
if appstreamcli.found()
  test (
    'Validate appdata file',
    appstreamcli,
    args: ['validate-relax', join_paths(meson.current_build_dir (), project_id + '.appdata.xml')]
  )
endif

# Validating schemas
compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif


message('Making a list of icons')
# subdir('icons')
