# -*- coding: utf-8 -*-
"""Copy of Covid_Vacination_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11mji_pBT_xLIHDHXm8mHBylep7voYzag

# Google Authentication
"""

from google.colab import drive
drive.mount("/content/gdrive")

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/MyDrive/CSE519Fall2021/Final_Project

"""# Data Sets """

import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('Covid_countylevel.csv')

df_population=pd.read_csv('Population.csv')

df_education=pd.read_csv('Education_Degree.csv')

df_poverty=pd.read_csv('Poverty.csv')

df_employment=pd.read_csv('Employment_Rate.csv')

df_policy=pd.read_csv('State_Vaccination_policy.csv')

df_covid_cases=pd.read_csv("covid_cases.csv")

df.drop(df[df['FIPS']=='UNK'].index, inplace = True)

df['FIPS']=df['FIPS'].astype('float').astype('Int64')

df_population.rename(columns={'FIPStxt':'FIPS'},
inplace=True)

df_employment.rename(columns={'FIPS_Code':'FIPS'},
inplace=True)

df_population['Population'] = df_population['Population'].apply(lambda x:str(x).replace(",",""))

df_population['Population'] = df_population['Population'].astype('float').astype('Int64')

dataframe = df.merge(df_population, on=['FIPS'])

dataframe=dataframe.merge(df_education,on=['FIPS'])

dataframe=dataframe.merge(df_poverty, on=['FIPS'])

dataframe=dataframe.merge(df_employment, on=['FIPS'])

dataframe=dataframe.merge(df_policy,on='Recip_State')

dataframe=dataframe.drop(['State','Area name'],axis=1)

dataframe['Recip_County'].dropna(how='any',inplace=True)

dataframe['Date'] = pd.to_datetime(dataframe['Date'], format='%m/%d/%Y')

dataframe['YearMonth'] = dataframe['Date'].dt.strftime('%Y-%m')

dataframe1 = dataframe.pivot_table('Series_Complete_Yes', index='YearMonth', columns='Recip_County', 
                   aggfunc={'Series_Complete_Yes':['sum']})

dataframe['Date'] = pd.to_datetime(dataframe['Date'])
dataframe['Year'] = dataframe.Date.dt.year
dataframe['Month'] = dataframe.Date.dt.month

df_cc1=pd.read_csv("covid_p.csv")

df_cc2=pd.read_csv("covid_r.csv")

"""# Data PreProcessing"""

cols=['below_high_school','High_school_diploma','Some_college_degree','Higher_Bachelors_degree','Poverty_ALL','Median_Household_Income','Civilian_labor_force_2020','Employed_2020','Unemployed_2020']

for C in cols:
    dataframe[C] = dataframe[C].apply(lambda x:str(x).replace(",",""))

dataframe[cols] = dataframe[cols].astype('float').astype('Int64')

dataframe_any = dataframe.groupby(['Recip_County', 'FIPS','Recip_State','Free_Vaccine','Metro_status','Mandate_place']).mean()

dataframe['Metro_status'].fillna("Non-metro", inplace = True)

dataframe['Metro_status'] = dataframe['Metro_status'].map({'Non-metro': 0,'Metro': 1})

dataframe['Metro_status'] = dataframe['Metro_status'].astype(int)

colms=['Series_Complete_12Plus','Series_Complete_12PlusPop_Pct','Administered_Dose1_Recip','Administered_Dose1_Recip_12Plus','Administered_Dose1_Recip_12PlusPop_Pct','Administered_Dose1_Recip_18Plus','Administered_Dose1_Recip_65Plus',
       'Series_Complete_Pop_Pct_SVI','Series_Complete_12PlusPop_Pct_SVI','Series_Complete_18PlusPop_Pct_SVI','Series_Complete_65PlusPop_Pct_SVI','Series_Complete_Pop_Pct_UR_Equity','Series_Complete_12PlusPop_Pct_UR_Equity','Series_Complete_18PlusPop_Pct_UR_Equity',
       'Series_Complete_65PlusPop_Pct_UR_Equity']

dataframe[colms]=dataframe[colms].fillna(value=0)

dataframe['SVI_CTGY']=dataframe['SVI_CTGY'].fillna(value='E')

dataframe['SVI_CTGY']=dataframe['SVI_CTGY'].map({'A':1,'B':2,'C':3,'D':4,'E':0})

dataframe['SVI_CTGY']=dataframe['SVI_CTGY'].astype(int)

df_covid_cases['community_transmission_level'].unique()

df_covid_cases['community_transmission_level']=df_covid_cases['community_transmission_level'].fillna(value='0')

df_covid_cases['community_transmission_level']=df_covid_cases['community_transmission_level'].map({'substantial':2, 'high':3, 'low':0, 'moderate':1,'0':0})

df_covid_cases['report_date'].dropna(how='any',inplace=True)

df_covid_cases[['cases_per_100K_7_day_count_change','percent_test_results_reported_positive_last_7_days']]=df_covid_cases[['cases_per_100K_7_day_count_change','percent_test_results_reported_positive_last_7_days']].fillna(value=0)

#df_covid_cases.drop(columns=['state_name', 'county_name'], inplace=True)

#df_covid_cases['cases_per_100K_7_day_count_change']=df_covid_cases['cases_per_100K_7_day_count_change'].map({'suppressed':'0'})

#df_covid_cases['cases_per_100K_7_day_count_change'].value_counts()

#df_covid_cases['cases_per_100K_7_day_count_change']=df_covid_cases['cases_per_100K_7_day_count_change'].fillna(value=0)

dataframe['Date']=pd.to_datetime(dataframe['Date'],format='%M/%d/%Y')

dataframe['YearMonth']=pd.to_datetime(dataframe['YearMonth'],format='%Y-%m')

df_cc2.dropna(inplace=True)

df_cc2['date']=pd.to_datetime(df_cc2['date'])

df_cc2['YearMonth'] = df_cc2['date'].dt.strftime('%Y-%m')

"""# Analysis

**Correlation**
"""

option=['Series_Complete_Yes','Population','Poverty_ALL','Higher_Bachelors_degree','Median_Household_Income']

dataframe_feature = dataframe[option]
pearson = dataframe_feature.corr(method='pearson')
round(pearson,2)

dataframe_feature = dataframe[option]
pearson = dataframe_feature.corr(method='pearson')
import seaborn as sns
sns.heatmap(pearson,annot=True);

"""**Metro vs Non Metro**"""

x=dataframe[['Metro_status','Series_Complete_Yes']].groupby('Metro_status').sum()

x.plot(kind='bar')

"""**Vaccination Policies vs Vaccination trend**"""

jaffa=dataframe[['Free_Vaccine','Series_Complete_Yes']].groupby('Free_Vaccine').sum()

jaffa.plot(kind='bar')

daffa=dataframe.groupby(['Recip_County','Free_Vaccine']).agg({'Series_Complete_Yes':'sum'})

daffa.reset_index(level=0, inplace=True)

daffa.reset_index(level=0, inplace=True)

daffa

dataframe[['Recip_County','Free_Vaccine','Series_Complete_Yes']].groupby('Recip_County').mean()

plt.rcParams['figure.figsize'] = (12.0, 10.0)
for i in [0, 1]:
    data = daffa[daffa['Free_Vaccine'] == i]
    plt.scatter(data['Recip_County'], data['Series_Complete_Yes'], label=i)
plt.legend()
plt.xlabel('Recip_County')
plt.ylabel('Series_Complete_Yes')
plt.show()

"""**deep analysis**"""

df=dataframe

df.sort_values(by='Date',ascending=False,inplace=True)
df.reset_index(drop=True, inplace=True)

df["Total_vaccinations"]= df.groupby("Recip_County").Series_Complete_Yes.head(1)

dfc=df_cc2

dfc.sort_values(by='date',ascending=False,inplace=True)
dfc.reset_index(drop=True, inplace=True)

dfc["Total_Cases"]=dfc.groupby("fips").cases.head(1)

dfc.dropna(inplace=True)

"""**Top 20 Counties with Heighest Vaccinationation**"""

x=df.groupby("Recip_County")["Total_vaccinations"].mean().sort_values(ascending= False).head(20)

x.index

sns.set_style("darkgrid")
plt.figure(figsize= (10,10))
ax= sns.barplot(x.values,x.index)
ax.set_xlabel("Total de vacinações")
ax.set_ylabel("Países")
plt.show()

"""**Least 20 Counties with Low Vaccinationation**"""

l=df.groupby("Recip_County")["Total_vaccinations"].mean().sort_values(ascending= False).tail(20)

l.index

import seaborn as sns
sns.set_style("darkgrid")
plt.figure(figsize= (10,10))
ax= sns.barplot(l.values,l.index)
ax.set_xlabel("Total de vacinações")
ax.set_ylabel("Países")
plt.show()

"""**Top Counties vaccination Trend over the period**"""

y= df.loc[(df.Recip_County== "Los Angeles County") | (df.Recip_County== "San Diego County")| (df.Recip_County== "Maricopa County")| (df.Recip_County== "Miami-Dade County")|(df.Recip_County== "Queens County")]

plt.figure(figsize= (15,5))
sns.lineplot(x= "Date",y= "Series_Complete_Yes" ,data= y,hue= "Recip_County")
plt.xlabel("Data")
plt.ylabel("Total Vaccination")
plt.title("Vaccination trend")
plt.show()

"""**Lowest trend**"""

z= df.loc[(df.Recip_County== "Hawaii County")| (df.Recip_County== "Slope County")| (df.Recip_County== "Maui County")|(df.Recip_County== "Arthur County")]

plt.figure(figsize= (15,5))
sns.lineplot(x= "Date",y= "Series_Complete_Yes" ,data= z,hue= "Recip_County")
plt.xlabel("Data")
plt.ylabel("Total Vaccination")
plt.title("Vaccination trend")
plt.show()

"""**covid cases analysis**"""

covid_coun= [ 6037, 6073, 36081	, 4013, 12086]

tmp_cc=dfc[dfc['fips'].isin(covid_coun)]

tmp_cc

pie_rep=tmp_cc[['county','cases']].set_index('county')

pie_rep

zc= dfc.loc[(df_cc2.county== "Los Angeles")| (df_cc2.county== "Miami-Dade")| (df_cc2.county== "Maricopa")|(dfc.fips== 6073.0)]

zc.set_index('county')

zzc=zc[['county','cases','deaths']]

zzc.set_index('county',inplace=True)

zzc['cases']=np.log2(zzc['cases'])

zzc['deaths']=np.log2(zzc['deaths'])

zzc

zzc.plot.bar()

pie_rep.plot.pie(subplots=True,figsize=[10,10],autopct='%.2f',title='Covid_Cases', fontsize=15)
plt.legend(loc='lower left', bbox_to_anchor=(0.7, 1.05),
          ncol=3, fancybox=True, shadow=True);

covid_coun1=[48269,15001,38087,15009,31005]

tmp_cc1=dfc[dfc['fips'].isin(covid_coun1)]

tmp_cc1

zzc1=tmp_cc1[['county','cases','deaths']]

zzc1.set_index('county',inplace=True)

zzc1['cases']=np.log2(zzc1['cases'])
zzc1['deaths']=np.log2(zzc1['deaths'])

zzc1.plot.bar()

pie_rep1=tmp_cc1[['county','cases']].set_index('county')

pie_rep1.plot.pie(subplots=True,figsize=[10,10],autopct='%.2f',title='Covid_Cases', fontsize=15)
plt.legend(loc='lower left', bbox_to_anchor=(0.7, 1.05),
          ncol=3, fancybox=True, shadow=True);

#covid_coun= [ 6037, 17031, 48201,  4013, 12086,  6059,  6073, 36081, 53033, 36047,
        6085, 48113,  6065, 12011, 48029, 36061,  6001, 25017, 32003,  6071]

#covid_trend = df_covid_cases.loc[df_covid_cases['fips_code'].isin(covid_coun)]

#c= covid_trend.loc[(covid_trend.fips_code== 6037) | (covid_trend.fips_code== 17031)|(covid_trend.fips_code== 4013) |(covid_trend.fips_code== 12086)]

#c['report_date']=pd.to_datetime(c['report_date'],format='%Y/%M/%d')
#c['YearMonth'] = c['report_date'].dt.strftime('%Y-%m')

#c['Date']=pd.to_datetime(c['report_date'],format='%Y/%M')
#c['Date'] = c['report_date'].dt.strftime('%Y-%m')

plt.figure(figsize= (15,5))
sns.lineplot(x= "Date",y= "" ,data= c,hue= "county_name")
plt.xlabel("Date")
plt.ylabel("poverty")
plt.title("PercentageCovid Cases")
plt.show()

"""**Top Counties Data Collection**"""

county=['Los Angeles County', 'Maricopa County', 'Miami-Dade County',
       'San Diego County', 'Queens County', 'Kings County',
       'Santa Clara County', 'Riverside County', 'Broward County',
       'Bexar County', 'New York County', 'Alameda County',
       'San Bernardino County', 'Tarrant County', 'Suffolk County',
       'Nassau County', 'Philadelphia County', 'Sacramento County',
       'Palm Beach County', 'Bronx County']

llp=df.loc[df['Recip_County'].isin(county)]

llp['FIPS'].unique()

v_fips= [36081, 36005, 36059, 36047, 36103, 48029, 36061, 42101,  4013, 25025, 12011,
 12086, 48439,  6071,  6073, 12099, 12089,  6085,  6031,  6001,  6065,  6067,
  6037]

t_values=[6285278., 2265664., 2075462., 1755886., 1681946., 1550370.,
       1467364., 1271829., 1250590., 1226117., 1213258., 1197748.,
       1088050., 1068012., 1004932.,  980574.,  921631.,  913722.,
        906168.,  878777.]

top_df=df.loc[df['FIPS'].isin(v_fips)]

top_df=df.loc[df['Total_vaccinations'].isin(t_values)]

top_df.reset_index(drop=True,inplace=True)

imp_features=['FIPS','MMWR_week','Recip_County','SVI_CTGY','Series_Complete_12Plus','Recip_State','Metro_status', 'below_high_school','High_school_diploma',
              'Some_college_degree','Population','Higher_Bachelors_degree',	'Poverty_ALL',	'Median_Household_Income','Series_Complete_65Plus',
'Civilian_labor_force_2020',	'Employed_2020',	'Unemployed_2020',	'Free_Vaccine',	'Mandate_place',	'YearMonth','Total_vaccinations']

top_counties=top_df[imp_features]

top_counties.sort_values(by='Total_vaccinations',ascending=False,inplace=True)

top_counties.reset_index(drop=True,inplace=True)

"""**Top 5 Data Set**"""

repr=top_counties.head(5).reset_index(drop=True)

repr=repr.set_index('Recip_County')

sel=['Population','Employed_2020']
rep=repr[sel]

rep.plot.bar(figsize=[15,5])
plt.legend(loc='lower right', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True);

"""**Lowest Counties Data Collection**"""

counties=['Banner County', 'Billings County', 'Loup County', 'Nantucket County',
       'Petroleum County', 'Arthur County', 'Maui County', 'Slope County',
       'Hawaii County', 'King County', 'Trinity County', 'Modoc County',
       'Mono County', 'Mariposa County', 'Loving County', 'Alpine County',
       'Kauai County', 'Plumas County', 'Inyo County', 'Sierra County']

low_df=df.loc[df['Recip_County'].isin(counties)]

low_df['FIPS'].unique()

l_fips=[ 6063,  6091, 48301, 35051,  6043,  6003,  6051,  6049,  6105,  6027, 48455,
 48269, 38007, 25019, 38087, 30069, 31007, 15007, 15009, 53033, 31115, 15001,
 31005]

l_values=[201., 184., 181., 159., 139.,  81.,  78.,  75.,  64.,  56.]

low_df=df.loc[df['FIPS'].isin(l_fips)]

low_df=df.loc[df['Total_vaccinations'].isin(l_values)]

low_counties=low_df[imp_features]

low_counties.sort_values(by='Total_vaccinations',ascending=False,inplace=True)

low_counties.reset_index(drop=True,inplace=True)

"""**Least 5 Counties**"""

low_counties

rep2=low_counties.tail(5).set_index('Recip_County')

sel=['Population','Employed_2020']

#df_min_max_scaled = rep2[sel].copy()
   
# apply normalization techniques
for column in df_min_max_scaled.columns:
    df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

df_min_max_scaled=rep2[sel]

df_min_max_scaled['Population']=np.log2(df_min_max_scaled['Population'])

df_min_max_scaled['Employed_2020']=np.log2(df_min_max_scaled['Employed_2020'])

df_min_max_scaled

#df_max_scaled = rep2[sel].copy()
  
# apply normalization techniques
#for column in df_max_scaled.columns:
    #df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()

#df_max_scaled['Population']=200*df_max_scaled['Population']

#df_max_scaled['Employed_2020']=200*df_max_scaled['Employed_2020']

#df_max_scaled

df_min_max_scaled.plot.bar(figsize=[15,5])
plt.legend(loc='lower right', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True);

"""New Rule"""

repr.reset_index(level=0, inplace=True)

sc_rep=repr[['Recip_County','SVI_CTGY','Total_vaccinations']]

a=[3,4]

import matplotlib.pyplot as px
px.scatter(sc_rep,x='SVI_CTGY',y='Total_vaccinations', color='Recip_County',
           title='SVI_vs_Vaccination',range_y=[0,1500])

"""**K Means**"""

top_counties

low_counties

clu=top_counties[['SVI_CTGY','Total_vaccinations']].head(10)

from sklearn.cluster import KMeans
kmeans = KMeans(2).fit(clu)

centroids = kmeans.cluster_centers_

plt.scatter(clu['SVI_CTGY'], clu['Total_vaccinations'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

clu_l=low_counties[['SVI_CTGY','Total_vaccinations']].head(10)

from sklearn.cluster import KMeans
kmeans = KMeans(3).fit(clu_l)

centroids = kmeans.cluster_centers_

plt.scatter(clu_l['SVI_CTGY'], clu_l['Total_vaccinations'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

mains=df[['SVI_CTGY','Series_Complete_Yes']]

mains['SVI_CTGY'].unique()

from sklearn.cluster import KMeans
kmeans = KMeans(5).fit(mains)

centroids = kmeans.cluster_centers_
plt.figure(figsize=(8, 8))
plt.scatter(mains['SVI_CTGY'], mains['Series_Complete_Yes'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

low_counties

df_cc2

top_counties

allvac=df

allvac.dropna(inplace=True)

def plot_custom_scatter(df, x, y, size, color):
    fig = px.scatter(df, x=x, y=y, size=size, color=color)
    fig.update_layout({'legend_orientation':'h'})
    fig.update_layout(legend=dict(yanchor="top", y=-0.2))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='grey')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='grey')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.show()

plot_custom_scatter(allvac, x="Series_Complete_Yes", y="Population", size="Series_Complete_Yes", color="Recip_County")

"""**Covid Cases And deaths**"""

rep2.reset_index(level=0, inplace=True)

tmp_cc1['fips']=tmp_cc1['fips'].astype(int)

tmp_cc1.rename(columns={"fips": "FIPS"},inplace=True)

rep2=rep2.merge(tmp_cc1,on=['FIPS'])

rep2['cases']=np.log2(rep2['cases'])
rep2['deaths']=np.log2(rep2['deaths'])



sho=rep2[['Recip_County','Total_vaccinations','cases','deaths']]

sho.set_index('Recip_County',inplace=True)

sho.plot.bar(figsize=[15,5])

"""**high**"""

repr.reset_index(level=0, inplace=True)

tmp_cc['fips']=tmp_cc['fips'].astype(int)
tmp_cc.rename(columns={"fips": "FIPS"},inplace=True)

repr=repr.merge(tmp_cc,on=['FIPS'])

repr['cases']=np.log2(repr['cases'])
repr['deaths']=np.log2(repr['deaths'])

repr['Total_vaccinations']=np.log2(repr['Total_vaccinations'])

sho1=repr[['Recip_County','Total_vaccinations','cases','deaths']]

sho1.set_index('Recip_County',inplace=True)

sho1.plot.bar(figsize=[15,5])

"""# Model Linear Regression"""

feature_cols=['FIPS','Series_Complete_12Plus','Administered_Dose1_Recip_12Plus','SVI_CTGY','Series_Complete_12PlusPop_Pct_SVI','Metro_status',
              'Series_Complete_12PlusPop_Pct_UR_Equity','Population','below_high_school','High_school_diploma','Some_college_degree','Higher_Bachelors_degree','Poverty_ALL',
              'Free_Vaccine','Mandate_place','Median_Household_Income']

validation_set=dataframe[(dataframe['YearMonth'] > '2021-09')]
train=dataframe[(dataframe['YearMonth'] > '2020-09') & (dataframe['YearMonth'] < '2021-09')]

x_train=train[feature_cols]
y_train=train.Series_Complete_Yes

pd.to_datetime("12-11-2010 00:00", format="%d-%m-%Y %H:%M")

from sklearn.linear_model import LinearRegression

#X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=1)
lr = LinearRegression()
lr.fit(x_train,y_train)

y_pred1=lr.predict(validation_set[feature_cols])

import sklearn
import math

mse = sklearn.metrics.mean_squared_error(list(validation_set.Series_Complete_Yes), y_pred1)

rmse = math.sqrt(mse)

print(rmse)

"""# Model Random Regression"""

features_clmns =['Date','FIPS','Series_Complete_12Plus','Administered_Dose1_Recip_12Plus','SVI_CTGY','Series_Complete_12PlusPop_Pct_SVI','Metro_status',
              'Series_Complete_12PlusPop_Pct_UR_Equity','Population','below_high_school','High_school_diploma','Some_college_degree','Higher_Bachelors_degree','Poverty_ALL',
              'Free_Vaccine','Mandate_place','Median_Household_Income']

data_regre=dataframe

data_regre['Date'] = data_regre['Date'].values.astype(float)

validation_set=data_regre[(data_regre['YearMonth'] > '2021-09')]
train=data_regre[(data_regre['YearMonth'] > '2020-09') & (data_regre['YearMonth'] < '2021-09')]

X_train=train[features_clmns]
X_test=train['Series_Complete_Yes']
y_train=train[features_clmns]
y_test=validation_set['Series_Complete_Yes']

def rmpse(y_true, y_pred):
    ytr = []
    ypr = []
    cnt = 0
    for i, x in enumerate(y_true):
        if x==0:
            continue
        ytr.append(x)
        ypr.append(y_pred[i])
    rmpse = np.sqrt(np.mean(np.square(((np.array(ytr) - np.array(ypr)) / np.array(ytr))), axis=0))
    return rmpse

from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(n_estimators=50, max_depth=30, random_state=0)
X = train[features_clmns]
Y = train['Series_Complete_Yes']
regr.fit(X, Y)
y_pred=regr.predict(validation_set[features_clmns])
rmpse(validation_set["Series_Complete_Yes"].values, y_pred)

"""# Model ARIMA"""

features_clmns =['Date','FIPS','Recip_County','Series_Complete_12Plus','Administered_Dose1_Recip_12Plus','SVI_CTGY','Series_Complete_12PlusPop_Pct_SVI','Metro_status',
              'Series_Complete_12PlusPop_Pct_UR_Equity','Population','below_high_school','High_school_diploma','Some_college_degree','Higher_Bachelors_degree','Poverty_ALL',
              'Free_Vaccine','Mandate_place','Median_Household_Income']

dataframe = dataframe.sort_values('Recip_County')
dataframe['eid'] = (dataframe.groupby(['Recip_County']).cumcount()==0).astype(int)
dataframe['eid'] = dataframe['eid'].cumsum()

dataframe[dataframe['FIPS']==36103]

ndf=dataframe.loc[dataframe['eid'] == 1618]
sndf = ndf.sort_values('Series_Complete_Yes')
sndf

val=sndf['Series_Complete_Yes'].values

import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

# Original Series
fig, axes = plt.subplots(3, 2, sharex=True)
axes[0, 0].plot(val); axes[0, 0].set_title('Original Series')
plot_acf(val, ax=axes[0, 1])
# 1st Differencing
axes[1, 0].plot(np.diff(val)); axes[1, 0].set_title('1st Order Differencing')
plot_acf(np.diff(val), ax=axes[1, 1])
diffval = np.diff(val)

# 2nd Differencing
axes[2, 0].plot(np.diff(diffval)); axes[2, 0].set_title('2nd Order Differencing')
plot_acf(np.diff(diffval), ax=axes[2, 1])
plt.show()

pip install pmdarima

pip install pyramid-arima

pip install --upgrade Cython

pip install --upgrade git+https://github.com/statsmodels/statsmodels

from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
model = pm.auto_arima(val, start_p=1, start_q=1,
test='adf',
max_p=3, max_q=3,
m=1,
d=None,
seasonal=False,
start_P=0,
D=0,
trace=True,
error_action='ignore',
suppress_warnings=True,
stepwise=True)
print(model.summary())

model.plot_diagnostics(figsize=(7,5))
plt.show()

# Forecast
n_periods = 50
fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = np.arange(len(val), len(val)+n_periods)

# make series for plotting purpose
fc_series = pd.Series(fc, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.plot(val)
plt.plot(fc_series, color='darkgreen')
plt.fill_between(lower_series.index,
lower_series,
upper_series,
color='k', alpha=.15)
plt.title("Forecast of Vaccination Rate")
plt.show()

"""# model LSTM"""

data=dataframe.loc[dataframe['eid'] == 1618]

data=data.filter(['Series_Complete_Yes'])

from sklearn.preprocessing import MinMaxScaler
dataset = data.values

scaler = MinMaxScaler(feature_range=(-1, 0))
scaled_data = scaler.fit_transform(dataset)

"""# Model PyCaret """

pyf=dataframe.loc[dataframe['eid'] == 1618]

dataframe.info()

features_pyc =['Series_Complete_Yes','Series_Complete_12Plus','Completeness_pct',
              'Population','below_high_school','Unemployed_2020','Civilian_labor_force_2020','SVI_CTGY',
              'Free_Vaccine','Median_Household_Income','Year']

data_pycaret=pyf

data_pycaret['Date'] = data_pycaret['Date'].values.astype(float)

test=data_pycaret[(data_pycaret['YearMonth'] > '2021-09')]
train=data_pycaret[(data_pycaret['YearMonth'] > '2020-09') & (data_pycaret['YearMonth'] < '2021-09')]

train=train[features_pyc]
test=test[features_pyc]

train.shape, test.shape

pip install pycaret Metro_status 'High_school_diploma', 'High_school_diploma','Poverty_ALL',

from pycaret.regression import *

train.info()

s = setup(data = train, test_data = test, target = 'Series_Complete_Yes', fold_strategy = 'timeseries')

best = compare_models(sort = 'MAE')

