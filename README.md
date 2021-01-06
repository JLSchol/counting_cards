# Readme file

Counting cards for blackjack

### content
This workspace contains:
1. README.md 
2. requirements.txt (list of package required to run software)
3. BlackJackGame.py (play the game, can be used to test other classes)
3. CountCards.py (class that is enables counting cards)
4. RecordScreen.py (class that records screen)
5. DetectCards.py (class that detect the cards)
6. DetectGameState.py (class that detect state of the game)
7. DetectPlayers.py (class that detects players dealers and their corresponding hand)
5. Main.py





### Installation instruction
0. prerequisites
1. Clone repositiory
2. install requirements
3. run programm

#### 0. prerequisites
Used on windows 10
Before startign you should have installed:
python 3.8
pip3 (packet manager for python 3)
git (used to clone repository, additionally other commands are given in git bash)
virualenv (optional)

Should have installed git as the commands are exicuted in their git bash terminal



#### 1. Clone repository
Create a copy of the repository by cloning it in your local machine or by downloading the zip file.
To clone, navigate to the directory where you want to clone the repositor and open your git bash terminal
```bash
git clone https://github.com/JLSchol/counting_cards.git
```

#### 2. install requiremnets (dependencies/packages)
After having succesfully cloned the repository, install the dependent packages.

optional steps using a virtual environment:
Sometimes, python packages can not be installed side by side your existing packages (e.g. different versions)
To make sure that the installed packages do not conflict with the packages your have currently installed on your machine, use a virtual environmnet.
To install in a virutal environment (use:
```bash 
	pip install virtualenv
```
) 
navigate to the top of your project directory and create the virtual environment.
```bash
virtualenv venv -p python3.8
```
activate: (windows 10 using git bash)
```bash
source venv/Scripts/activate
```
Now you venv is active and you can install the packages while this is active. You should see (venv) in your git bash
To deactivate type:
```bash
deactivate
```

make sure pip is up to date (also in venv)
```bash
python -m pip install --upgrade pip
```

Install the dependent python modules using the requirements.txt file:
```bash
pip3 install -r requirements.txt
```

Check if version correspond with requirements (should have similar packages as specified in requirments file):
```bash
pip list
```

write added packages to requirements.txt file
```bash
pip freeze > requirements.txt
```

#### 3. install requiremnets (dependencies/packages)