Uberwriter
==========

Uberwriter is a GTK+ based distraction free Markdown editor, mainly developed by Wolf Vollprecht. It uses pandoc as backend for markdown parsing and offers a very clean and sleek user interface.

To use uberwriter, please make sure you have some dependencies installed:

- Pandoc, the program used to convert Markdown to basically anything else (the package name should be pandoc in most distributions)
- Of course, gtk3 etc. needs to be installed as well since this is a gtk application
- Please find these packages on your distribution: `python3 python3-regex python3-setuptools python3-levenshtein python3-enchant python3-gi python3-cairo`

You can run UberWriter with `./bin/uberwriter` without installing it in the system,
but you'll need to install and compile the schemas before:
`sudo cp data/de.wolfvollprecht.UberWriter.gschema.xml /usr/share/glib-2.0/schemas/de.wolfvollprecht.UberWriter.gschema.xml`
`sudo glib-compile-schemas /usr/share/glib-2.0/schemas`

It's also possible to build, run and debug a flatpak package. You'll need flatpak-builder for this:

- cd to the flatpak dir of the repo
- `flatpak-builder --install --force-clean some_folder_name uberwriter.json` (this installs and cleans the build folder)
- `flatpak run de.wolfvollprecht.UberWriter`

If you can't find Uberwriter after this, it's due to a Flatpak bug. Try to export it to a local repo before installing it:

- `cd flatpak`
- `flatpak-builder --repo=org.foo.Uberwriter --force-clean build uberwriter.json`
- `flatpak remote-add --no-gpg-verify user org.foo.Uberwriter`
- `flatpak install foo de.wolfvollprecht.UberWriter`

Where `org.foo.repo` is the name of your repo, you can change 'foo' with the name you want
Then you can run it as before or from your system launcher.

If you want to update an existing installation, just run

- `flatpak update de.wolfvollprecht.UberWriter`

You can also debug it with the following: `flatpak-builder --run --share=network some_folder_name uberwriter.json sh`

If you want to install it using setuptools, simply run `python3 setup.py build install`