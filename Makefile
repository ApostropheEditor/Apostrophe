.PHONY: flatpak-user-install flatpak-generate-python-modules

flatpak-user-install:
	cd flatpak; flatpak-builder --force-clean --install --user _build uberwriter.json

flatpak-generate-python-modules:
	# gtkspellcheck's setup.py wants enchant to already be installed
	flatpak-pip-generator --output flatpak/python3-enchant.json pyenchant
	flatpak-pip-generator --output flatpak/python3-packages.json `grep -v enchant requirements.txt`
