# coding: utf-8

# Import modules
import pandas as pd
import ijson
import urllib
from decimal import Decimal

def api_to_pandas(csv=False):
    """
    This function is used to call the top 100 cryptos ranking from CMC API and to store it into a pandas dataframe
    """
    
    # Get the data
    f = urllib.request.urlopen('https://api.coinmarketcap.com/v2/ticker/?structure=array')
    objects = ijson.items(f, 'data.item')
    columns = list(objects)
    
    # Keep only the key attributes of interest
    main_column_names = [col for col in columns[0].keys() if col not in ('quotes', 'id')]
    sub_column_names = [col for col in columns[0]['quotes']['USD'].keys()]
    column_names = main_column_names + sub_column_names

    # Take values from those attributes
    data = []
    for rank in range(len(columns)):
        main_info = []
        for col in main_column_names:
            main_info.append(columns[rank][col])
        # Collect informations economic informations in USD     
        sub_info = list(columns[rank]['quotes']['USD'].values())      
        info = main_info + sub_info
        for index, value in enumerate(info):
            if type(value) == decimal.Decimal:
                info[index] = float(value)            
        data.append(info)
        
    # Create a pandas dataframe
    cmc_df = pd.DataFrame(data, columns=column_names)
    cmc_df.drop('percent_change_1h', axis=1, inplace=True)
    
    # Store the dataframe locally as a csv file
    if csv == True:
        cmc_df.to_csv('cmc_top100_' + strftime("%Y-%m-%d", gmtime()) + '.csv')
    
    return cmc_df