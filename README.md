[![Please do not theme this app](https://stopthemingmy.app/badge.svg)](https://stopthemingmy.app)

# Uberwriter
==========

![](screenshots/main.png)

## About

Uberwriter is a GTK+ based distraction free Markdown editor, mainly developed by Wolf Vollprecht. It uses pandoc as backend for markdown parsing and offers a very clean and sleek user interface.

## Install

You can get UberWriter on Flathub!
[Get it now](https://flathub.org/apps/details/de.wolfvollprecht.UberWriter)

## Contributions and localization

If you want to help to localize the project, just join us at [Poeditor](https://poeditor.com/join/project/gxVzFyXb2x)
Any help is appreciated!

## Building from Git

```bash
$ git clone https://github.com/UberWriter/uberwriter.git`
$ cd uberwriter
$ meson builddir --prefix=/usr
# sudo ninja -C builddir install
```

To use uberwriter, please make sure you have some dependencies installed:

- Pandoc, the program used to convert Markdown to basically anything else (the package name should be pandoc in most distributions)
- Of course, gtk3 etc. needs to be installed as well since this is a gtk application
- webkit2gtk is also needed for the preview panel
- Please find these packages on your distribution: `python3 python3-regex python3-setuptools python3-levenshtein python3-enchant python3-gi python3-cairo`
- Optional dependencies are `texlive` for the pdftex module.

### Running it without installing it

You can run UberWriter with `./uberwriter.in` without installing it in the system,
but you'll need to install and compile the schemas before:

```bash
# sudo cp data/de.wolfvollprecht.UberWriter.gschema.xml /usr/share/glib-2.0/schemas/de.wolfvollprecht.UberWriter.gschema.xml
# sudo glib-compile-schemas /usr/share/glib-2.0/schemas
```

### Building a flatpak package

It's also possible to build, run and debug a flatpak package. You'll need flatpak-builder for this:

```bash
$ cd build-aux/flatpak
$ flatpak-builder --force-clean --install --user _build de.wolfvollprecht.UberWriter.json
```
