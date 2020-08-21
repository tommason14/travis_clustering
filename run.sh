#!/bin/sh
mkdir -p data plots 
./split_clusters.py cluster_C5H14NO.xyz &&
./calculate_rmsd.py &&
./plot_distribution.py &&
./kmeans_cluster_analysis.py &&
./pick_selection_of_clusters.py 
