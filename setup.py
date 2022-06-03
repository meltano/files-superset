from setuptools import setup, find_packages

setup(
    name="files-superset",
    version="0.1",
    description="Meltano project files for Superset",
    packages=find_packages(),
    package_data={
        "bundle": [
            "analyze/superset/*",
        ]
    },
)
