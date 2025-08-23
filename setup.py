import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pycwmanage',
    version='0.1.0',
    author='CaeNeb, LLC',
    author_email='marcus@marcusbevans.com',
    description='Python client library for ConnectWise Manage REST API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/marcusbevans/pycwmanage',
    project_urls={
        "Bug Tracker": "https://github.com/marcusbevans/pycwmanage/issues",
        "Documentation": "https://github.com/marcusbevans/pycwmanage#readme",
        "Source Code": "https://github.com/marcusbevans/pycwmanage"
    },
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests>=2.25.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'python-dotenv>=0.19.0',
            'pytest-cov>=2.0',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
    ],
    keywords='connectwise manage api client rest',
)
