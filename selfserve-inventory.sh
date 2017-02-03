#!/bin/bash

set -eu

# where root of puppet again checkout is
PUPPET_AGAIN=${PUPPET_AGAIN:-../puppet}
# node def relative to $PUPPET_AGAIN
PUPPET_NODES=${PUPPET_NODES:-manifests/moco-nodes.pp}

NODE_PATH=$PUPPET_AGAIN/$PUPPET_NODES

warn() { for m; do echo "$m"; done 1>&2 ; }
die() { warn "$@" ; exit 1; }
usage() { warn "$@" "${USAGE:-}"; test $# -eq 0 ; exit $?; }

if ! test -r $NODE_PATH; then
    usage "Can't read $PUPPET_NODES under $PUPPET_AGAIN" \
        "set 'PUPPET_AGAIN' to your local checkout"
fi

# one liner to get nodes, piped into subshell to JSONify it
grep -B 12 selfserve_agent $NODE_PATH | grep -w node | cut -d\" -f2 |
(
    cat <<EOF
{
    "selfserve_agents": [
EOF
    leader="      "
    while read node; do
        echo "${leader}\"$node\""
        leader="    , "
    done
    cat <<EOF
    ]
}
EOF
) # subshell end

