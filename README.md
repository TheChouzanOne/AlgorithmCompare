# AlgorithmCompare

> Note: this only works for windows systems

This project was developed to illustrate the difference between DFS, BFS and A* algorithms, by allowing the user to create a maze in a grid and observe how every algorithm behaves in order to find its objective.

If you want to run this project I recommend creating a virtual environment for it. You can also just install the required Python 3 dependencies but the first option is probably better.

First you will need to install Python 3.8 (probably any Python 3 version works, but only this one has been tested) and `venv` package via pip:

`python -m pip install virtualenv`

Then, on the root directory of this repo create your virtual environment:

`python -m venv .`

and activate it using the following scripts depending on your shell:

|Shell       | Command                 |
|------------|-------------------------|
| Powershell | `Scripts/Activate.ps1`    |
| CMD        | `Scripts/activate.bat`    |

To finish configuration, install the required dependencies with pip by running

`pip install -r dependencies.txt`

and run the project:

`python src/main.py`

Remember, every time you want to run this project you will need to activate the virtual environment.