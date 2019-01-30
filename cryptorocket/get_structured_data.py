# coding: utf-8

# Import modules
import pandas as pd
import ijson
import urllib
from decimal import Decimal
from time import gmtime, strftime


def api_to_pandas(csv=False):
    """
    This function is used to call the top 100 cryptos ranking from CMC API and to store it into a pandas dataframe
    """

    # Get the data
    f = urllib.request.urlopen(
        "https://api.coinmarketcap.com/v2/ticker/?structure=array&convert=BTC"
    )
    objects = ijson.items(f, "data.item")
    columns = list(objects)

    # Keep only the key attributes of interest
    main_column_names = [
        col for col in columns[0].keys() if col not in ("quotes", "id", "last_updated")
    ]
    usd_column_names = ["usd_" + col for col in columns[0]["quotes"]["USD"].keys()]
    btc_column_names = ["btc_" + col for col in columns[0]["quotes"]["USD"].keys()]
    column_names = main_column_names + usd_column_names + btc_column_names

    # Take values from those attributes
    data = []
    for rank in range(len(columns)):
        main_info = []
        for col in main_column_names:
            main_info.append(columns[rank][col])
        # Collect economic informations relative to USD and BTC
        usd_info = list(columns[rank]["quotes"]["USD"].values())
        btc_info = list(columns[rank]["quotes"]["BTC"].values())
        info = main_info + usd_info + btc_info
        for index, value in enumerate(info):
            if type(value) == Decimal:
                info[index] = float(value)
        data.append(info)

    # Create a pandas dataframe
    cmc_df = pd.DataFrame(data, columns=column_names)
    cmc_df.set_index("symbol", inplace=True)
    cmc_df.drop(
        [
            "usd_percent_change_1h",
            "btc_volume_24h",
            "btc_market_cap",
            "btc_percent_change_1h",
        ],
        axis=1,
        inplace=True,
    )
    cmc_df["perc_market_cap_top100"] = (
        cmc_df.usd_market_cap * 100 / cmc_df.usd_market_cap.sum()
    )

    # Store the dataframe locally as a csv file
    if csv == True:
        cmc_df.to_csv('cmc_top100_' + strftime("%Y-%m-%d", gmtime()) + '.csv')
        print("File successfully saved under the name cmc_top100_" + strftime("%Y-%m-%d", gmtime()) + ".csv")
    
    return cmc_df
