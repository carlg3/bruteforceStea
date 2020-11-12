rm bruteforceStea.exe
pyinstaller -c --clean --distpath ./ -F -i icon.ico bruteforceStea.py
rm -d -r build
rm bruteforceStea.spec
