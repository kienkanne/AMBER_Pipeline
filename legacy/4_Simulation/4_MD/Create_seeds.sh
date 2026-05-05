#!/usr/bin/bash
set -euo pipefail

TEMPLATE="${1:?Usage: The template directory to be copied}"
N="${2:?Usage: The number of copies}"

for i in $(seq 1 "$N"); do
    dir="${i}_seed"
    if [ -d "$dir" ]; then
	    echo "Skipping $dir"
	    continue
    fi

    # Copy template
    cp -r "$TEMPLATE" "$dir"

    # Replace placeholders in all relevant files
    find "$dir" -type f \( -name "*.in" -o -name "*.sh" -o -name "*.mdin" \) | while read -r file; do
        sed -i "s/__SEED__/${i}/g" "$file"
    done

    echo "Created $dir with __SEED__=$i"
done
