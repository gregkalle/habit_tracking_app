"""
    Name
        setup
    
    Description
        Sets up the habit tracking app.
"""
from setuptools import setup, find_packages

def finding_requirements():
    """
    Returns the install_requirements to setup the habit tracking app

    Returns:
        (str): 
    """
    with open(file="requirements.txt", encoding="utf-8") as req:
        text = req.read()
        requirements = text.split("\n")
    return requirements


setup(
    name="habit tracking app",
    version="0.1",
    py_modules=["main"],
    packages=find_packages(),
    install_requires=finding_requirements(),
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        habits=main:main
    """,
)
