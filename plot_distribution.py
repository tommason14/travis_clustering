#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='whitegrid', font='Ubuntu')
df = pd.read_csv('csv_files/rmsd.csv')
sns.distplot(df['rmsd'], color='#348595')
plt.xlabel('RMSD')
plt.ylabel('Occurrence')
plt.savefig('plots/rmsd_distribution.png', dpi=300)
