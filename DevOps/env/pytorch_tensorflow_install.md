
https://blog.csdn.net/zhangxinyu11021130/article/details/64125058

## 安装anconda

Download ancoda from https://www.anaconda.com/download/#linux. and installing as follow command:
>bash ./Anaconda2-5.1.0-Linux-x86_64.sh

## 安装pytorch

### Via conda
To install a previous version of PyTorch via Anaconda or Miniconda, replace “0.1.12” in the following commands with the desired version (i.e., “0.2.0”).

- Installing with CUDA 8

>conda install pytorch=0.1.12 cuda80 -c soumith

- Installing with CUDA 7.5

>conda install pytorch=0.1.12 cuda75 -c soumith

- Installing without CUDA

>conda install pytorch=0.1.12 -c soumith

## 安装tensorflow

[1] https://www.tensorflow.org/install/  
[2] https://www.tensorflow.org/install/install_linux

### Install TensorFlow

Assuming the prerequisite software is installed on your Linux host, take the following steps:

1. Install TensorFlow by invoking one of the following commands:
>\$ pip install tensorflow      # Python 2.7; CPU support (no GPU support)  
\$ pip3 install tensorflow     # Python 3.n; CPU support (no GPU support)  
\$ pip install tensorflow-`gpu`  # Python 2.7;  GPU support  
\$ pip3 install tensorflow-`gpu` # Python 3.n; GPU support

	If the preceding command runs to completion, you should now validate your installation.

2. (Optional.) If Step 1 failed, install the latest version of TensorFlow by issuing a command of the following format:
>\$ sudo pip  install --upgrade tfBinaryURL   # Python 2.7  
>\$ sudo pip3 install --upgrade tfBinaryURL   # Python 3.n
	
    where tfBinaryURL identifies the URL of the TensorFlow Python package. The appropriate value of tfBinaryURL depends on the operating system, Python version, and GPU support. Find the appropriate value for tfBinaryURL here. For example, to install TensorFlow for Linux, Python 3.4, and CPU-only support, issue the following command:
> \$ sudo pip3 install --upgrade 
 https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.8.0-cp34-cp34m-linux_x86_64.whl
 
	If this step fails, see [Common Installation Problems](https://www.tensorflow.org/install/install_linux#common_installation_problems).

### Next Steps
After installing TensorFlow, [validate your installation](https://www.tensorflow.org/install/install_linux#ValidateYourInstallation).

### Uninstalling TensorFlow
To uninstall TensorFlow, issue one of following commands:

>\$ sudo pip uninstall tensorflow  # for Python 2.7  
\$ sudo pip3 uninstall tensorflow # for Python 3.n


## 编译安装dlib

These instructions assume you don't have an nVidia GPU and don't have Cuda and cuDNN installed and don't want GPU acceleration (since none of the current Mac models support this).

1. Clone the code from github:
>git clone https://github.com/davisking/dlib.git

2. Build the main dlib library (optional if you just want to use Python):
>cd dlib  
>mkdir build; cd build; cmake .. -DDLIB_USE_CUDA=0 -DUSE_AVX_INSTRUCTIONS=1; cmake --build .

3. Build and install the Python extensions:
>cd ..  
>python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA

	At this point, you should be able to `run python3` and type `import dlib` successfully.


## Linux下系统自带python和Anaconda切换 

1. 在安装anconda后，系统会修改当前用户的配置文件(<code>~/.bashrc</code>)，加入
<code>export PATH="/home/myname/anaconda2/bin:$PATH"</code>.

2. 通过别名实现不同系统默认python和Anconda下python的切换.
>alias py27="/usr/bin/python2.7"   
>alias pyana="/home/*`username`*/anaconda2/bin/python2.7" # 一定要精确到python的版本，不能只到文件夹

