rm -f source/wnnet.*.rst
mkdir -p source/_static source/_templates
sphinx-apidoc -M -f -o -n source ../layerspy
make html
