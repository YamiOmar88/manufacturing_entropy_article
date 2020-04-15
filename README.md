# Manufacturing Entropy

This repository contains all data related to the article titled "xxx" submitted to Manufacturing Letters. Full bibliographic information will be made available if the article is accepted.

## Path - Transfer flow Entropy for manufacturing networks

This work is based on Tutzauer's model of path-transfer flow entropy explained in his 2007 article available [here](https://www.sciencedirect.com/science/article/abs/pii/S0378873306000426).

## Application example

To demonstrate the use of path - transfer flow entropy on manufacturing networks, a network was constructed using [data from Bosch publicly availble on Kaggle](https://www.kaggle.com/c/bosch-production-line-performance). The data used for this application example is contained the `train_date.csv` file available for download from Kaggle. This data corresponds to anonymized time-stamps obtained when RFID tagged items pass by any of the 52 workstations in this manufacturing plant.

### Data processing

1. From time stamp to manufacturing paths: the data in `train_date.csv` is processes using `from_timestamp_to_paths.py` to obtain `data/manufacturing_paths.txt` and `data/manufacturing_edges.txt`.
