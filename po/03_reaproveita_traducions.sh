#!/bin/bash

# messages_gl.po antigo traducido
# gl.po novo a traducir

#msgmerge messages_gl.po gl.po > messages_gl_merged.po
msgmerge  orcana_version_anterior.po orcana_limpo.po -o orcana_nova_version.po

exit 0
