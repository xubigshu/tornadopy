from setuptools import setup, find_packages
import tornadopy

setup(
    name="tornadopy",
    version=tornadopy.__version__,
    description="tornadopy based on tornado",
    long_description="tornadopy is based on tornado,django like web framework.",
    keywords='python tornadopy django tornado',
    author="xubigshu",
    url="https://github.com/xubigshu/tornadopy",
    license="BSD",
    packages=find_packages(),
    package_data={'tornadopy': ['resource/exception.html']},
    author_email="xubigshu@gmail.com",
    requires=['tornado', 'futures'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    scripts=[],
    install_requires=[
        'futures',
    ],
)
