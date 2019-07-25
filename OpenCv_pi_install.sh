#!/bin/bash

. common.sh

checkroot
doing_updates

echo Enabling Camera
$rcn do_camera 0

if [[ $do_installs == true ]]; then
  echo Lets install some files
  $apti read-edid i2c-tools wiringpi git vim
  $apti libgirepository-1.0 gir1.2-glib
  $apti libavutil-dev libavcodec-dev libavformat-dev libsdl2-dev
  $apti libpython3-dev python3-pip python3-smbus python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0
  $apti liblapack3 libcblas3 libatlas-dev libatlas3-base libjasper1 openexr libswscale4 libqtgui4 libqt4-test
  $apti python-gi python3-gi \
    gstreamer1.0-tools \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-libav
  $apti gstreamer1.0-tools gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good,ugly,bad}
  $apti gstreamer1.0-omx-rpi-config gstreamer1.0-omx

  $apti uvcdynctrl
fi

usermod -a -G video pi
if ! grep -q bcm2835-v4l2 /etc/modules ; then
    echo bcm2835-v4l2 >> /etc/modules
fi

function setup_vkc_python_env() {
if [ ! -d ${pyvenv_dir} ] ; then
	echo creating environment
    pyvenv-3.5 --system-site-packages ${pyvenv_dir}
fi

. ${pyvenv_dir}/bin/activate

python -m pip install --user pip
python -m pip install opencv-python Pillow "picamera[array]"

deactivate

}

export -f setup_vkc_python_env
su pi -c "bash -c setup_vkc_python_env"

echo REBOOT!!!
# vim: set ts=4 sw=4 tw=0 noet: expandtab:





#sudo apt-get update && sudo apt-get upgrade

#E: Package 'libcblas3' has no installation candidate
#E: Package 'libatlas-dev' has no installation candidate
#E: Unable to locate package numpy
#E: Unable to locate package matplotlib


#!/bin/bash

: ${do_uninstalls:=false}
: ${do_installs:=false}
: ${create_pyvenv:=false}
: ${do_build:=false}
: ${do_git:=false}
: ${do_opencv_install:=false}

: ${pyvenv_dir:=/home/pi/.pyvenv/opencv}
: ${src_dir:=/home/pi/src/opencv}
: ${opencv_version:=4.1.0}

echo "do_uninstalls:     $do_uninstalls"
echo "do_installs:       $do_installs"
echo "create_pyvenv:     $create_pyvenv"
echo "do_build:          $do_build"
echo "do_git:            $do_git"
echo "do_opencv_install: $do_opencv_install"
echo "pyvenevdir:        $pyvenv_dir"
echo "src_dir:           $src_dir"
echo "opencv_version:    $opencv_version"




pkgs=(vim)

# basic build stuff
pkgs+=(build-essential cmake unzip pkg-config git)

#images
pkgs+=(libjpeg-dev libpng-dev libtiff-dev)
# audio
pkgs+=(libavcodec-dev libavformat-dev)
# video
pkgs+=(libxvidcore-dev libx264-dev)

# gtk
pkgs+=(libgtk-3-dev libgtk2.0-dev)
pkgs+=("libcanberra-gtk*")

pkgs+=(libatlas-base-dev gfortran liblapack-dev libeigen3-dev)

pkgs+=(python3-dev python3-venv python3-virtualenv python-virtualenv)
pkgs+=(python3-gi python3-gi-cairo gir1.2-gtk-3.0 virtualenvwrapper)
pkgs+=(liblapack3 libcblas3 libatlas-dev libatlas3-base libjasper1)
pkgs+=(libdc1394-22-dev libv4l-dev)

pkgs+=(libgstreamer1.0-0 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev)
pkgs+=(gstreamer1.0-tools gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-libav)
pkgs+=(gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good,ugly,bad})
pkgs+=(gstreamer1.0-omx-rpi-config gstreamer1.0-omx)

# we'll use virtual envs for python
pypkgs=(numpy matplotlib)

if[[ ${do_uninstalls} == true]] ; then
  get purge wolfram-engine
  sudo apt-get purge libreoffice*
  sudo apt-get clean
  sudo apt-get autoremove
fi

if [[ ${do_installs} == true ]] ; then
  apt install ${pkgs[@]}
  sed -i 's/^CONF_SWAPSIZE=*?$/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
  systemctl restart dphys-swapfile
  exit
fi

if [[ ${create_pyvenv} == true ]] ; then
  #virtualenv --system-site-packages --python=`which python3.5m` ${pyvenv_dir}
  source ${pyvenv_dir}/bin/activate
  python -m pip install ${pypkgs[@]}
  deactivate

#  if ! grep -q venv ~/.profile ; then
#    cat >> ~/.profile << "EOF"
#
## venv
#export WORKON_HOME=$HOME/.pyvenv
#export VIRTUALENVWRAPPER_PYTHON=`which python3`
#source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
#EOF
#  fi
fi

[[ -d ${src_dir} ]] || mkdir -p ${src_dir}
cd ${src_dir}

if [[ ${do_git} == true ]] ; then
  git clone https://github.com/opencv/opencv.git
  cd opencv
  git checkout tags/${opencv_version}
  cd ..

  git clone https://github.com/opencv/opencv_contrib.git
  cd opencv_contrib
  git checkout tags/${opencv_version}
  cd ..
fi

if [[ ${do_build} == false ]] ; then
  exit
fi

mkdir build
cd build

source ${pyvenv_dir}/bin/activate
if [[ $do_opencv_install == true ]] ; then
  make install
else
  if [[ -d ../opencv ]] ; then
    #add_opts=""
    #add_opts+=" -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules"
    #add_opts+=" -D BUILD_opencv_python2=OFF"
    cmake \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D BUILD_DOCS=OFF \
      -D BUILD_TESTS=OFF \
      -D BUILD_EXAMPLES=OFF \
      -D PYTHON3_EXECUTABLE=${pyvenv_dir}/bin/python \
      -D PYTHON_DEFAULT_EXECUTABLE=${pyvenv_dir}/bin/python \
      -D BUILD_NEW_PYTHON_SUPPORT=ON \
      -D WITH_GSTREAMER=ON \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D WITH_TBB=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      ${add_opts} \
      ../opencv
    make -j5

    if ! grep -q opencv ~/.profile ; then
      cat >> ~/.profile << "EOF"

# opencv
export PATH=$PATH:/usr/local/lib
export LD_LIBRARY_PATH=$LD_LIRARY_PATH:/usr/local/lib
EOF

    fi
  fi
fi

deactivate
