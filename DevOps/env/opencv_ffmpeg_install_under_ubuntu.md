`NOTE:` FFMpeg's version must be matched for a certain OpenCV(i.e. OpenCV3.3.1 with FFMpeg3.2)

[1] [Install OpenCV3 on Ubuntu](https://www.learnopencv.com/install-opencv3-on-ubuntu/)  
[2] [Compile OpenCV (and ffmpeg) on Ubuntu Linux](http://www.wiomax.com/compile-opencv-and-ffmpeg-on-ubuntu/)




## Intall ffmpeg

### Removing any pre-installed ffmpeg and x264
>sudo apt-get -qq remove x264 libx264-dev ffmpeg  
sudo apt-get --purge remove libav-tools  
sudo apt-get --purge autoremove

### Install dependencies
>sudo apt-get -qq install libopencv-dev build-essential checkinstall cmake pkg-config yasm libjpeg-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev python-dev python-numpy libtbb-dev libqt4-dev libgtk2.0-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils

### Install ffmpeg
>git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg  
cd ffmpeg  
./configure --enable-nonfree --enable-pic --enable-shared  
make  
sudo make install

## Install OpenCV

### Update packages
>sudo apt-get update  
sudo apt-get upgrade

### Install OS libraries
>sudo apt-get install build-essential checkinstall cmake pkg-config yasm  
sudo apt-get install git gfortran  
sudo apt-get install libjpeg8-dev libjasper-dev libpng12-dev
 

>\# If you are using Ubuntu 14.04  
sudo apt-get install libtiff4-dev  
\# If you are using Ubuntu 16.04  
sudo apt-get install libtiff5-dev

 
>sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev  
sudo apt-get install libxine2-dev libv4l-dev  
sudo apt-get install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev  
sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev  
sudo apt-get install libatlas-base-dev  
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev  
sudo apt-get install libvorbis-dev libxvidcore-dev  
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev  
sudo apt-get install x264 v4l-utils  
 
>\# Optional dependencies  
sudo apt-get install libprotobuf-dev protobuf-compiler  
sudo apt-get install libgoogle-glog-dev libgflags-dev  
sudo apt-get install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen 

### Install Python libraries
>sudo apt-get install python-dev python-pip python3-dev python3-pip  
>sudo -H pip2 install -U pip numpy  
>sudo -H pip3 install -U pip numpy  
	
We will use Virtual Environment to install Python libraries. It is generally a good practice in order to separate your project environment and global environment.
>\# Install virtual environment  
sudo pip2 install virtualenv virtualenvwrapper  
sudo pip3 install virtualenv virtualenvwrapper  
echo "# Virtual Environment Wrapper"  >> ~/.bashrc  
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc  
source ~/.bashrc  
  
>\############ For Python 2 ############  
\# create virtual environment  
mkvirtualenv facecourse-py2 -p python2  
workon facecourse-py2  
  
>\# now install python libraries within this virtual environment  
pip install numpy scipy matplotlib scikit-image scikit-learn ipython  
  
>\# quit virtual environment  
deactivate  
\######################################
  
>\############ For Python 3 ############  
\# create virtual environment  
mkvirtualenv facecourse-py3 -p python3  
workon facecourse-py3  
  
>\# now install python libraries within this virtual environment  
pip install numpy scipy matplotlib scikit-image scikit-learn ipython    


>\# quit virtual environment  
deactivate  
\######################################


### Download OpenCV and OpenCV_contrib
>git clone https://github.com/opencv/opencv.git
cd opencv 
git checkout 3.3.1 
cd ..

>git clone https://github.com/opencv/opencv_contrib.git  
cd opencv_contrib  
git checkout 3.3.1  
cd ..  

### Compile and install OpenCV with contrib modules
>\#Create a build directory  
cd opencv  
sudo mkdir build  
cd build  

>\#Run CMake  
sudo cmake \  
    -D CMAKE_BUILD_TYPE=RELEASE \  
    -D CMAKE_INSTALL_PREFIX=/usr/local \  
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \  
    -D WITH_CUDA=ON \  
    -D BUILD_TIFF=ON \  
    -D WITH_TBB=ON  \   
    -D WITH_QT=ON  \  
    -D WITH_OPENGL=ON  \  
    -D WITH_FFMPEG=ON  \  
    -D ENABLE_AVX=ON  \  
    -D WITH_OPENCL=ON \  
    -D WITH_IPP=ON \  
    -D WITH_EIGEN=ON \  
    -D WITH_V4L=ON  \  
    -D WITH_VTK=OFF  \  
    -D BUILD_opencv_java=OFF \  
    -D BUILD_opencv_python2=OFF \  
    -D BUILD_TESTS=OFF \  
    -D BUILD_PERF_TESTS=OFF \  
    -D CMAKE_INSTALL_PREFIX=\$(python3 -c "import sys; print(sys.prefix)") \  
    -D PYTHON3_EXECUTABLE=\$(which python3) \  
    -D PYTHON3_INCLUDE_DIR=\$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \  
    -D PYTHON3_PACKAGES_PATH=\$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \  
    -D BUILD_NEW_PYTHON_SUPPORT=ON \  
    -D INSTALL_PYTHON_EXAMPLES=ON \  
    -D INSTALL_C_EXAMPLES=ON \  
    -D BUILD_EXAMPLES=ON ..  

>\# Compile and Install    
make -j4  
sudo make install  
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'  
sudo ldconfig  

>find /usr/local/lib/ -type f -name "cv2*.so"  
\#It should output paths similar to one of these (or two in case OpenCV was compiled for both Python2 and Python3):  


>\############ For Python 2 ############  
>\## binary installed in dist-packages  
/usr/local/lib/python2.6/dist-packages/cv2.so  
/usr/local/lib/python2.7/dist-packages/cv2.so  
\## binary installed in site-packages  
/usr/local/lib/python2.6/site-packages/cv2.so  
/usr/local/lib/python2.7/site-packages/cv2.so  
  
>\############ For Python 3 ############  
>\## binary installed in dist-packages  
/usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-x86_64-linux-gnu.so  
/usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so  
\## binary installed in site-packages  
/usr/local/lib/python3.5/site-packages/cv2.cpython-35m-x86_64-linux-gnu.so  
/usr/local/lib/python3.6/site-packages/cv2.cpython-36m-x86_64-linux-gnu.so  
Double check the exact path on your machine before running the following commands  

>\############ For Python 2 ############  
>cd ~/.virtualenvs/facecourse-py2/lib/python2.7/site-packages  
ln -s /usr/local/lib/python2.7/dist-packages/cv2.so cv2.so  
  
>\############ For Python 3 ############  
cd ~/.virtualenvs/facecourse-py3/lib/python3.6/site-packages  
ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so

### Test OpenCV3

#### Test C++
>\# compile  
\# There are backticks ( \` ) around pkg-config command not single quotes  
g\+\+ \-std=c++11 removeRedEyes.cpp \`pkg-config --libs --cflags opencv\` -o removeRedEyes  
\# run  
./removeRedEyes

#### Test Python
>workon facecourse-py3

>\# open ipython (run this command on terminal)  
ipython  
\# import cv2 and print version (run following commands in ipython)  
import cv2  
print(cv2.\_\_version\_\_)  
\# If OpenCV3 is installed correctly,  
\# above command should give output 3.3.1  
\# Press CTRL+D to exit ipython  
  
>\#Run RedEyeRemover demo  
python removeRedEyes.py  

>\#Now you can exit from Python virtual environment.  
deactivate

