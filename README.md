# Manufacturing Entropy

This repository contains all data related to the article titled "xxx" submitted to Manufacturing Letters. Full bibliographic information will be made available if the article is accepted.

## Path - Transfer flow Entropy for manufacturing networks

This work is based on Tutzauer's model of path-transfer flow entropy explained in his 2007 article available [here](https://www.sciencedirect.com/science/article/abs/pii/S0378873306000426).

## Application example

To demonstrate the use of path - transfer flow entropy on manufacturing networks, a network was constructed using [data from Bosch publicly availble on Kaggle](https://www.kaggle.com/c/bosch-production-line-performance). The data used for this application example is contained the `train_date.csv` file available for download from Kaggle. This data corresponds to anonymized time-stamps obtained when RFID tagged items pass by any of the 52 workstations in this manufacturing plant.

### Data processing

1. **From time stamp to manufacturing paths:** the data in `train_date.csv` is processes using `from_timestamp_to_paths.py` to obtain `data/manufacturing_paths.txt` and `data/manufacturing_edges.txt`.

   `data/manufacturing_paths.txt` contains a manufacturing path in each line as well as the count for said path. The path is a list of white space separated workstations (identified with an integer from 0 to 51) while the count is the frequency with which said path showed in the data under evaluation. Thus, the count is a natural number. In total, there are 164213 different manufacturing paths in this dataset.

   `data/manufacturing_edges.txt` is obtained by processing the manufacturing paths to obtain pair of workstations (i,j) and the frequency of the material flow from i to j. In total, there are 681 edges (accounting for dummy edges pointing from the source to a starting workstation, as well as pointing from a finishing workstation to a dummy sink).

2. **Cleaning paths and edges:** analysis of the edges saved in `data/manufacturing_edges.txt` show many edges with very low weight. These may be the result of noisy data recording. Thus, the pre-processed paths and edges saved in `data/manufacturing_paths.txt` and `data/manufacturing_edges.txt` are cleaned by identifying edges whose weight fall below a threshold (chosen as 0.1% of the total manufactured items). Then, paths that contain these edges are removed from the dataset. Finally, edges and their weight are recalculated from the clean paths dataset. This results in a paths dataset containing 95.77% of the original manufacturing paths. The clean edges dataset contains 307 edges (not considering dummy edges).

2. **From paths and edges to entropy:** a graph is built using the edges recorded in `data/manufacturing_edges.txt` and the path-transfer flow entropy as proposed by [Tutzauer in 2007](https://www.sciencedirect.com/science/article/abs/pii/S0378873306000426) is calculated with one simple, yet major change. Instead of searching for all paths in the graph, which is computationally prohibitive, only real manufacturing paths as obtained from time stamp data are used to calculate the entropy of each node (workstation). The results are saved to `results/manufacturing_entropy.txt`.
