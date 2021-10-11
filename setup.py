from setuptools import find_packages, setup

setup(
    name='trackerdcs',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'influxdb-client',
        'paho-mqtt',
        'pyserial',
    ],
)