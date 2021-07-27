from setuptools import setup
import torch
import setuptools
import os

with open('requirements.txt') as f:
    reqs = f.read().split('\n')

if torch.cuda.is_available():
    reqs = [req for req in reqs if 'torch' not in req]
    reqs += ['torch==1.9.0+cu111', 'torchvision==0.10.0+cu111', 'torchaudio==0.9.0']

setup(
    name='common',
    version='1.0',
    packages=['tests', 'common'],
    install_requires=reqs,
    url='',
    license='',
    author='ohad',
    author_email='ogdoron@gmail.com',
    description='Common Utilities'
)
