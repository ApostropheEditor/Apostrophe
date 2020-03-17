function generate_po()
{
    >LINGUAS
    for po in *.po
    do
        msgmerge -N $po uberwriter.pot > /tmp/$$language_new.po
        mv /tmp/$$language_new.po $po
        language=${po%.po}
        echo $language >>LINGUAS
    done

    find . -name \*.po -execdir sh -c 'msgfmt "$0" -o uberwriter.mo' '{}' \; 

}

generate_po

