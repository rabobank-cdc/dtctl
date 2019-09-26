from setuptools import setup, find_packages

setup(
    # mandatory
    name='dtctl',
    # mandatory
    version='0.2.8',
    # mandatory
    author_email='daan@vynder.io',
    packages=find_packages(),
    package_data={},
    install_requires=['click', 'requests', 'openpyxl', 'pandas', 'netaddr', 'pycryptodomex', 'dictdiffer'],
    entry_points={
        'console_scripts': ['dtctl = dtctl.cli:cli']
    }
)
