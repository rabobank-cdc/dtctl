# dtctl

A Darktrace CLI written in Python for interacting with the Darktrace API.

## Getting Started

```python >= 3.7``` is required to run dtctl.

To get started quickly with the Darktrace cli, do the following:

```
python setup.py install
dtctl config set secure-dtkey
dtctl --host <host> --pub-dtkey <public Darktrace key> system info
```

Alternatively, configure the host, public key and a custom certificate using `dtctl config set`

```dtctl``` outputs information in JSON because it is both human readable and machine parsable. If you prefer a
different output format, you are welcome to submit a pull request.

### Prerequisites

For fully using dtctl including running tests ensure the following packages are installed:

```
click
requests
openpyxl
pandas
netaddr
pycryptodomex
dictdiffer
pytest
prospector
requests-mock
```

### Installing

Installation is straight forward and can be done using easy-install
```
python setup.py install
```

If you want to install the development environment

```
python setup.py develop
```

and just run

```
dtctl 
```

## Docker
A Dockerfile is made available for getting started with dtctl. If you want to make use of a
configuration file, make sure you mount a volume.

First build

```
docker build . -t dtctl
```

Than run

```
docker run -v $HOME/.dtctl:/root/.dtctl dtctl --help
```


## Development
Development follows the Gitflow Workflow but without the use of the Gitflow extension.
For background information check 
[Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) 

In short:
1. Commit your changes in the ```develop``` branch
2. Build features in feature branches (i.e. ```feature_branch```)
3. Merge feature branches into the ```develop``` branch
4. Run tests and linting
5. Merge the ```develop``` branch into the ```master``` branch when production ready
6. Tag the ```master``` branch for each release

## Running the tests

Test coverage is limited and tests mainly focus on CLI interface. Tests can be run by doing

```
python -m pytest tests/
```

When developing make sure you also perform manual testing to ensure correct workings of dtctl

### Coding style

Code style conventions mostly follow Python Style Guide (PEP 8) except for line lengths, 
and number of arguments and variables. Checks are done with prospector and pylint.

```
prospector -W pylint
```

We run pylint separately

```
pylint --max-line-length=120 --disable=too-many-arguments --disable=too-many-locals --disable=duplicate-code dtctl
```

* too-many-arguments - Disabled due to click options requiring numerous function arguments
* too-many-locals - Disabled due to reasons
* duplicate-code - Disabled because pylint marks re-used Click arguments and options

## Built With

* [Click](https://click.palletsprojects.com/en/7.x/) - The "Command Line Interface Creation Kit"

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors
* **Connor Dillon** - *Initial work* - [Connor](https://github.com/connordillon)
* **Daan Wagenaar** - *Creation of CLI* - [Daanwa](https://github.com/daanwa)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks for the Rabobank CDC team for support
* Heavily inspired by `git` cli
