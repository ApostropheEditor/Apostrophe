sassc = find_program('sassc', required: false)
if not sassc.found() and not get_option('sassc').disabled()
  subproject('sassc')
  sassc = find_program('sassc', required: get_option('sassc').enabled())
endif

if sassc.found()
  sassc_opts = [ '-a', '-M', '-t', 'compact' ]

  style_deps = [
    custom_target('Stylesheet-adwaita',
      input: 'Adwaita.scss',
      output: 'Adwaita.css',
      command: [
        sassc, sassc_opts, '@INPUT@', '@OUTPUT@',
      ],
      depend_files: files([
       '_definitions.scss',
       '_drawing.scss',
       '_recoloring.scss',
       'base.scss',
       'Adwaita.scss',
      ]),
    ),
    custom_target('Stylesheet-adwaita-dark',
      input: 'Adwaita-dark.scss',
      output: 'Adwaita-dark.css',
      command: [
        sassc, sassc_opts, '@INPUT@', '@OUTPUT@',
      ],
      depend_files: files([
       '_definitions.scss',
       '_drawing.scss',
       '_recoloring.scss',
       'base.scss',
       'Adwaita-dark.scss'
      ]),
    ),
    custom_target('Stylesheet-adwaita-sepia',
      input: 'Adwaita-sepia.scss',
      output: 'Adwaita-sepia.css',
      command: [
        sassc, sassc_opts, '@INPUT@', '@OUTPUT@',
      ],
      depend_files: files([
       '_definitions.scss',
       '_drawing.scss',
       '_recoloring.scss',
       'base.scss',
       'Adwaita.scss'
      ]),
    ),
  ]
endif
