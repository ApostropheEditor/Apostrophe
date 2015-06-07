Uberwriter
==========

Uberwriter is a GTK+ based distraction free Markdown editor, mainly developed by Wolf Vollprecht. It uses pandoc as backend for markdown parsing and offers a very clean and sleek user interface.

To use uberwriter, please make sure you have some dependencies installed:

- Pandoc, the program used to convert Markdown to basically anything else (the package name should be pandoc in most distributions)
- Use pip to install python dependencies: `sudo pip3 install -r requirements.txt`
- Of course, gtk3 etc. needs to be installed as well since this is a gtk application
  - Please find these packages on your distribution: `python3 python3-regex python3-distutils-extra python3-levenshtein python3-enchant python3-gi python3-cairo`

It should be possible to install UberWriter with `sudo python3 setup.py install --root=/`
