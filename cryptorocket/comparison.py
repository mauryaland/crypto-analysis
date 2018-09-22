import pandas as pd
from datetime import date
import re
import numpy as np

class CMComparison():
    
    def __init__(self, old_cmc_data, fresh_cmc_data):
        self.old_cmc_data = old_cmc_data
        self.fresh_cmc_data = fresh_cmc_data
        self.df_old = pd.read_csv(old_cmc_data, index_col=0)
        self.df_fresh = pd.read_csv(fresh_cmc_data, index_col=0)
        
    def enhanced_fresh_top100(self):
        
        """
        This function returns the freshest CMC ranking dataframe with 
        all new information computed in multiple new columns
        """
        
        # Add delta_ranking and pct_change_market_cap columns
        df = pd.concat([self.df_fresh, self.delta_ranking(), self.pct_change_market_cap()], 
                       axis=1, sort=False, join='outer')
        
        # Add USD and BTC pct change columns if delta days is not 1 or 7
        if self.usd_percent_change() is not None:
            df = pd.concat([df, self.usd_percent_change(), self.btc_percent_change()],
                           axis=1, sort=False, join='outer')
        
        return df
        
        
    def delta_ranking(self):
        
        """
        This function returns a dataframe indexed by cryptocurrency symbols with a new
        column which is the delta of the ranking with the old CMC ranking dataset
        """
        
        # Compute the delta_rank dataframe
        index = []
        delta_rank = []
        for i in self.df_old.index:
            if i in self.df_fresh.index:
                index.append(i)
                delta_rank.append(int(self.df_old['rank'].loc[i] - self.df_fresh['rank'].loc[i]))
        delta_df = pd.DataFrame(data={'delta_rank': delta_rank}, index=index, dtype=np.int64)
        
        return delta_df
    
    def pct_change_market_cap(self):
   
        """
        This function returns dataframe indexed by cryptocurrency symbols with a new 
        column which is the percent change of the market cap of each cryptocurrency
        """

        # Compute the pct_change_market_cap dataframe
        index = []
        pct_change_market_cap = []
        for i in self.df_old.index:
            if i in self.df_fresh.index:
                index.append(i)
                pct_change_market_cap.append((self.df_fresh['usd_market_cap'].loc[i] - self.df_old['usd_market_cap'].loc[i]) * 100 / self.df_old['usd_market_cap'].loc[i])
        pct_df = pd.DataFrame(data={'pct_change_market_cap': pct_change_market_cap}, index=index)  
        
        return pct_df
    
    def usd_percent_change(self):
        
        """
        This function returns dataframe indexed by cryptocurrency symbols with a new 
        column which is the percent change of the usd price of each cryptocurrency
        
        """
        # Compute difference of days between the two datasets
        year_old, month_old, day_old = map(int, re.findall(r'\d{4}-\d{2}-\d{2}', self.old_cmc_data)[0].split('-'))
        year_fresh, month_fresh, day_fresh = map(int, re.findall(r'\d{4}-\d{2}-\d{2}', self.fresh_cmc_data)[0].split('-'))
        day_old = date(year_old, month_old, day_old)
        day_fresh = date(year_fresh, month_fresh, day_fresh)
        delta = day_fresh - day_old
        
        # If the number of days is 1 or 7, information is already include
        # Otherwise, compute a new column in the dataframe
        if delta.days in {1, 7}:
            print('Information already in the columns:\n \
                   - usd_percent_change_24h\n \
                   - usd_percent_change_7d')
        else:
            index = []
            usd_percent_change = []
            for i in self.df_old.index:
                if i in self.df_fresh.index:
                    index.append(i)
                    usd_percent_change.append((self.df_fresh['usd_price'].loc[i] - self.df_old['usd_price'].loc[i]) * 100 / self.df_old['usd_price'].loc[i])
            usd_pct_df = pd.DataFrame(data={'usd_percent_change_' + str(delta.days) + 'd': usd_percent_change}, index=index)
            
            return usd_pct_df
        
        
    def btc_percent_change(self):
        
        """
        This function returns a dataframe indexed by cryptocurrency symbols with a new 
        column which is the percent change of the btc price of each cryptocurrency
        
        """
        # Compute difference of days between the two datasets
        year_old, month_old, day_old = map(int, re.findall(r'\d{4}-\d{2}-\d{2}', self.old_cmc_data)[0].split('-'))
        year_fresh, month_fresh, day_fresh = map(int, re.findall(r'\d{4}-\d{2}-\d{2}', self.fresh_cmc_data)[0].split('-'))
        day_old = date(year_old, month_old, day_old)
        day_fresh = date(year_fresh, month_fresh, day_fresh)
        delta = day_fresh - day_old
        
        # If the number of days is 1 or 7, information is already include
        # Otherwise, compute a new column in the dataframe
        if delta.days in {1, 7}:
            print('Information already in the columns:\n \
                   - btc_percent_change_24h\n \
                   - btc_percent_change_7d')
            
        else:
            index = []
            btc_percent_change = []
            for i in self.df_old.index:
                if i in self.df_fresh.index:
                    index.append(i)
                    btc_percent_change.append((self.df_fresh['btc_price'].loc[i] - self.df_old['btc_price'].loc[i]) * 100 / self.df_old['btc_price'].loc[i])
            btc_pct_df = pd.DataFrame(data={'btc_percent_change_' + str(delta.days) + 'd': btc_percent_change}, index=index)
            
            return btc_pct_df
    
    
    def newcomers_top100(self):
        
        """
        This function returns a dataframe containing only the new cryptocurrencies
        that appears the CMC top100 for the freshest CMC top 100 put as input since the oldest 
        CMC top100 dataframe put as input
        """
        
        newcomers = self.df_fresh.index.difference(self.df_old.index)
        return self.df_fresh.loc[newcomers]
    
    def out_top100(self):
        
        """This function returns a list of the cryptocurrencies out of the CMC top100"""
        
        out = list(self.df_old.index.difference(self.df_fresh.index))
        return out
        
        
