#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from config import file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7

logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)
def read_in():
    #Reads in file paths from config file and put them into a single dataframe
    coal = pd.read_csv(file_path_1)
    nat_gas = pd.read_csv(file_path_2)
    wind = pd.read_csv(file_path_3)
    renew = pd.read_csv(file_path_4)
    nuclear = pd.read_csv(file_path_5)
    hydro = pd.read_csv(file_path_6)
    petro = pd.read_csv(file_path_7)
    coal['Source'] = 'coal'
    nat_gas['Source'] = 'natural_gas'
    wind['Source'] = 'wind'
    renew['Source'] = 'renew'
    nuclear['Source'] = 'nuclear'
    hydro['Source'] = 'hydro'
    petro['Source'] = 'petro'
    df = pd.concat([coal, nat_gas, wind, renew, nuclear, hydro, petro])
    for x in df.State.unique():
        df = df.replace(x, x[3:])
    return df

def create_date(df):
    #Dataframes are fed in as columns so this isolates each month and makes that an entry row-wise before all months are
    #concated together
    dataframes = []
    for x in df.columns[1:-1]:
        placeholders = ['State', 'Source']
        temp = df[placeholders]
        temp['Date'] = str(x)
        temp['Electricity'] = df[x]
        dataframes.append(temp)
    start = dataframes[0]
    for x in dataframes[1:]:
        start = pd.concat([start, x])
    df = start
    return df

def fix_date(df):
    #Converts date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
    return df

def take_input(df):
    #Takes input to define dataframe by state
    print('Enter the initials state you want to view(to see the total for the US leave blank):')
    ab = str(input()).upper()
    df_ = df
    x = 'US'
    return df_, x
    
def create_cats(df_):
    #Seperates new dataframe for source specific information
    coal = pd.DataFrame(df_[df_['Source'] == 'coal'].groupby('Date')['Electricity'].sum()).reset_index()
    nat_gas = pd.DataFrame(df_[df_['Source'] == 'natural_gas'].groupby('Date')['Electricity'].sum()).reset_index()
    wind = pd.DataFrame(df_[df_['Source'] == 'wind'].groupby('Date')['Electricity'].sum()).reset_index()
    renew = pd.DataFrame(df_[df_['Source'] == 'renew'].groupby('Date')['Electricity'].sum()).reset_index()
    nuclear = pd.DataFrame(df_[df_['Source'] == 'nuclear'].groupby('Date')['Electricity'].sum()).reset_index()
    hydro = pd.DataFrame(df_[df_['Source'] == 'hydro'].groupby('Date')['Electricity'].sum()).reset_index()
    petro = pd.DataFrame(df_[df_['Source'] == 'petro'].groupby('Date')['Electricity'].sum()).reset_index()
    return coal, nat_gas, wind, renew, nuclear, hydro, petro

def time_graph(coal, nat_gas, wind, renew, nuclear, hydro, petro, x):
    #Use input to create a time series graph
    plt.figure(figsize=[12, 12])
    plt.plot(coal.Date, coal.Electricity, color='red', label='Coal')
    plt.plot(nat_gas.Date, nat_gas.Electricity, color='blue', label='Natural Gas')
    plt.plot(wind.Date, wind.Electricity, color='yellow', label='Wind')
    plt.plot(renew.Date, renew.Electricity, color='green', label='Renewables')
    plt.plot(nuclear.Date, nuclear.Electricity, color='orange', label='Nuclear')
    plt.plot(hydro.Date, hydro.Electricity, color='black', label='Hydroelectricity')
    plt.plot(petro.Date, petro.Electricity, color='purple', label='Petrochemcials')
    plt.legend(loc='upper left')
    plt.grid(color='black')
    plt.title('Electricity generation in US by Source')
    plt.xlabel('Date')
    plt.ylabel('Electricity generated(thousand megawatt per hour)')
    plt.show()
    
def bar_graph(coal, nat_gas, wind, renew, nuclear, hydro, petro, x, df_):
    #Creates a bar graph to show percentages of electricity generated
    total = df_.Electricity.sum()
    electricity = [(coal.Electricity.sum() / df_.Electricity.sum()) * 100, (nat_gas.Electricity.sum() / df_.Electricity.sum())  * 100, (wind.Electricity.sum() / df_.Electricity.sum())  * 100, (renew.Electricity.sum() / df_.Electricity.sum())  * 100, (nuclear.Electricity.sum() / df_.Electricity.sum())  * 100, (hydro.Electricity.sum() / df_.Electricity.sum())  * 100, (petro.Electricity.sum() / df_.Electricity.sum())  * 100]
    sources = ['coal', 'natural gas', 'wind', 'renewables', 'nuclear', 'hydro energy', 'petrochemicals']
    plt.figure(figsize=[12, 12])
    plt.bar(sources, electricity, edgecolor='Black')
    plt.xticks(label=sources)
    plt.ylabel('Percent of electricity generated')
    plt.xlabel('Source')
    plt.title('Electricity generated in US since 2000')
    plt.show()


def main():
    logger.info('Import data files from config')
    df = read_in()
    
    logger.info('Create Date column and stop using dates as columns')
    df = create_date(df)
    
    logger.info('Fixes date column')
    df = fix_date(df)
    
    logger.info('Takes input for visuals')
    df_, x = take_input(df)
    
    logger.info('Create source categories')
    coal, nat_gas, wind, renew, nuclear, hydro, petro = create_cats(df_)
    
    logger.info('Create time series graph')
    time_graph(coal, nat_gas, wind, renew, nuclear, hydro, petro, x)
    
    logger.info('Create a bar graph')
    bar_graph(coal, nat_gas, wind, renew, nuclear, hydro, petro, x, df_)
    
    logger.info('Export to csv')
    df.to_csv('US_power.csv')
    
if __name__ == '__main__':
    main()