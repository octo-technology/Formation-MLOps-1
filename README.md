# Create unit tests (4)

![branch build status](https://github.com/octo-technology/Formation-MLOps-1/actions/workflows/ci.yml/badge.svg?branch=4_create_unit_tests)

What is this?
-------------
At this step :
- Your notebook is clean and running
- You have a few documented functions
- Your functions are in a specific `.py` file
- Your functions are tested


Installation
-------------------
Install the required package in the proper environment.

```shell
pip install sphinx==6.1.3
```

Initiate your documentation by running the following commands.
```shell
mkdir ./docs
cd docs
sphinx-quickstart
```

What is the goal ?
-------------------
The goal at this step is to generate a sphinx documentation.

Following instructor demonstration you will create a documentation using
`sphinx`. The result will be some `html` pages.


Installation
-------------------
Install the required package in the proper environment.

```shell
pip install -r requirements_test.txt
```

Initiate your documentation by running the following commands.
```shell
mkdir ./docs
cd docs
sphinx-quickstart
```


When I'm done ?
---------------
When you are done, please wait for the rest of the group.

For the next step of the practical work, you can either
keep on working on the code as it is, or checkout branch `5_add_sphinx_doc`

To check out branch `5_add_sphinx_doc` you need to either commit
or stash your changes :
```
git stash
git checkout 5_add_sphinx_doc
```