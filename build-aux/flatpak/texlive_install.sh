# Download the installer! 
# Currently using 2017 edition, upgrade to 2018 tomorrow! (just released, needs)
# time to propagate everywhere
wget ftp://tug.org/historic/systems/texlive/2019/install-tl-unx.tar.gz
myhash=$(sha256sum install-tl-unx.tar.gz | cut -d' ' -f1)
if [ $myhash != "44aa41b5783e345b7021387f19ac9637ff1ce5406a59754230c666642dfe7750" ] ; then echo "CHECKSUM MISMATCH!"; exit 1 ; fi

tar xvf install-tl-unx.tar.gz

# The texlive profile sets some variables for the installation
# so the installer doesn't use the text user interface
# Most importantly (besides the paths') is "selected-scheme"
# Currently set to scheme-minimal which installs almost nothing
# (which is great for testing, but less for actual usage! :)

cat <<EOF > texlive.profile
# texlive.profile written on Sat Apr 28 18:37:30 2018 UTC
# It will NOT be updated and reflects only the
# installation profile at installation time.
selected_scheme scheme-basic
TEXDIR /app/extensions/TexLive/2019
TEXMFCONFIG ~/.texlive2019/texmf-config
TEXMFHOME ~/texmf
TEXMFLOCAL /app/extensions/TexLive/texmf-local
TEXMFSYSCONFIG /app/extensions/TexLive/2019/texmf-config
TEXMFSYSVAR /app/extensions/TexLive/2019/texmf-var
TEXMFVAR ~/.texlive2019/texmf-var
binary_x86_64-linux 1
collection-latex 1
collection-binextra 1
collection-fontsrecommended 1
instopt_adjustpath 0
instopt_adjustrepo 1
instopt_letter 0
instopt_portable 1
instopt_write18_restricted 1
tlpdbopt_autobackup 1
tlpdbopt_backupdir tlpkg/backups
tlpdbopt_create_formats 1
tlpdbopt_desktop_integration 1
tlpdbopt_file_assocs 1
tlpdbopt_generate_updmap 0
tlpdbopt_install_docfiles 0
tlpdbopt_install_srcfiles 0
tlpdbopt_post_code 1
tlpdbopt_sys_bin /usr/local/bin
tlpdbopt_sys_info /usr/local/share/info
tlpdbopt_sys_man /usr/local/share/man
tlpdbopt_w32_multi_user 1
EOF

# Makefile which is required by flatpak ... so this one is almost empty
# except for the install command which uses the texlive installer to download
# all the packages!

cat <<EOF > Makefile
all:
	echo "I am a pretty empty Makefile."

install:
	./install-tl-20190410/install-tl --profile texlive.profile
EOF
