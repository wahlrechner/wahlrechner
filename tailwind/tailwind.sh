#!/usr/bin/env bash

cd "$(dirname "$0")"
npx tailwindcss -i ../wahlrechner/static/wahlrechner/styles.css -o ../static/tailwind/styles.css --minify --watch