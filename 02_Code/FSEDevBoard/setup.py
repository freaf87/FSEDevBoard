from distutils.core import setup

setup(
    name='FseDevBoard',
    version='0.0.1',
    author='Frederic Afadjigla',
    author_email='freddy1187@gmail.com',
    packages=['FseDevBoard'],
    url='https://fullstackembedded.com',
    license='LICENSE.txt',
    description='Drivers for FSEDevBoard used in FSE workshops.',
    long_description=open('README.txt').read(),
    install_requires=[
        "smbus2",
        "wiringpi",
        "spidev",
    ],
)

