# truckload
Evolutionary algorithm trying to find the best way to fulfill assignments with trucks. 

## maintainers
* 5320806
* 1980527

## run it
You need  python ~3.9 with numpy and deap.

Change in the directory of the `main.py` and run `python main.py`!



## config
A config file named `truckload.config` placed in the root directory of the project is required, edit the existing one to your favors. 
It has to have the following content: 
```
[probabilities]
p_mutate = 0.001
p_crossover = 0.8

[population]
initial_population_size = 100
generations = 100
keep = 0.8
new_random = 0.2
hall_of_fame = 3

[files]
truck_file = ../data/Evo11/Evo11_LKW.csv
assignment_file = ../data/Evo11/Evo11_Auftraege.csv
```