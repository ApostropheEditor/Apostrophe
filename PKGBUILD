pkgname=uberwriter
_pkgname=uberwriter
pkgver=2.1.2
pkgrel=1
pkgdesc='A distraction free Markdown editor for GNU/Linux made with GTK+'
arch=('any')
url='http://uberwriter.github.io/uberwriter/'
license=('GPL3')
depends=('gtk3' 'pandoc' 'python-gtkspellcheck')
makedepends=('python-setuptools')
optdepends=('texlive-core' 'otf-fira-mono: Recommended font')
provides=("$_pkgname")
conflicts=("$_pkgname")
source=('git+https://github.com/UberWriter/uberwriter.git'
        'uberwriter.patch')
sha256sums=('SKIP'
            '11f4c27a7f8ae954dd69f691b3a2c49db019cbc3c6a2e4c4a1a47293162e3d1b')

pkgver() {
    cd $_pkgname
    git describe --long --tags | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g'
}

prepare() {
    cd $_pkgname
    patch -Np1 -i "${srcdir}/uberwriter.patch"
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
