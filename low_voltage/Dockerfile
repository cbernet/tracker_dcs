#FROM  --platform=linux/amd64 centos:centos7 
FROM  centos:centos7
#CMD uname -m

WORKDIR /usr/app

RUN yum update -y
#RUN yum install -y epel-release
RUN yum install -y python3

RUN python3 -m pip install --upgrade
RUN python3 -m pip install -U PyVISA-py PyVISA

#======for python2=============================//
#RUN yum install -y python-pip
#RUN pip install --upgrade 
#RUN pip install PyVISA-py PyVISA
#==============================================//

#====install rpm & deltarpm====================// 
RUN yum install -y rpm
RUN yum provides applydeltarpm
RUN yum install -y deltarpm 

#====install unzip============================//   
RUN yum install -y unzip 

WORKDIR /usr/app/low_voltage_packages/

#===rpm and zip packages (provided by Pierre) are in driver directory====//
#COPY low_voltage/driver . 
COPY driver ./ 

##===install the rsvisa-centos_5.12.1-1.x86_64.rpm package==============//
RUN rpm -ivh --nodeps rsvisa-centos_5.12.1-1.x86_64.rpm

#unzip  ni-software
RUN unzip NILinux2019DeviceDrivers.zip

#==Install ni-software-2019-19.2.0.49152-0 + f0.el7.noarch.rpm : which configures NI repositories on Centos==//
RUN rpm -ivh --nodeps ni-software-2019-19.2.0.49152-0+f0.el7.noarch.rpm 

#===install the libivivisa0 ni-icp.noarch ni-visa ni-daqmx kernel-devel packages====//
RUN yum install -y libusb 
RUN yum install -y libivivisa0
RUN yum install -y ni-icp.noarch
RUN yum install -y ni-visa
RUN yum install -y ni-daqmx
RUN yum install -y kernel-devel

COPY ../requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
#COPY low_voltage/hmp.py .
COPY hmp.py ./

