# Predict notebook (8)

![branch build status](https://github.com/octo-technology/Formation-MLOps-1/actions/workflows/ci.yml/badge.svg?branch=8_predict_notebook)

What is this?
-------------

This the correction of practical work for Data Science Industrialization.

In this branch you will find :
- A clean and running notebook
- A few documented and tested functions
- Some `sphinx` documentation
- A `setup.py`
- A predict notebook that reload model and make predictions.

How to run the docker container ?
---------------------------------

```
docker build -t mlops-1 .
docker run -p 80:80 mlops-1
```

The API is exposed and can be reached at 0.0.0.0:80
The doc is available [here](http://127.0.0.1/docs)

[Call example](http://127.0.0.1/predict/2/Nasser,%20Mrs.%20Nicholas%20(Adele%20Achem)/female/?&age=14.0&sibSp=1&parch=0&ticket=237736&fare=30.0708&embarked=C) that should return the following message:
```
input_proba:
0	0.1997672537546488
1	0.8002327462453511
```

How to restart ?
----------------

To start this practical work from the beginning you should :
```
git stash
git checkout master
```


How to run tests ?
------------------

Test are written in bats, to install it on your computer :

For MacOS:
```
brew install bats
```

For Fedora:
```
dnf install bats
```

For Ubuntu:
```
sudo add-apt-repository ppa:duggan/bats
sudo apt-get update
sudo apt-get install bats
```

for other systems, look at the documentation [here](https://github.com/sstephenson/bats/wiki/Install-Bats-Using-a-Package)

To run tests, activate the conda environement and run the bats command on the test file :

```
conda activate python_indus && bats test.bats
```


