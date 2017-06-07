# Genetics

## Preface
This repository uses [git-lfs](https://git-lfs.github.com/) to store datasets. In order to access them, you'll need to install it to your computer.  
In order to enable git-lfs:  
1. Install git-lfs package from the [official webpage](https://git-lfs.github.com/)
2. Run the config initialization command:  
```
git lfs install
```
3. Done! You should be able to access the data files on next pull

## Project dependencies
- python 3.5 minimum
- In ubuntu: python3-tk
## Pycharm Debug
* https://github.com/amnong/misc/tree/master/pycharm_runner

## Running project
First we need to initialize  the environment:
```
make install
```
There are a couple of ways to run the project.  
All configs are located inside the tp3/data/configs folder. After changing any you should `make install` before running the project.  
You can specify which config to use when running:
```
./venv/bin/tp3 --config default.json
```
Or you can run the application in report-mode that will run everything inside configs/reports/:
```
./venv/bin/tp3 --all
```

There's also help for the application:  
```
./venv/bin/tp3 --help
```
