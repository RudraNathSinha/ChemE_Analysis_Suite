from setuptools import setup, find_packages

setup(
    name="cheme_analysis_suite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "numpy>=1.24.3",
        "pandas>=2.0.2",
        "opencv-python-headless>=4.7.0.72",
        "pillow>=9.5.0",
        "plotly>=5.15.0",
        "scipy>=1.10.1",
        "scikit-learn>=1.2.2"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive suite of chemical engineering analysis tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ChemE_Analysis_Suite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
