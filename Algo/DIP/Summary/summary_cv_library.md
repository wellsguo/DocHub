
## [OpenCV](https://opencv.org/about/)  

OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial products. Being a BSD-licensed product, OpenCV makes it easy for businesses to utilize and modify the code.





## [vlfeat](http://www.vlfeat.org/)
The VLFeat open source library implements popular computer vision algorithms specializing in image understanding and local features extraction and matching. Algorithms include Fisher Vector, VLAD, SIFT, MSER, k-means, hierarchical k-means, agglomerative information bottleneck, SLIC superpixels, quick shift superpixels, large scale SVM training, and many others. It is written in C for efficiency and compatibility, with interfaces in MATLAB for ease of use, and detailed documentation throughout. It supports Windows, Mac OS X, and Linux. The latest version of VLFeat is 0.9.21.

* Download  
[VLFeat 0.9.21](http://www.vlfeat.org/download/vlfeat-0.9.21-bin.tar.gz) (Windows, Mac, Linux)  
[Source code and installation](http://www.vlfeat.org/download.html)  
 [repository](https://github.com/vlfeat/vlfeat), bug tracking.  
 
* Documentation  
MATLAB commands  
C API with algorithm descriptions  
Command line tools  

* Tutorials  
Features: Covariant detectors, HOG, SIFT, MSER, Quick shift, SLIC  
Clustering: IKM, HIKM, AIB  
Matching: Randomized kd-trees  
All tutorials  

* Example applications  
Caltech-101 classification  
SIFT matching for auto-stitching  
All example applications

## [CCV](http://ccv.nuigroup.com/)

<img src="http://ccv.nuigroup.com/images/screen.jpg" width="400px" height="auto"/>

* About CCV - Community Core Vision  
Community Core Vision, CCV for short is a open source/cross-platform solution for blob tracking with computer vision. It takes an video input stream and outputs tracking data (e.g. coordinates and blob size) and events (e.g. finger down, moved and released) that are used in building multi-touch applications. CCV can interface with various web cameras and video devices as well as connect to various TUIO/OSC/XML enabled applications and supports many multi-touch lighting techniques including: FTIR, DI, DSI, and LLP with expansion planned for the future vision applications (custom modules/filters). This project is developed and maintained by the NUI Group Community.

* Features  
   - **Simple GUI** - The new interface is more intuitive and easier to understand and use.  
   - **Filters** (dynamic background subtraction, high-pass, amplify/scaler, threshold) - This means it will work with all optical setups (FTIR, DI, LLP, DSI). More filters can be added as modules.  
   - **Camera Switching** - Have more than one camera on your computer? Now you can press a button and switch to the next camera on your computer without having to exit the application.  
   - **Input Switching** - Want to use test videos instead of a live camera? Go ahead, press a button and it will switch to video input.  
   - **Dynamic Mesh Calibration **- For people with small or large tables, now you can add calibration points (for large displays) or create less points (smaller displays) while maintaining the same speed and performance.  
   - **Image Reflection** - Now you can flip the camera vertical or horizontal if it is the wrong way.  
   - **Network Broadcasting** - You can send OSC TUIO messages directly from the configapp for quick testing.  
   - **Camera and application FPS details viewer** - Now you can see the framerate of both the tracker and camera that you are getting.  
   - **GPU Mode** - Utilize your GPU engine for accelerated tracking.  
   - **Cross-platform** - This works on Windows, Mac, and Linux.  
   - **Multiple Camera Support** - Camera stitching and calibration for larger environments. (Windows Preview)  
   - **Object/Pattern Tracking** - Tracks fidicuals and objects places on surface.  
   - **External Communications** - External communications with TUIO and other protocols.  

## [BazAR](https://cvlab.epfl.ch/software/descriptors-and-keypoints/bazar/)
BazAR is a computer vision library based on feature points detection and matching. In particular, it is able to quickly detect and register known planar objects in images. Well adapted to Augmented Reality applications, it is the result of advanced computer vision research.


## [ImageJ](https://imagej.nih.gov/ij/index.html)

It can display, edit, analyze, process, save and print 8-bit, 16-bit and 32-bit images. It can read many image formats including TIFF, GIF, JPEG, BMP, DICOM, FITS and "raw". It supports "stacks", a series of images that share a single window. It is multithreaded, so time-consuming operations such as image file reading can be performed in parallel with other operations.

It can calculate area and pixel value statistics of user-defined selections. It can measure distances and angles. It can create density histograms and line profile plots. It supports standard image processing functions such as contrast manipulation, sharpening, smoothing, edge detection and median filtering.

It does geometric transformations such as scaling, rotation and flips. Image can be zoomed up to 32:1 and down to 1:32. All analysis and processing functions are available at any magnification factor. The program supports any number of windows (images) simultaneously, limited only by available memory.

Spatial calibration is available to provide real world dimensional measurements in units such as millimeters. Density or gray scale calibration is also available.

## [ImageMagick](https://imagemagick.org/index.php)

Use ImageMagick® to create, edit, compose, or convert bitmap images. It can read and write images in a variety of formats (over 200) including PNG, JPEG, GIF, HEIC, TIFF, DPX, EXR, WebP, Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and Bézier curves.

ImageMagick is free software delivered as a ready-to-run binary distribution or as source code that you may use, copy, modify, and distribute in both open and proprietary applications. It is distributed under a derived Apache 2.0 license.

ImageMagick utilizes multiple computational threads to increase performance and can read, process, or write mega-, giga-, or tera-pixel image sizes.

## [GraphicsMagick](http://www.graphicsmagick.org/)

GraphicsMagick is the swiss army knife of image processing. Comprised of 267K physical lines (according to David A. Wheeler's SLOCCount) of source code in the base package (or 1,225K including 3rd party libraries) it provides a robust and efficient collection of tools and libraries which support reading, writing, and manipulating an image in over 88 major formats including important formats like DPX, GIF, JPEG, JPEG-2000, PNG, PDF, PNM, and TIFF.

Image processing is multi-threaded (see the multi-thread benchmark results) using OpenMP so that CPU-bound tasks scale linearly as processor cores are added. OpenMP support requires compilation with GCC 4.2 (or later), or use of any C compiler supporting at least the OpenMP 2.0 specification.

GraphicsMagick is quite portable, and compiles under almost every general purpose operating system that runs on 32-bit or 64-bit CPUs. GraphicsMagick is available for virtually any Unix or Unix-like system, including Linux. It also runs under Windows 2000 and later (Windows 2000, XP, Vista, 7, 8.X, 10), and MacOS-X.

GraphicsMagick supports huge images and has been tested with gigapixel-size images. GraphicsMagick can create new images on the fly, making it suitable for building dynamic Web applications. GraphicsMagick may be used to resize, rotate, sharpen, color reduce, or add special effects to an image and save the result in the same or different image format. Image processing operations are available from the command line, as well as through C, C++, Lua, Perl, PHP, Python, Tcl, Ruby, Windows .NET, or Windows COM programming interfaces. With some modification, language extensions for ImageMagick may be used.

## [OpenVSS](https://github.com/djhmateer/OpenVSSolution)
OpenVSS - 开放平台的视频监控系统 - 是一个系统级别的视频监控软件视频分析框架（VAF）的视频分析与检索和播放服务，记录和索引技术。它被设计成插件式的支持多摄像头平台，多分析仪模块（OpenCV的集成），以及多核心架构。 



## [OpenPR](http://www.openpr.org.cn/)
Pattern Recognition project（开放模式识别项目），致力于开发出一套包含图像处理、计算机视觉、自然语言处理、模式识别、机器学习和相关领域算法的函数库。 

## [cvBlob](https://github.com/Steelskin/cvblob)
cvBlob 是计算机视觉应用中在二值图像里寻找连通域的库.能够执行连通域分析与特征提取. 


## [C++计算机视觉库 Integrating Vision Toolkit](https://github.com/junaidnaseer/ivt)
Integrating Vision Toolkit (IVT) 是一个强大而迅速的C++计算机视觉库，拥有易用的接口和面向对象的架构，并且含有自己的一套跨平台GUI组件，另外可以选择集成OpenCV


## [ImageNets]()
ImageNets 是对OpenCV 的扩展，提供对机器人视觉算法方面友好的支持，使用Nokia的QT编写界面。 

## [opencv-processing](https://github.com/atduskgreg/opencv-processing)

A Processing library for the OpenCV computer vision library.

## [cognitivej](https://github.com/CognitiveJ/cognitivej)

### CognitiveJ - Image Analysis in Java
 [![Apache-2.0 license](http://img.shields.io/badge/license-Apache-brightgreen.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)
  [ ![Download](https://api.bintray.com/packages/cognitivej/CognitiveJ/CognitiveJ/images/download.svg) ](https://bintray.com/cognitivej/CognitiveJ/CognitiveJ/_latestVersion)
   [![Circle CI](https://circleci.com/gh/CognitiveJ/cognitivej.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/CognitiveJ/cognitivej)

CognitiveJ is an open-source fluent Java (8) API that manages and orchestrates the interaction between Java applications and 
Microsofts’ Cognitive (Project Oxford) Machine Learning & Image Processing libraries and allows you to query and analyze images.   

![](https://iwkelly.files.wordpress.com/2016/05/screen-shot-2016-05-11-at-11-54-02.png) 

**Faces**

*   Facial Detection – Capture faces, gender, age and associated facial features and landmarks from an image
*   Emotion Detection – Derive emotional state from faces within an image
*   Verification – Verify, with a confidence scale on whether 2 different faces are of the same person
*   Identification – Identify a person from a set of known people.
*   Find Similar – detect, group and rank similar faces
*   Grouping – group people based on facial characteristics
*   Person Group/Person/Face Lists; Create, manage and train groups, face lists and persons to interact with the identification/grouping/find similar face features.


**Vision**

*   Image Describe - Describe visual content of an image and return real world caption to what the Image is of.
*   Image Analysis – extract key details from an image and if the image is of an adult/racy nature.
*   OCR – detect and extract text from an image.
*   Thumbnail – Create thumbnail images based on key points of interest from the image.

**Overlay _(Experimental)_**

*   Apply image layers onto images to visually represent found features.
*   Apply captions onto faces and images
*   Graphically illustrate the Faces/Vision feature sets.
*   Pixelate faces in an image.

**Other Features**

*   Works with local or remote images
*   validation of parameters

## [Java Image Filters](http://www.jhlabs.com/ip/filters/index.html)


