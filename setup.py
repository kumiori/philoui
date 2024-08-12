from setuptools import setup, find_packages

setup(
    name='philoui',
    version='0.1',
    packages=find_packages(),
     include_package_data=True,
    install_requires=[
        # List dependencies here
        'streamlit',
        # other dependencies
    ],
    # metadata
    author='Andrés A León Baldelli',
    author_email='leon.baldelli@cnrs.fr',
    description='A library of interactive interfaces for streamlit.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kumiori3/philoui',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)