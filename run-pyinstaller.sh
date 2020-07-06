
rm -rf dist/* build/*

pipenv run pyinstaller L1L2_subs.spec

/c/Program\ Files/7-Zip/7z a -r dist/L1L2_subs.zip dist/L1L2_subs
