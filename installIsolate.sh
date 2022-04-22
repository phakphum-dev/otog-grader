#! /bin/bash
git clone https://github.com/ioi/isolate.git

make --directory=isolate isolate
make --directory=isolate install

rm -r isolate