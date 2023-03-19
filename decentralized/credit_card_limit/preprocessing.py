import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import math
import tensorflow as tf

def preprocess(source):
    warnings.filterwarnings("ignore")
    print("To Start reading samples from dataset")
    df = pd.read_csv(source)
    # check number of df after dropping rows. it was 2260701 initially
    print("Initial Rows count:", len(df))

    #Removing attributes which has missing values more than 50%
    keep = df.columns[((df.isnull().sum() / len(df)) * 100 < 50)].to_list()
    df = df[keep]
    print("Rows,columns after dropping attributes which has missing values more than 50%:", df.shape)


    print("Dropping fields about customer's personal details")
    df=df.drop(["CODE_GENDER","FLAG_OWN_CAR","FLAG_OWN_REALTY","CNT_CHILDREN","NAME_EDUCATION_TYPE","NAME_FAMILY_STATUS","REGION_POPULATION_RELATIVE","FLAG_MOBIL","FLAG_EMP_PHONE","FLAG_WORK_PHONE","FLAG_CONT_MOBILE","FLAG_PHONE","FLAG_EMAIL","FLAG_EMAIL","CNT_FAM_MEMBERS","REGION_RATING_CLIENT_W_CITY","REG_REGION_NOT_WORK_REGION","NAME_TYPE_SUITE","LIVE_REGION_NOT_WORK_REGION","REG_CITY_NOT_LIVE_CITY","REG_CITY_NOT_WORK_CITY","LIVE_CITY_NOT_WORK_CITY"],axis=1)


    print("Dropping fields about customer's housing")
    df=df.drop(['EMERGENCYSTATE_MODE', 'OBS_30_CNT_SOCIAL_CIRCLE',
           'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE',
           'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE'],axis=1)


    print("Dropping fields about customer's documents provided")
    df=df.drop(['FLAG_DOCUMENT_2',
           'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5',
           'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8',
           'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11',
           'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14',
           'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17',
           'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20',
           'FLAG_DOCUMENT_21'],axis=1)

    #Filling missing values
    # print(df.isnull().sum())
    for i in df.columns:
        if df[i].dtypes == 'object':
            df[i].fillna(df[i].mode()[0], inplace=True)
        else:
            df[i].fillna(df[i].median(), inplace=True)

    #SK_ID_CURR
    # print(len(df["SK_ID_CURR"].unique()))
    #There are 307511 unique values. It is field for uniquely identifying the record. So it is wise to drop the column.
    df = df.drop("SK_ID_CURR", axis=1)

    #NAME_CONTRACT_TYPE
    # print("NAME_CONTRACT_TYPE unique values:",len(df["NAME_CONTRACT_TYPE"].unique()))
    #Creating Dummies
    NAME_CONTRACT_TYPE_dummies = pd.get_dummies(df['NAME_CONTRACT_TYPE'])
    df = pd.concat([df.drop('NAME_CONTRACT_TYPE', axis=1), NAME_CONTRACT_TYPE_dummies], axis=1)

    #NAME_INCOME_TYPE
    # print("NAME_INCOME_TYPE unique values:",len(df["NAME_INCOME_TYPE"].unique()))
    #Creating Dummies
    NAME_INCOME_TYPE_dummies = pd.get_dummies(df['NAME_INCOME_TYPE'])
    df = pd.concat([df.drop('NAME_INCOME_TYPE', axis=1), NAME_INCOME_TYPE_dummies], axis=1)

    #NAME_HOUSING_TYPE
    # print(df["NAME_HOUSING_TYPE"].unique())
    # print("NAME_HOUSING_TYPE unique values:",len(df["NAME_HOUSING_TYPE"].unique()))
    #Creating Dummies
    NAME_HOUSING_TYPE_dummies = pd.get_dummies(df['NAME_HOUSING_TYPE'])
    df = pd.concat([df.drop('NAME_HOUSING_TYPE', axis=1), NAME_HOUSING_TYPE_dummies], axis=1)

    #OCCUPATION_TYPE
    # print(df["OCCUPATION_TYPE"].unique())
    # print("OCCUPATION_TYPE unique values:",len(df["OCCUPATION_TYPE"].unique()))
    #Creating Dummies
    OCCUPATION_TYPE_dummies = pd.get_dummies(df['OCCUPATION_TYPE'])
    df = pd.concat([df.drop('OCCUPATION_TYPE', axis=1), OCCUPATION_TYPE_dummies], axis=1)

    #ORGANIZATION_TYPE
    # print("ORGANIZATION_TYPE unique values:",len(df["ORGANIZATION_TYPE"].unique()))
    #Creating Dummies
    ORGANIZATION_TYPE_dummies = pd.get_dummies(df['ORGANIZATION_TYPE'])
    df = pd.concat([df.drop('ORGANIZATION_TYPE', axis=1), ORGANIZATION_TYPE_dummies], axis=1)


    #we notice that "DAYS_BIRTH"  'DAYS_EMPLOYED' 'DAYS_REGISTRATION' 'DAYS_ID_PUBLISH' columns have negative values,which is not not possible.
    #so we will try to correct this
    #we will now convert negative values to positve values using abs() and then convert days into years for better understanding
    days_cols = ['DAYS_BIRTH' ,'DAYS_EMPLOYED' ,'DAYS_REGISTRATION' ,'DAYS_ID_PUBLISH']
    df[days_cols] = df[days_cols].abs()
    df[days_cols] = df[days_cols]/365
    # print(df[days_cols].describe())
    #now that we have converted these values to years we need to update these column names as well to years
    df.rename(columns={'DAYS_BIRTH':'YEARS_BIRTH' ,'DAYS_EMPLOYED':'YEARS_EMPLOYED' ,'DAYS_REGISTRATION':'YEARS_REGISTRATION' ,'DAYS_ID_PUBLISH':'YEARS_ID_PUBLISH'}, inplace=True)

    #WEEKDAY_APPR_PROCESS_START
    #As The day of applying is not important, lets drop this column
    df = df.drop("WEEKDAY_APPR_PROCESS_START", axis=1)

    #HOUR_APPR_PROCESS_START
    #As the hour of applying is not important, lets drop this column
    df = df.drop("HOUR_APPR_PROCESS_START", axis=1)

    #YEARS_BEGINEXPLUATATION_AVG
    #As Information about house like entrance, size is not important, lets drop this column
    df = df.drop("YEARS_BEGINEXPLUATATION_AVG", axis=1)
    df = df.drop("YEARS_BEGINEXPLUATATION_MODE", axis=1)
    df = df.drop("YEARS_BEGINEXPLUATATION_MEDI", axis=1)

    #AMT_REQ_CREDIT_BUREAU_HOUR,AMT_REQ_CREDIT_BUREAU_DAY,AMT_REQ_CREDIT_BUREAU_WEEK,AMT_REQ_CREDIT_BUREAU_MON,AMT_REQ_CREDIT_BUREAU_QRT,AMT_REQ_CREDIT_BUREAU_YEAR
    #Dropping attributes containing number of enquiries made to credit bureau at different timeframe
    df = df.drop("AMT_REQ_CREDIT_BUREAU_HOUR", axis=1)
    df = df.drop("AMT_REQ_CREDIT_BUREAU_DAY", axis=1)
    df = df.drop("AMT_REQ_CREDIT_BUREAU_WEEK", axis=1)
    df = df.drop("AMT_REQ_CREDIT_BUREAU_MON", axis=1)
    df = df.drop("AMT_REQ_CREDIT_BUREAU_QRT", axis=1)
    df = df.drop("AMT_REQ_CREDIT_BUREAU_YEAR", axis=1)

    #FLOORSMAX_AVG,FLOORSMAX_MODE,FLOORSMAX_MEDI,TOTALAREA_MODE
    #Dropping attributes containing information about building where the client lives
    df = df.drop("FLOORSMAX_AVG", axis=1)
    df = df.drop("FLOORSMAX_MODE", axis=1)
    df = df.drop("FLOORSMAX_MEDI", axis=1)
    df = df.drop("TOTALAREA_MODE", axis=1)

    #checking the distribution of target variable
    sns.countplot(df['TARGET'])
    plt.xlabel("TARGET Value")
    plt.ylabel("Count of TARGET value")
    plt.title("Distribution of TARGET Variable")
    # plt.show()

    df = df.reindex(columns = [col for col in df.columns if col != 'TARGET'] + ['TARGET'])

    # print(list(df.columns))

    print("Final dataset shape:",df.shape)
    # We have 17 columns after preprocessing
    return df
