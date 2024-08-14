#!/bin/bash

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

VERSION="1.0.2"

wget https://github.com/jgthms/bulma/releases/download/$VERSION/bulma-$VERSION.zip
unzip bulma-$VERSION.zip
cd bulma-$VERSION

npm install

cp $DIR/build.scss .

node_modules/.bin/sass --style=expanded build.scss output.css
node_modules/.bin/postcss output.css --no-map --use cssnano --output $DIR/bulma-components-$VERSION.min.css
rm output.css
