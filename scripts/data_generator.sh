    #!/bin/bash

    # freely based on https://gitlab.gnome.org/World/lollypop/blob/master/generate_data.sh

function generate_resource()
{
    # TODO: package css styles too
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<gresources>'
    echo '  <gresource prefix="/org/gnome/gitlab/somas/Apostrophe/">'
    for file in ../data/media/css/gtk/*.css
    do
        echo -n '    <file compressed="true">'
        echo -n ${file#*/*/}
        echo '</file>'
    done
    for file in ../data/ui/*.ui About.ui
    do
        echo -n '    <file compressed="true" preprocess="xml-stripblanks">'
        echo -n ${file#*/*/}
        echo '</file>'
    done
    echo '  </gresource>'
    echo '</gresources>'
}

generate_resource > ../data/apostrophe.gresource.xml

