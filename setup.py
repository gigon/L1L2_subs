from setuptools import setup, find_packages
setup(
    name="L1L2_subs",
    version="1.0",
    packages=find_packages(),

   package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.json"],
    },    
)