from setuptools import setup, find_packages

setup(
    # mandatory
    name='dtctl',
    # mandatory
    version='0.5.0',
    # mandatory
    author_email='daan@vynder.io',
    packages=find_packages(),
    package_data={},
    install_requires=['click', 'requests', 'openpyxl', 'pandas', 'numpy', 'netaddr', 'pycryptodomex', 'dictdiffer'],
    entry_points={
        'console_scripts': ['dtctl = dtctl.cli:cli']
    }
)
