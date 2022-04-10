import pandas as pd
import numpy as np
from scipy import stats
import math

'''Main function'''
def main():
    df = pd.read_csv('FIFA_2018_Statistics.csv')      # read raw CSV
    print(df.shape)
    # drop all observations which aren't successful or failed
    #dropset = ['Free Kicks','1st Goal','index','Date','Saves', 'Red','Own goal Time', 'Own goals','Goals in PSO','PSO','Round', 'Yellow & Red', 'Yellow Card', 'Fouls Committed', 'Distance Covered (Kms)','Offsides','Blocked']
    #data = df.drop(dropset,axis=1)
    y = boxplot_outlier(df, 'Goal Scored')
    print(y)



    '''

    pre_process_manual(df)
    pre_process_grubbs(df)
    pre_process_original(df)'''

def boxplot_outlier(data, target):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    iqr = stats.iqr(data)#IQR(data)
    data = data[(data[target]>(Q1-1.5*iqr)) & (data[target]<(Q3+1.5*iqr))]
    return data

''' Prune and create CSV based on Hypothesis'''
def pre_process_manual(df):
    df = df[(df['goal'] <= df['goal'].std()) | ((df['goal'] >= df['goal'].std()) & (df['state'] == 1)) ].copy()
    print('manual', df.shape)
    df.to_csv('KS_manual_pre_process.csv', sep=',', index=False)


''' Grubbs-Test algorithm'''
def grubbs_test(N, df, a = 0.05): 
    p = 1-(a/(2*N))
    nn = N-2
    value = stats.t.ppf(p, nn)
    value**=2
    thresh = math.sqrt(value/(nn*value)) * (N-1)/math.sqrt(N)
    y = df['goal']
    mean = y.mean()
    std = y.std()
    term_factor_max = 0
    term_factor_min = 0
    mean_dev = abs(y-mean)
    for i in range(N):
        y_max = mean_dev.idxmax()
        y_min = mean_dev.idxmin()
        if y_max == term_factor_max and y_min == term_factor_min:
            break
        term_factor_max = y_max
        term_factor_min = y_min
        G1 = abs(mean_dev[y_min])/std
        G2 = abs(mean_dev[y_max])/std
        if G1>thresh:
            mean_dev = mean_dev[mean_dev != mean_dev[y_min]]
            df = df[y != y[y_min]]
        if G2>thresh:
            mean_dev = mean_dev[mean_dev != mean_dev[y_max]]
            df = df[y != y[y_max]]
        #print(i, thresh, G1, y_min, G2, y_max)
    #p = stats.t.cdf(value, nn)
    return df

''' Create Original CSV with clean variables'''
def pre_process_original(df):
    df.to_csv('KS_original_pre_process.csv', sep=',', index=False)


''' Prune and create CSV based on Grubbs-Test outlier detection'''
def pre_process_grubbs(df):
    df = grubbs_test(df.shape[0], df)
    df.to_csv('KS_grubb_pre_process.csv', sep=',', index=False)


''' Main entry point'''
main()