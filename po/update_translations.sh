function generate_po()
{
    >LINGUAS
    for po in */LC_MESSAGES/*.po
    do
        msgmerge -N $po apostrophe.pot > /tmp/$$language_new.po
        mv /tmp/$$language_new.po $po
        language=${po%.po}
        echo $language >>LINGUAS
    done

    find . -name \*.po -execdir sh -c 'msgfmt "$0" -o apostrophe.mo' '{}' \; 

}

generate_po

