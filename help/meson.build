help_pages = files(
	'index.page',
	'pandocs-markdown.page',
	'preview.page'
)

help_media = files(
	'figures/icon.png',
	'figures/icon_down.png'
)

gnome.yelp(meson.project_name(),
    sources: help_pages,
    media: help_media,
    symlink_media: true
)
