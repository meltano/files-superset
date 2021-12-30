from setuptools import setup, find_packages

setup(
    name="files-superset",
    version="0.1",
    description="Meltano project files for Superset",
    packages=find_packages(),
    package_data={
        "bundle": [
            "analyze/superset/README.md",
            "analyze/superset/*",
            "analyze/superset/docker/*",
            "analyze/superset/docker/.env",
            "analyze/superset/docker/pythonpath_dev/*",
            "analyze/superset/assets/*/.*",
        ]
    },
)
