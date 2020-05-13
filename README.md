[![Please do not theme this app](https://stopthemingmy.app/badge.svg)](https://stopthemingmy.app)

# Apostrophe

![](screenshots/main.png)

## About

Apostrophe is a GTK+ based distraction free Markdown editor, mainly developed by Wolf Vollprecht and Manuel Genovés. It uses pandoc as backend for markdown parsing and offers a very clean and sleek user interface.

## Install

You can get Apostrophe on Flathub!
[Get it now](https://flathub.org/apps/details/org.gnome.gitlab.somas.Apostrophe)

Unofficial builds are also available for some platforms:
* Nix(OS): [`pkgs.apostrophe`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/apostrophe/default.nix)
* ArchLinux (AUR)
* [Fedora](https://src.fedoraproject.org/rpms/apostrophe): `sudo dnf install apostrophe`

## Contributions and localization

If you want to help to localize the project, just join us at [Poeditor](https://poeditor.com/join/project/gxVzFyXb2x)
Any help is appreciated!

## Building with GNOME Builder

The easiest method, just follow [this guide](https://wiki.gnome.org/Newcomers/BuildProject), you'll be up and running in one minute.

## Building from Git

```bash
$ git clone https://gitlab.gnome.org/somas/apostrophe/
$ cd apostrophe
$ meson builddir --prefix=/usr
# sudo ninja -C builddir install
```

To use apostrophe, please make sure you have some dependencies installed:

- `meson` and `ninja-build` are required to build and install Apostrophe
- Pandoc, the program used to convert Markdown to basically anything else (the package name should be pandoc in most distributions)
- GTK3 and GLib development packages need to be installed: libgtk3-dev libglib2.0-dev`
- webkit2gtk is also needed for the preview panel
- GSpell and GObject-introspection libraries for spell checking: `gobject-introspection libgirepository1.0-dev gir1.2-gspell1 gettext`
- Please find these packages on your distribution/pip: `python3 python3-regex python3-setuptools python3-levenshtein python3-enchant python3-gi python3-cairo python3-pypandoc`
- Optional dependencies are `texlive` and `texlie-latex-extra` for the pdftex module; `libjs-mathjax` for formula preview.

Depending where you install it you may need to install the schemas before:

```bash
# sudo cp data/org.gnome.gitlab.somas.Apostrophe.gschema.xml /usr/share/glib-2.0/schemas/org.gnome.gitlab.somas.Apostrophe.gschema.xml
# sudo glib-compile-schemas /usr/share/glib-2.0/schemas
```

### Building a flatpak package

It's also possible to build, run and debug a flatpak package. You'll need flatpak-builder for this:

```bash
$ cd build-aux/flatpak
$ flatpak-builder --force-clean --install --user _build org.gnome.gitlab.somas.Apostrophe.json
```
