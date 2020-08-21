#!/bin/sh
mkdir plots csv_files
./split_clusters.py cluster_C5H14NO.xyz &&
./calculate_rmsd.py &&
./plot_distribution.py &&
./kmeans_cluster_analysis.py &&
echo "CSV files and plots are placed in separate subdirectories"
