#!/bin/bash

# Get current date in YYYY-MM-DD format
folder_name=$(date +%Y-%m-%d)

# Create the folder if it doesn't exist
if [ ! -d "$folder_name" ]; then
    mkdir -p "$folder_name"
    echo "Created folder: $folder_name"
else
    echo "Folder $folder_name already exists"
fi

# Change to the folder
cd "$folder_name"

# Get number of files to create from argument (default: 1)
num_files=${1:-1}

# Find the highest ex number from ex*.py and ex*.ipynb files
highest=0
for file in ex*.py ex*.ipynb; do
    if [[ $file =~ ex([0-9]+)\.(py|ipynb) ]]; then
        num=${BASH_REMATCH[1]}
        if (( num > highest )); then
            highest=$num
        fi
    fi
done

# Create next ex files
for ((i=1; i<=num_files; i++)); do
    next=$((highest + i))
    new_file="ex${next}.py"
    touch "$new_file"
    echo "Created $new_file in $folder_name"
done