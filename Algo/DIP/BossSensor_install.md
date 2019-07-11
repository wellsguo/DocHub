## BossSensor

### Install

1. Download
> git clone https://github.com/Hironsan/BossSensor.git

2. Install requrements
> conda create -n venv python=3.5 # create an virture environment  
> source activate venv  
> \# conda install -c https://conda.anaconda.org/menpo opencv3  
> conda install -c conda-forge tensorflow  
> pip install -r requirements.txt

3. Compile OpenCV with ffmpeg
There are some solutions for [for OpenCV3](http://www.erogol.com/installing-opencv-3-2-anaconda-environment-ffmpeg-support/) or by this [url](https://qiita.com/ikeyasu/items/49cd5d0ad02fece5fa62) and some one [for OpenCV2](http://dhaneshr.net/2016/06/03/installing-opencv-2-4-x-with-ffmpeg-python-on-anaconda/) or [this](https://askubuntu.com/questions/988137/build-opencv-with-ffmpeg-support).



### Usage
1. Train boss image.
> python boss_train.py

2. start BossSensor. 
> python camera_reader.py