pkgname=apostrophe
_pkgname=apostrophe
pkgver=2.1.3
pkgrel=1
pkgdesc='A distraction free Markdown editor for GNU/Linux made with GTK+'
arch=('any')
url='https://world.pages.gitlab.gnome.org/apostrophe/'
license=('GPL3')
depends=('gtk3' 'pandoc' 'gspell')
makedepends=('python-setuptools')
optdepends=('texlive-core' 'otf-fira-mono: Recommended font')
provides=("$_pkgname")
conflicts=("$_pkgname")
source=('git+https://gitlab.gnome.org/somas/apostrophe')
sha256sums=('SKIP')

pkgver() {
    cd $_pkgname
    git describe --long --tags | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g'
}

build() {
    cd $_pkgname
    python setup.py build
}

package() {
    cd $_pkgname
    python setup.py install --skip-build --root="$pkgdir" --optimize=1
}

post_install() {
    /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
}
post_upgrade() {
    /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
}
post_remove() {
    /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
}
