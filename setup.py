from setuptools import setup
import torch
import setuptools
import os

with open('requirements.txt') as f:
    reqs = f.read().split('\n')

if torch.cuda.is_available():
    reqs = [req for req in reqs if 'torch' not in req]
    reqs += ['torch==1.9.0+cu111', 'torchvision==0.10.0+cu111', 'torchaudio==0.9.0']
else:
    reqs += ['torch', 'torchvision', 'torchaudio']

setup(
    name='common',
    version='1.0',
    packages=['tests', 'common'],
    install_requires=['loguru==0.5.3', 'mongoengine==0.23.1', 'mongomock==3.23.0', 'numpy==1.21.1', 'Pillow==8.3.1',
                      'pymongo==3.12.0', 'pytest==6.2.4', 'toml==0.10.2', 'torch==1.9.0', 'torchvision==0.10.0',
                      'trains==0.16.4', 'pytorch-lightning', 'simpleitk', 'lightning-bolts'],
    url='',
    license='',
    author='ohad',
    author_email='ogdoron@gmail.com',
    description='Common Utilities'
)
