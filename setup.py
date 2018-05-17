from setuptools import setup, find_packages

setup(
    name="pandas_xyz_pif_ingester",
    version="0.1",
    author="Lawrence Crosby",
    author_email="crosbyla@u.northwestern.edu",
    description="Python module for parsing GDB-9 XYZ files using Pandas library",
    # packages=['pandas_ingester'],
    packages=find_packages(),
    install_requires=[
        "pypif",
        "pandas>=0.20",
        "",
    ],
    tests_require=[
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'pandas-ingester=pandas_ingester.pandas_ingester:parse_cli',
        ]
    },
)
