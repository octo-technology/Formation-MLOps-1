# Training MLOps 1

This is a practical work to illustrate Data Science industrialization. It is part of a training provided
by Octo Academy, more
details [here](https://www.octo.academy/catalogue/formation/dsind-mlops-industrialisation-dun-projet-de-data-science/)

## How do I install it

### 1. Get project

First, clone the project from GitLab : (if you are on Windows you will
need [Git for windows](https://gitforwindows.org/) and do git command in Git Bash)

```sh
git clone git@github.com:octo-technology/Formation-MLOps-1.git
```

### 2. Open it in pycharm and configure pycharm

Second, open project in Pycharm.

If on Windows, configure your terminal in Pycharm so that you can run all commands :

- Go to Settings > Tools > Terminal
- Change “Shell path” by : `cmd.exe  "/K"  "C:\Users\>>me<<\Miniconda3\Scripts\activate.bat"`
- Restart Pycharm
- Test it by typing `git` in terminal

### 3. Create an env

Third, make sure you have miniconda or anaconda installed. If not, install it!

Change directory into the repo you cloned

```sh
cd Formation-MLOps-1
```

Create a conda env

```sh
conda create -n formation_mlops_1 python=3.10
```

Activate your env

```sh
conda activate formation_mlops_1
```

Install all needed dependencies

```sh
pip install -r requirements.txt
```

Start a jupyter notebook in the folder

```sh
jupyter-notebook
```

If your `formation_mlops_1` environment is not available in `jupyter` interface (when clicking on new). You should :

- Quit jupyter-notebook with <kbd>ctrl</kbd>+<kbd>c</kbd> in terminal
- Run `conda install -n formation_mlops_1 nb_conda_kernels`
- Start `jupyter-notebook`

## How to follow it

It is highly linked to the presentation of the formation.

To navigate between steps change branch.

To see all branches

```sh
git branch -a
```

To start the practical work you should check out branch `0_initial_state`

```sh
git checkout 0_initial_state
```