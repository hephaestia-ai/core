#!/usr/bin/env zsh
# sh scripts/build.sh 1.0.0 

# Builds the python project
# Uploads to pypi
# Takes the tag for the release via CLI 
# Then deletes the files from dist/* for next upload 

error() {
    # Check if the first argument ($1) or tag is provided
    if [[ -z $1 ]]; then
        echo "Error: No argument provided. Usage: $0 <argument>"
    exit 1
fi
}

build() {
    python -m build 
    echo "Project built" 
}

upload() {
    twine upload dist/*
    gh release create v$1 dist/*.tar.gz
    echo "Github release published" 
}

cleanup() {
    rm dist/*
}

error $1  
build
upload $1  
cleanup