import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import math

warnings.filterwarnings("ignore")

import tensorflow as tf

import constants

# ---------------------------------------------------------------------Preprocessing--------------------------------------------------------------------------
print("To Start reading samples from dataset")
df = pd.read_csv(constants.SOURCE_CSV)
# check number of df after dropping rows. it was 2260701 initially
print("Initial Rows count:", len(df))

df = df.drop("id", axis=1)

# We will drop rows which have loan_status other than Fully Paid and Charged Off
df = df[(df["loan_status"] == "Fully Paid") | (df["loan_status"] == "Charged Off")]
# check number of df after dropping rows
print(
    "check number of df after dropping rows other than loan status is fully paid or charged off:",
    len(df),
)

# Data Cleaning
keep = df.columns[((df.isnull().sum() / len(df)) * 100 < 50)].to_list()
df = df[keep]  # dropping features with 50% or more missing data
print("Rows,columns:", df.shape)

# Since some features will not be available before getting loan, we select only those features that will be available during loan application
final_features = [
    "addr_state",
    "annual_inc",
    "earliest_cr_line",
    "emp_length",
    "emp_title",
    "fico_range_high",
    "fico_range_low",
    "grade",
    "home_ownership",
    "application_type",
    "initial_list_status",
    "int_rate",
    "loan_amnt",
    "num_actv_bc_tl",
    "mort_acc",
    "tot_cur_bal",
    "open_acc",
    "pub_rec",
    "pub_rec_bankruptcies",
    "purpose",
    "revol_bal",
    "revol_util",
    "sub_grade",
    "term",
    "title",
    "total_acc",
    "verification_status",
    "loan_status",
]
df = df[final_features]

# 1)addr_state represents the state provided by borrower
add_state_dummies = pd.get_dummies(
    df["addr_state"], drop_first=True
)  # drop_first will drop the first dummy column
df = pd.concat([df.drop("addr_state", axis=1), add_state_dummies], axis=1)

# 2)The self-reported annual income provided by the borrower during registration.
# There are 13447 rows of customers with annual_inc > 250000, i.e., 1%. Since these are outliers, let's drop these rows.
# Lets remove the rows with annual_inc > $250000
df = df[df["annual_inc"] <= 250000]

# 3)The month and year the borrower's earliest reported credit line was opened.
# Lets remove the month and just keep the year as integer.
df["earliest_cr_line"] = df["earliest_cr_line"].apply(lambda date: int(date[-2:]))

# 4)Employment length in years. Possible values are between 0 and 10 where 0 means less than one year and 10 means ten or more years.
emp_charged_off = (
    df[df["loan_status"] == "Charged Off"].groupby("emp_length").count()["loan_status"]
)
emp_fully_paid = (
    df[df["loan_status"] == "Fully Paid"].groupby("emp_length").count()["loan_status"]
)
percentage_charged_off = (emp_charged_off * 100) / (emp_charged_off + emp_fully_paid)
# plt.figure(figsize=(12,4), dpi=130).show()
percentage_charged_off.plot(kind="bar", cmap="viridis")
# There is not much differnce. This feature won't make much differnece in our training and predictions. Hence, its better to drop this feature.
df = df.drop("emp_length", axis=1)

# 5)The job title supplied by the Borrower when applying for the loan.
print(df["emp_title"].describe())
# There are 378007 unique values, way too many to create dummies. Hence, it is wise to drop this feature.
df = df.drop("emp_title", axis=1)

# 6) Fico range low and fico range fico_range_high
# Both fico_range_high and fico_range_low have similar mean and standard deviation. So, we will use mean of both scores.
df["fico"] = (df["fico_range_high"] + df["fico_range_low"]) / 2
df = df.drop(["fico_range_high", "fico_range_low"], axis=1)
# plt.figure(figsize=(10,5), dpi=70).show()
sns.boxplot(data=df, y="loan_status", x="fico", palette="viridis")
# There is a differnce between fico scores of customers who Fully paid loan and who did not.

# 7)LC assigned loan grade and sub grade.
# Customers who don't pay back loan have higher grade.<br>
# Information of 'grade' is already embedded in 'sub_grade'.
# plt.figure(figsize=(16,4)).show()
subgrade_order = sorted(df["sub_grade"].unique())
sns.countplot(
    x="sub_grade", data=df, order=subgrade_order, palette="viridis", hue="loan_status"
)
# Let's drop 'grade' feature.
df = df.drop("grade", axis=1)
dummies_sub_grade = pd.get_dummies(df["sub_grade"], drop_first=True)
df = pd.concat([df.drop("sub_grade", axis=1), dummies_sub_grade], axis=1)

# 8)The home ownership status provided by the borrower during registration or obtained from the credit report. Our values are: RENT, OWN, MORTGAGE, OTHER.
# Let's merge 'ANY' and 'NONE' into 'OTHER'.
df["home_ownership"] = df["home_ownership"].replace(["NONE", "ANY"], "OTHER")
dummies_home_ownership = pd.get_dummies(df["home_ownership"], drop_first=True)
df = pd.concat([df.drop("home_ownership", axis=1), dummies_home_ownership], axis=1)

# 9)Indicates whether the loan is an individual application or a joint application with two co-borrowers.
charged_off = (
    df[df["loan_status"] == "Charged Off"]
    .groupby("application_type")
    .count()["loan_status"]
)
fully_paid = (
    df[df["loan_status"] == "Fully Paid"]
    .groupby("application_type")
    .count()["loan_status"]
)
percentage_charged_off = (charged_off * 100) / (charged_off + fully_paid)
# plt.figure(figsize=(10,5), dpi=70).show()
percentage_charged_off.plot(kind="bar", cmap="viridis")
plt.title("Percentage charged off per application_type category")
# plt.show()
# There is difference between categories of home_ownership
dummies_application_type = pd.get_dummies(df["application_type"], drop_first=True)
df = pd.concat([df.drop("application_type", axis=1), dummies_application_type], axis=1)

# 10)The initial listing status of the loan. Possible values are – W(Whole), F(Fractional).
charged_off = (
    df[df["loan_status"] == "Charged Off"]
    .groupby("initial_list_status")
    .count()["loan_status"]
)
fully_paid = (
    df[df["loan_status"] == "Fully Paid"]
    .groupby("initial_list_status")
    .count()["loan_status"]
)
percentage_charged_off = (charged_off * 100) / (charged_off + fully_paid)
percentage_charged_off.plot(kind="bar", cmap="viridis")
plt.title("Percentage charged off per initial_list_status category")
# plt.show()
# Percentage charged off is almost same. Let's drop this feature.
df = df.drop("initial_list_status", axis=1)

# 11)Interest Rate on the loan.
sns.boxplot(data=df, y="loan_status", x="int_rate", palette="viridis")
# Clear difference can be seen in the mean 'int_rate' between the two 'loan_status' categories

# 12)The listed amount of the loan applied for by the borrower. If at some point in time, the credit department reduces the loan amount, then it will be reflected in this value.
sns.boxplot(data=df, y="loan_status", x="loan_amnt", palette="viridis")
# Clear difference can be seen in the mean 'loan_amnt' between the two 'loan_status' categories.

# 13)Number of currently active bankcard accounts.
sns.boxplot(data=df, y="loan_status", x="num_actv_bc_tl", palette="viridis")
# Minute difference can be seen in the mean 'num_actv_bc_tl' between the two 'loan_status' categories. We will go ahead and keep this feature.
# Range of num_actv_bc_tl is from 0 to 35 with mean at 3.64 and mojority of values between 2 to 5. Lets fill the missing values with the integer value closest to mean, i.e., 4.
df["num_actv_bc_tl"] = df["num_actv_bc_tl"].fillna(4)
# Since there are some outliers, we will drop rows with customers with 'num_actv_bc_tl' > 9.
df = df[df["num_actv_bc_tl"] < 10]

# 14)Number of mortgage accounts.
sns.boxplot(data=df, y="loan_status", x="mort_acc", palette="viridis")
# Minute difference can be seen in the mean 'mort_acc' between the two 'loan_status' categories. We will go ahead and keep this feature.
df.corr()["num_actv_bc_tl"].sort_values()[:-1]
# 'num_actv_bc_tl' and 'open_acc' are closely related. Let's fill missing 'mort_acc' by the mode of corresponding value in 'num_actv_bc_tl'.
df["mort_acc"] = df["mort_acc"].fillna(
    df.groupby("open_acc")["mort_acc"].transform(lambda x: x.value_counts().index[0])
)
# Since there are some outliers, we will drop rows with customers with mort_acc > 8.
df = df[df["mort_acc"] < 9]

# 15)The total number of credit lines currently in the borrower's credit file.
df.groupby("loan_status")["total_acc"].describe()
# Difference can be seen in the mean 'total_acc' between the two 'loan_status' categories. We will go ahead and keep this feature.
# Since there are some outliers, we will drop rows with customers with 'total_acc' > 63.
df = df[df["total_acc"] < 64]

# 16)Total current balance of all accounts.
df["tot_cur_bal"] = df["tot_cur_bal"].fillna(df["tot_cur_bal"].describe()["mean"])
# Since there are some outliers, we will drop rows with customers with 'tot_cur_bal' > $1000000.
df = df[df["tot_cur_bal"] < 1000001]
df.groupby("loan_status")["tot_cur_bal"].describe()
# Mean 'tot_cur_bal' is higher in case of customers who fully paid the loan.

# 17)The number of open credit lines in the borrower's credit file.
df.groupby("loan_status")["open_acc"].describe()
# Minute difference can be seen in the mean 'open_acc' between the two 'loan_status' categories. We will go ahead and keep this feature.

# 18)Number of derogatory public records.
# There are some outliers. Let's drop the rows with customers who have 'pub_rec > 2.
df = df[df["pub_rec"] < 3]
df.groupby("loan_status")["pub_rec"].describe()
# Minute difference can be seen in the mean 'pub_rec' between the two 'loan_status' categories. We will go ahead and keep this feature.

# 19)Number of public record bankruptcies.
df.groupby("loan_status")["pub_rec_bankruptcies"].describe()


# Minute difference can be seen in the mean 'pub_rec' between the two 'loan_status' categories. We will go ahead and keep this feature.
def inc_cat(income):
    if income < 50000:
        return "cat 1"
    if income >= 50000 and income < 100000:
        return "cat 2"
    if income >= 100000 and income < 150000:
        return "cat 3"
    if income >= 150000 and income < 200000:
        return "cat 4"
    if income >= 200000:
        return "cat 5"


df["annual_inc_categorised"] = df["annual_inc"].apply(
    inc_cat
)  # make a new column in the df for categorised income
df["pub_rec_bankruptcies"] = df["pub_rec_bankruptcies"].fillna(
    df.groupby("annual_inc_categorised")["pub_rec_bankruptcies"].transform("mean")
)
df = df.drop("annual_inc_categorised", axis=1)

# 20)A category provided by the borrower for the loan request.
# plt.figure(figsize=(14,6)).show()
charged_off = (
    df[df["loan_status"] == "Charged Off"].groupby("purpose").count()["loan_status"]
)
fully_paid = (
    df[df["loan_status"] == "Fully Paid"].groupby("purpose").count()["loan_status"]
)
percentage_charged_off = (charged_off * 100) / (charged_off + fully_paid)
percentage_charged_off.plot(kind="bar", cmap="viridis")
plt.title("Percentage charged off per purpose category")
# plt.show()
dummies_purpose = pd.get_dummies(df["purpose"], drop_first=True)
df = pd.concat([df.drop("purpose", axis=1), dummies_purpose], axis=1)

# 21)The number of payments on the loan. Values are in months and can be either 36 or 60.
# Let's convert these strings to integers.
df["term"] = df["term"].apply(lambda x: int(x[1:3]))
charged_off = (
    df[df["loan_status"] == "Charged Off"].groupby("term").count()["loan_status"]
)
fully_paid = (
    df[df["loan_status"] == "Fully Paid"].groupby("term").count()["loan_status"]
)
percentage_charged_off = (charged_off * 100) / (charged_off + fully_paid)
percentage_charged_off.plot(kind="bar", cmap="viridis")
plt.title("Percentage charged off per term category")
# plt.show()
# Customers whose loan term was 60 months had almost double chance of charging off.
dummies_term = pd.get_dummies(df["term"], drop_first=True)
pd.concat([df.drop("term", axis=1), dummies_term], axis=1)

# 22)The loan title provided by the borrower
len(df["title"].unique())
# This feature has a lot of unique values for dummies. Plus this info and the info in feature purpose is closely matching. Lets drop this feature
df = df.drop("title", axis=1)

# 23) Total credit revolving balance.
# There are some outliers. Let's drop rows with 'revol_bal' > $100000.
df = df[df["revol_bal"] < 100001]
df.groupby("loan_status")["revol_bal"].describe()
# Difference can be seen in the mean 'revol_bal' between the two 'loan_status' categories. We will go ahead and keep this feature.

# 24)Revolving line utilization rate, or the amount of credit the borrower is using relative to all available revolving credit.
df["revol_util"] = df["revol_util"].fillna(df["revol_util"].mean())
# There are some outliers. Let's drop them.
df = df[df["revol_util"] < 150]
df.groupby("loan_status")["revol_util"].describe()
# Difference can be seen in the mean 'revol_util' between the two 'loan_status' categories.

# 25)Indicates if income was verified by LC, not verified, or if the income source was verified.
charged_off = (
    df[df["loan_status"] == "Charged Off"]
    .groupby("verification_status")
    .count()["loan_status"]
)
fully_paid = (
    df[df["loan_status"] == "Fully Paid"]
    .groupby("verification_status")
    .count()["loan_status"]
)
percentage_charged_off = (charged_off * 100) / (charged_off + fully_paid)
percentage_charged_off.plot(kind="bar", cmap="viridis")
plt.title("Percentage charged off per verification_status category")
# plt.show()
# Difference can be seen betweeen percentage charged off per 'initial_list_status' categories.
dummies_verification_status = pd.get_dummies(df["verification_status"], drop_first=True)
df = pd.concat(
    [df.drop("verification_status", axis=1), dummies_verification_status], axis=1
)
# All features are done, except the feature we want to predict. Let us map the contents in the feature, i.e., 'Fully Paid' and 'Charged Off' to boolean values.
df["loan_status"] = df["loan_status"].map({"Fully Paid": 1, "Charged Off": 0})


df = df.reindex(
    columns=[col for col in df.columns if col != "loan_status"] + ["loan_status"]
)

print(df.shape)
# We have 22 columns after preprocessing
# ----------------------------------------------------------Preprocessing End------------------------------------------------------------------------

total_row_count=df.shape[0]
row_count=math.floor(total_row_count/3)
twice_row_count=row_count*2

print("total_row_count:",total_row_count)
print("row_count:",row_count)
print("twice_row_count:",twice_row_count)

df1 = df.iloc[:row_count]
df2 = df.iloc[row_count:twice_row_count]
df3 = df.iloc[twice_row_count:]
print(df1.shape, df2.shape, df3.shape)

import os
import shutil

parent_dir = os.getcwd()
directory = "generated"
parent_path = os.path.join(parent_dir, directory)
client1_path = os.path.join(parent_path, "client1")
client2_path = os.path.join(parent_path, "client2")
client3_path = os.path.join(parent_path, "client3")

try:
    for path in [parent_path, client1_path, client2_path, client3_path]:
        os.mkdir(path)
except:
    print("Already created path")

try:
    shutil.copy("./client.py", client1_path)
    shutil.copy("./constants.py", client1_path)
    df1.to_csv(client1_path + "/dataset.csv")
    shutil.copy("./client.py", client2_path)
    shutil.copy("./constants.py", client2_path)
    df2.to_csv(client2_path + "/dataset.csv")
    shutil.copy("./client.py", client3_path)
    shutil.copy("./constants.py", client3_path)
    df3.to_csv(client3_path + "/dataset.csv")
except:
    print("Copying and generating CSV failed")
