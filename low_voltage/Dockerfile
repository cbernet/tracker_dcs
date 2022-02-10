FROM centos:centos7

WORKDIR /usr/app

RUN yum install -y epel-release
RUN yum install -y python-pip
RUN pip install --upgrade "pip < 21.0"

#install the PyVISA-py PyVISA package via pip
RUN pip install PyVISA-py PyVISA

#install rpm & deltarpm  
RUN yum install -y rpm
RUN yum install -y deltarpm # otherwise: it complains : Delta RPMs disabled because /usr/bin/applydeltarpm not installed.

#install unzip  
RUN yum install -y unzip 

#add the rsvisa-centos_5.12.1-1.x86_64.rpm package (provided by Pierre)
#COPY rsvisa-centos_5.12.1-1.x86_64.rpm /usr/app/LowVoltage_packages/

#Download ni-software.zip archive at National Instrument : https://www.ni.com/fr-fr/support/downloads/drivers/download.ni-linux-device-drivers.html#349661

#COPY NILinux2019DeviceDrivers.zip /usr/app/LowVoltage_packages/

WORKDIR /usr/app/LowVoltage_packages/

COPY driver . 

##install the rsvisa-centos_5.12.1-1.x86_64.rpm package
RUN rpm -ivh --nodeps rsvisa-centos_5.12.1-1.x86_64.rpm

#unzip  ni-software
RUN unzip NILinux2019DeviceDrivers.zip

#Install ni-software-2019-19.2.0.49152-0 + f0.el7.noarch.rpm : which configures NI repositories on Centos
RUN rpm -ivh --nodeps ni-software-2019-19.2.0.49152-0+f0.el7.noarch.rpm 

#install the libivivisa0 ni-icp.noarch ni-visa ni-daqmx kernel-devel packages
RUN yum install -y libusb # libvisa requires usb device-  without this /usr/lib64/librsvisa.so: libusb-1.0.so.0: cannot open shared object file
RUN yum install -y libivivisa0
RUN yum install -y ni-icp.noarch
RUN yum install -y ni-visa
RUN yum install -y ni-daqmx
RUN yum install -y kernel-devel

COPY HMP4040.py /usr/app/LowVoltage_packages/
#CMD ["python" , "./HMP4040.py"]
