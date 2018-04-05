Uberwriter
==========

Uberwriter is a GTK+ based distraction free Markdown editor, mainly developed by Wolf Vollprecht. It uses pandoc as backend for markdown parsing and offers a very clean and sleek user interface.

To use uberwriter, please make sure you have some dependencies installed:

- Pandoc, the program used to convert Markdown to basically anything else (the package name should be pandoc in most distributions)
- Of course, gtk3 etc. needs to be installed as well since this is a gtk application
  - Please find these packages on your distribution: `python3 python3-regex python3-distutils-extra python3-levenshtein python3-enchant python3-gi python3-cairo`

You can build UberWriter with `sudo python3 setup.py build`, 
and then run it with `./bin/uberwriter`

It's also possible to build, run and debug a flatpak package. You'll need flatpak-builder for this:

- cd to the flatpak dir of the repo
- flatpak-builder --install --force-clean some_folder_name uberwriter.json # this installs and cleans the build folder)
- flatpak run de.wolfvollprecht.UberWriter
- you can also debug with the following: flatpak-builder --run --share=network some_folder_name uberwriter.json sh
