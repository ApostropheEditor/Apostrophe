find . -name \*.po -execdir sh -c 'msgfmt "$0" -o uberwriter.mo' '{}' \; 

