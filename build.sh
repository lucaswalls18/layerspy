# Script to automate build for PyPI.

rm -fr dist
cd python
rm -fr xsd_pub
git clone https://bitbucket.org/mbradle/xmlcoll_xsd.git xsd_pub
cd ..
python -m pip install --upgrade build
python -m build
