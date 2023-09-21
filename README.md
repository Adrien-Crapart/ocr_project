Download Poppler
wget https://poppler.freedesktop.org/poppler-21.09.0.tar.xz
tar -xvf poppler-21.09.0.tar.xz

Install some dependencies(if missing)
sudo apt update
sudo apt install poppler-utils
sudo apt install tesseract-ocr
sudo apt-get install libnss3 libnss3-dev
sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev
sudo apt-get install cmake libblkid-dev e2fslibs-dev libboost-all-dev libaudit-dev
sudo apt-get install libopenjp2-7-dev -y

Make install
cd poppler-21.09.0/
mkdir build
cd build/
cmake -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_INSTALL_PREFIX=/usr \
 -DTESTDATADIR=$PWD/testfiles \
 -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
 ..
make
sudo make install

export PATH="/usr/bin/tesseract:$PATH"
