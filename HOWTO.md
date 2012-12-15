## How to Build committer Yourself

### Fork the Git repository

Simply [fork](https://github.com/aelgru/committer/fork_select) committer.

### Create a [virtual environment](http://www.virtualenv.org/)

To build committer you will have to install dependencies.
This would normally affect your system.
Instead of installing those dependencies into your system we will install them into a virtual environment.

```bash
virtualenv venv
```

### Activate the virtual environment

```bash
source venv/bin/activate
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

Before installing committer, please leave the virtual environment by executing:

```bash
deactivate
```

Within the `target/dist` dir you will find the built artefacts.

Once you changed into the `target/dist/committer-x.x.x` directory you can install committer:

```bash
sudo python setup.py install
```

