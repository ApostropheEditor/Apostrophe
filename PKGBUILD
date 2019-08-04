pkgname=uberwriter
pkgver=2.1.5
pkgrel=1
pkgdesc="A distraction free Markdown editor for GNU/Linux made with GTK+"
arch=('any')
url="https://uberwriter.github.io"
license=('GPL3')
depends=('gtk3' 'webkit2gtk' 'gspell' 'python-pypandoc' 'python-regex' 'python-levenshtein' 
	'python-pyenchant' 'python-cairo')
makedepends=('python-setuptools')
optdepends=('texlive-core: For the pdftex module' 'otf-fira-mono: Recommended font')
source=("$pkgname-$pkgver.tar.gz::https://github.com/UberWriter/uberwriter/archive/v$pkgver.tar.gz")
sha256sums=('2b62cecfdbe226d71fa86778b08a2d7500e43c28eaeea9bb574a57eb6cd7d15e')

 build() {
    cd "$pkgname-$pkgver"
    python setup.py build
}

 package() {
    cd "$pkgname-$pkgver"
    python setup.py install --skip-build --root="$pkgdir" --optimize=1
}
