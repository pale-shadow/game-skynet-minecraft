aclocal
autoreconf -fi
automake --add-missing
source .venv/bin/activate
./configure
make python
