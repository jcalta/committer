## How to Build committer Yourself

### Fork the Git repository

Simply [fork](https://github.com/aelgru/committer/fork_select) committer.

### Create a virtual environment

To build committer you will have to install dependencies.
This would normally affect your system.
Instead of installing those dependencies into your system we will install them into a virtual environment.

```bash
virtualenv ve
```

### Activate the virtual environment

```bash
source ve/bin/activate
```

### Install [pybuilder](http://pybuilder.github.com/)

```bash
pip install pybuilder
```

### Install committer dependencies

```bash
pyb install_dependencies
```

This will download the dependencies using `pip`.

### Build committer

```bash
pyb
```

This will execute all unittests and check the coverage.

### Install and test the built version

Within the `target/dist` dir you will find the built artefacts.

One possibility is to change into the `target/dist/committer-0.0.70` directory.

```bash
python setup.py install
```

