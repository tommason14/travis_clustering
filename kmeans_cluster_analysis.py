#!/usr/bin/env python3
import os
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
import seaborn as sns

def fit_clusters(df, n = 10):
    """
    Classifies clusters based on the KMeans algorithm.
    """
    km = KMeans(n_clusters = n)
    rmsd = df['rmsd'].values.reshape(-1,1) # All sklearn algorithms require 2D arrays
    km.fit(rmsd)

    clusters = km.predict(rmsd) 
    # by predicting the clusters of the original data,
    # this gives the group each RMSD value is placed in
    df['cluster_id'] = clusters

    # cluster-12.xyz -> 12, for plotting
    df['cluster1'] = df['cluster1'].str.extract(r'cluster-([0-9]+).xyz').astype(int)
    df['cluster2'] = df['cluster2'].str.extract(r'cluster-([0-9]+).xyz').astype(int)
    return df, km

def plot_heatmap(df, output = 'plots/heatmap.png'):
    """
    Plot heatmap where the x and y axis are numerical descriptors of each xyz file,
    and the colours represent the different clusters each RMSD value is grouped into.
    """
    piv = df.pivot('cluster1', 'cluster2', 'cluster_id')
    plot = sns.heatmap(piv)
    # to rotate, need to access the underlying api, so will set the label here as well,
    plot.collections[0].colorbar.ax.set_ylabel('KMeans cluster ID', rotation=-90, va='bottom')
    # x axis labels are squashed together, so take every fourth value
    plot.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    plot.xaxis.set_major_locator(ticker.MultipleLocator(base=4))
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.xlabel('Cluster 1')
    plt.ylabel('Cluster 2')
    plt.savefig(output, dpi=300)
    plt.clf()

def plot_centroids(km, output = 'plots/centroids.png'):
    """
    Takes in the KMeans instance after the clustering has been performed.
    """
    centroids = km.cluster_centers_
    colours = cm.get_cmap('Dark2')
    for n, yval in enumerate(centroids):
        plt.plot(1, yval, color = colours(n), marker='x', markersize=10)
    plt.xticks([])
    plt.title('Centroids')
    plt.ylabel('RMSD')
    plt.savefig(output, dpi=300)
    plt.clf()

def find_most_prominent_cluster(df, output='csv_files/kmeans_assignments.csv'):
    """
    For each xyz in cluster1, sum up the number of times that each xyz file in cluster2
    is assigned to each cluster ID. Each xyz then has a cluster ID assigned to it, which is
    written to a csv
    """
    counts = df.groupby('cluster1')['cluster_id'].value_counts().reset_index(name='counts')
    idx = counts.groupby('cluster1')['counts'].idxmax()
    most_prominent_kmeans_id = counts.loc[idx]
    prominent = most_prominent_kmeans_id[['cluster1','cluster_id']]
    prominent.columns = ['xyz','kmeans_cluster']
    prominent.to_csv(output, index=False)

def main():
    sns.set(style='whitegrid', font='Ubuntu') # also controls matplotlib style
    df = pd.read_csv('csv_files/rmsd.csv')
    clustered, kmeans = fit_clusters(df)
    clustered.to_csv('csv_files/clustering_results.csv', index=False)
    find_most_prominent_cluster(clustered)
    plot_centroids(kmeans)
    plot_heatmap(clustered)

if __name__ == "__main__":
    main()
