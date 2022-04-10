## Abstract

Data pruning is the process of eliminating certain suboptimal data from the dataset, to observe an improvement in the learning performance. In this paper, we propose the idea of pruning data by eliminating outliers and testing multiple datasets. During our analysis, comparison of various machine learning algorithms was performed on 3 different datasets using both unpruned and pruned versions of each using our pruning hypothesis. The objective was to understand whether the performance of the algorithms varied when the unpruned and the pruned datasets were used and observe if pruning made a difference in the results. We used various classification algorithms, to observe the effect of data pruning on the accuracy of these classifiers.

## Introduction

An important question to be addressed in training a model would be, whether a training example can have adverse effects on learning. The belief that more data results in better prediction can be contradicted by showing that the quality of the examples also matter. This is where data pruning steps in, wherein some data is strategically eliminated to improve generalization performance. Before we run the dataset for learning to determine the accuracy, we need to perform Data Cleaning, which is followed by Data Pruning. The two are fundamentally similar with very minute differences. Data Cleaning is the process of removing inaccurate, irrelevant records or Null Values (records which do not contribute to the dataset); whereas removal of data in Pruning follows a certain criteria defined by the user or some statistical method.


## Related Work
Data Pruning consists of learning diverse classifiers by randomizing the training set and then combining their output to decide on difficult examples[1]

The RANSAC method has been most common in identifying outliers[2]. RANSAC stands for Random Sample Consensus. It is used to obtain to obtain robust models with a certain probability when the noise in the data doesn't obey the general noise assumption. It follows the following principle: Create a large number of trials, extracting small sets of examples (sufficient to estimate the model), hoping that there will be at least one clean sample to produce a good model.

Using the Google Play Store Database[3], a prediction analysis of the ratings of the application on basis of the regression algorithms’ Mean Squared Error and Mean Absolute Error. Random Forest Regression presents the best outcome with least Mean Squared Error of 0.24 and least Mean Absolute Error of 0.32. Fifa 2018 Man of the Match prediction was also carried out in 2018[4], however the results were not definite due to lack of conclusion.

## Methodology

### Dataset
To answer the research question, we have chosen three datasets from Kaggle.com. Two of the datasets are partially related, being the Android Play-Store and Apple App-Store. We use regression methods to predict the User Ratings and the third dataset is a Kaggle challenge to predict whether a team in Fifa World Cup 2018 would have a man of the match.

The PlayStore data contains 10840 app data with 13 features. The App-Store data contains 7198 app data with 17 features, both with ratings in the range of 1-5. The Fifa data is an experiment with a very small dataset containing 128 observations, with 27 features. Fig.2 

### Pre-Processing

The PlayStore dataset contains few variables with missing values in the ​Rating​(User Ratings), Current Ver​(Current Version of app), ​Android Ver​(Compatible version of Android) and ​Type​(Free or Paid app). The Android Version and Current Version of app were dropped assuming they don't contribute much to the user ratings. Type had a missing value as one of the entries was corrupt, which was removed. The Rating variable had a significant amount of missing values, which were filled with the median value of all the applications of same ​Genre​. The App-Store dataset on the other hand didn't have any missing values. The categorical data were converted to numeric form using LabelEncoder of the scikit-learn library.

In the Fifa dataset, the NaN values correspond to an event not occuring, hence it was labeled as ‘-1’. We plot the correlation matrix to look for possible relationships between the variables and eliminate the least related variables to the Man of the Match​ feature to clean the dataset. ​Fig 5

### Data Pruning

On observing the variables of PlayStore used for training the model ​Fig 3​, we see a high correlation between the reviews an app has received vs the number of installs. This is also mostly due to co-dependence. We use this fact to detect and prune outliers using Grubbs test[5] and Interquartile Range[6] as we do not consider ratings from Outlier Reviews. Since the App-Store doesn’t share number of installs, we assume a similar relationship between rating_count_tot​(Total Reviews of an app) and its install from the Play-Store Correlation and accordingly prune the dataset using the same method. Unlike in Play-Store dataset, we see a stronger correlation between user_rating​(app user rating) and ​rating_count_tot​. ​Fig 4

The Fifa dataset being a small classification problem with multiple correlations, we prune the dataset with respect to all the variables selected for training the model. ​Fig 5-c​. We opt for the same outlier detection method used earlier to prune the dataset.

### Algorithms

The Play-Store and App-Store datasets being a regression problems, we have used Linear-Regression ​LR​, Support Vector regression (SVR), K-Neighbors Regressor (KNR) and Random Forest Regressor (RFR) to evaluate the learning performance on data pruning. We have used K-Fold Cross Validation with the value of K as 10 and taken the average of the 10 Folds as the final value for evaluation.

The Fifa dataset uses 9 classification algorithms. We have trained Support-Vector-Cosine ​SVC​, Multi-Layer-Perceptron MLP​, Logistic-Regression ​LGR​, K-Nearest-Neighbours KNN​, Random-Forest ​RF​, Decision-Tree ​DT​, AdaBoost ​AB and Bagging-Classifier ​BC​, XGBoost ​GBM.

## Results and Discussion

We have taken into consideration Grubbs’ Test and Box Test on the Attempts parameter of the Fifa 18 Dataset which results in ​AdaBoost ​performing higher than the other algorithms in both. Logistic Regression in Box Test performs much better than in Grubb’s Test. This is seen in XGBoost, Bagging Classifier and Decision Tree as well. ​

Graphing ​Grubbs and Box Test on Goals Scored Variable results in an upward rise in Decision Tree and Logistic Regression Classifiers. 

Performing Decision Tree Classification on Pass Accuracy variable shows the best case scenario with a 100 % accuracy. Plotting it with a Decision Tree Classification Visualization with Graphviz confirms the results. 

Decision Tree Classification Visualization in Appendix demonstrates 100 percent match on comparison with the original Dataset and the result variable, ​Man of the Match​.  
Due to the noticeable increase in accuracy, on both the regression and Classification problem, we can conclude that pruning the dataset did improve the algorithms performance.


## Limitations and Outlook
An outlier is a very subjective term, as it depends on the analyst to determine what the anomaly is in a dataset. Likewise, in the process of Data Pruning, it is very difficult to determine which is a difficult example which needs to be removed to enhance the performance of a learning algorithm. It will always depend on some assumption making it susceptible to an erroneous elimination.

## Acknowledgements

This analysis was conducted as part of the 2018/19 Machine Learning module CS7CS4/CS4404 at Trinity College Dublin.

## References

[1] A. Angelova, "Data pruning", CalTech, 2004. [Online]. Available: https://thesis.library.caltech.edu/2184/1/DataPruning.pdf. [Accessed: 18- Dec- 2018].
    
[2] O. Sonmez, Math-info.univ-paris5.fr, 2006. [Online]. Available: http://www.math-info.univ-paris5.fr/~lomn/Cours/CV/SeqVideo/Material/R ANSAC-tutorial.pdf. [Accessed: 18- Dec- 2018].
 
 [3] J. Emseow, "Machine Learning to predict app ratings | Kaggle", Kaggle.com, 2018. [Online]. Available: https://www.kaggle.com/jemseow/machine-learning-to-predict-app-rating s. [Accessed: 18- Dec- 2018].
    
[4] R. Sah, "FIFA 2018 Man of the Match Prediction", www.kaggle.com, [Online]. Available: https://www.kaggle.com/ragnisah/eda-fifa2018-man-of-the-match-predicti on. [Accessed: 18- Dec- 2018].

[5] LLC, NCSS. “Grubbs’ Outlier Test .” Www.ncss.com, www.ncss.com/wp- content/themes/ncss/pdf/Procedures/NCSS/Grubbs_Outlier_Test.pdf.
    
[6] StatisticsHowTo (2018). ​Interquartile Range (IQR): What it is and How to Find it - Statistics How To​. [online] Statistics How To. Available at: https://www.statisticshowto.datasciencecentral.com/probability-and-statis tics/interquartile-range/ [Accessed 18 Dec. 2018]. 

## Appendix
![​Fig 1: Flowchart of the working of Data Pruning and retrieval of accuracy](Fig%201%20-%20Flowchart%20of%20the%20working%20of%20Data%20Pruning%20and%20retrieval%20of%20accuracy.png)

![Fig 3 - Dataset Description with missing Percentage (NaN)](Fig%203%20-%20Dataset%20Description%20with%20missing%20Percentage%20(NaN).png)
![Fig 5: Correlation of Fifa World Cup 2018 features ](Fig%205%20-%20Correlation%20of%20Fifa%20World%20Cup%202018%20features.jpg)
