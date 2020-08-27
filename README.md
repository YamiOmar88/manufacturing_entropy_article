# Manufacturing Entropy

This repository contains all data related to the article titled "Entropy of Complex Manufacturing Networks as a Metric of Flexibility" submitted to the Journal. Full bibliographic information will be made available if/when the article is accepted.

## Path - transfer flow entropy for manufacturing networks

This work is based on Tutzauer's model of path-transfer flow entropy explained in his 2007 article available [here](https://www.sciencedirect.com/science/article/abs/pii/S0378873306000426).

## Application example

To demonstrate the use of path - transfer flow entropy on manufacturing networks, a network was constructed using [data from Bosch publicly availble on Kaggle](https://www.kaggle.com/c/bosch-production-line-performance). The data used for this application example is contained the `train_date.csv` file available for download from Kaggle. This data corresponds to anonymized time-stamps obtained as in-process goods pass by any of the 52 workstations in this manufacturing plant.

### Data processing

1. **From time stamp to manufacturing paths:** the data in `train_date.csv` is processes using `from_timestamp_to_paths.py` to obtain `data/manufacturing_paths.txt` and `data/manufacturing_edges.txt`.

   `data/manufacturing_paths.txt` contains a manufacturing path in each line as well as the count for said path. The path is a list of white space separated workstations (identified with an integer from 0 to 51) while the count is the frequency with which said path showed in the data under evaluation. Thus, the count is a natural number. In total, there are 164213 different manufacturing paths in this dataset.

   `data/manufacturing_edges.txt` is obtained by processing the manufacturing paths to obtain pair of workstations (i,j) and the frequency of the material flow from i to j. In total, there are 681 edges (accounting for dummy edges pointing from the source to a starting workstation, as well as pointing from a finishing workstation to a dummy sink).

2. **Cleaning paths and edges:** analysis of the edges saved in `data/manufacturing_edges.txt` show many edges with very low weight. These may be the result of noisy data recording. Thus, the pre-processed paths and edges saved in `data/manufacturing_paths.txt` and `data/manufacturing_edges.txt` are cleaned by identifying edges whose weight fall below a threshold (chosen as 0.1% of the total manufactured items). Then, paths that contain these edges are removed from the dataset. Finally, edges and their weight are recalculated from the clean paths dataset. This results in a paths dataset containing 95.77% of the original manufacturing paths. The clean edges dataset contains 307 edges (not considering dummy edges). The clean datasets are saved as `data/clean_manufacturing_paths.txt` and `data/clean_manufacturing_edges.txt`.

3. **From clean paths and edges to path probabilities and entropy:** two approaches are analyzed:

  * **Binary, directed graph with self-loops on all nodes:** a binary, directed graph is constructed from the data in `data/clean_manufacturing_edges.txt`. Self-loops are added on all nodes. The path probability `p_ij` for all `i` and `j` is calculated. The necessary code is contained in `binary_pij.py`. Given the computational heaviness of this code, it was run in the University of Luxembourg HPC.

  * **Weighted, directed graph with self-loops on end nodes only:** a weighted, directed graph with self-loops on end nodes only is constructed as explained in the Methods section of the article. The path probability `p_ij` for all `i` and `j` is calculated. The necessary code is contained in `weighted_pij.py`. Given the computational heaviness of this code, it was run in the University of Luxembourg HPC.

### Heatmaps plotting

In order to plot the `p_ij` heatmaps, the `plot_heatmap.py` file must be run. This calls the `heatmap.py` module.
