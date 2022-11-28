################################################ ###
# Comparison of AB Test and Conversion of Bidding Methods
################################################ ###

################################################ ###
# Business Problem
################################################ ###

# Facebook recently introduced a new bidding type, "average bidding", as an alternative to the existing bidding type
# called "maximumbidding". One of our customers, bombabomba.com, decided to test this new feature and would like to
# do an A/B test to see if averagebidding converts more than maximumbidding. It is waiting for you to
# analyze the results of the A/B test. The ultimate success criterion for Bombambomba.com is Purchase.
# Therefore, the focus should be on the Purchase metric for statistical testing.


################################################ ###
# Dataset Story
################################################ ###

# In this data set, which includes the website information of a company, there is information such as the number of advertisements
# that users see and click, as well as earnings information from here. There are two separate data sets, the Control and Test group.
# These datasets are on separate pages of ab_testing.xlsx excel. Maximum Bidding was applied to the control group and
# AverageBidding was applied to the test group.

# impression: Ad views count
# Click: Number of clicks on the displayed ad
# Purchase: The number of products purchased after the ads clicked
# Earning: Earnings after purchased products

################################################ ###
# Project Tasks
################################################ ###

################################################ ###
# Task 1: Preparing and Analyzing Data
################################################ ###

# Step 1: Read the dataset ab_testing_data.xlsx consisting of control and test group data. Assign control and test group data to separate variables.

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("datasets/ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("datasets/ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Step 2: Analyze control and test group data.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# Step 3: After the analysis process, combine the control and test group data using the concat method.

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()





################################################ ###
# Task 2: Define A/B Test Hypothesis
################################################ ###

# Step 1: Define the hypothesis.

# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and test group.)


# Step 2: Analyze the purchase (gain) averages for the control and test group

df.groupby("group").agg({"Purchase": "mean"})



################################################ ###
# TASK 3: Performing Hypothesis Testing
################################################ ###

# Step 1: Check the assumptions before testing the hypothesis. These are Assumption of Normality and Homogeneity of Variance.

# Test separately whether the control and test groups comply with the normality assumption via the Purchase variable.
# Normality Assumption :
# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption not provided
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED
# Is the assumption of normality according to the test result provided for the control and test groups?
# Interpret the p-values obtained.


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO cannot be denied. The values of the control group provide the assumption of normal distribution.


# Variance Homogeneity :
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
# Is the assumption of normality provided according to the test result? Interpret the p-values obtained.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO cannot be denied. The values of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are Homogeneous.

# Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results

# Since assumptions are provided, independent two-sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no mean difference between the control group and test group purchase mean.)
# H1: M1 != M2 (There is a mean difference between the control group and test group purchase mean)
# p<0.05 HO RED , p>0.05 HO CANNOT BE REJECTED

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Step 3: Purchasing control and test groups, taking into account the p_value obtained as a result of the test
Comment if there is a statistically significant difference between the # means.

# p-value=0.3493
# HO cannot be denied. There is no statistically significant difference between the purchasing averages of the control and test groups.