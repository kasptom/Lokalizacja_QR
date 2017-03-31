# http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
# place this file next to opencv and opencv_contrib directory
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D WITH_TBB=ON \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D WITH_V4L=ON \
-D WITH_QT=ON \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
-D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
-D ENABLE_PRECOMPILED_HEADERS=OFF \
..
#-D INSTALL_C_EXAMPLES=ON \
#-D INSTALL_PYTHON_EXAMPLES=ON \
#-D BUILD_EXAMPLES=ON \
#-D INSTALL_C_EXAMPLES=OFF \

# In case of HDF5 problem append these at the end of CMake list
# https://github.com/opencv/opencv/issues/6050
#find_package(HDF5)
#include_directories(${HDF5_INCLUDE_DIRS})
#
#into modules/python/common.cmake
