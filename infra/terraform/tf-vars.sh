#!/usr/bin/env bash
set -o allexport

if [ -f ./../../.env ]; then
    while IFS='=' read -r key value; do
        # Ignore les lignes vides et celles qui commencent par #
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue

        key_lowercase=$(echo "$key" | tr '[:upper:]' '[:lower:]')
        export TF_VAR_"$key_lowercase"="$value"
    done < <(grep -v '^#' ./../../.env | grep -v '^[[:space:]]*$')
fi

set +o allexport

"$@"
