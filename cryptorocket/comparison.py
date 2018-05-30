import pandas as pd

class CMComparison():
    
    def __init__(self, old_cmc_data, fresh_cmc_data):
        self.df_old = pd.read_csv(old_cmc_data, index_col=0)
        self.df_fresh = pd.read_csv(fresh_cmc_data, index_col=0)
        
    def delta_ranking(self):
        
        """
        This function returns the freshest CMC ranking dataframe with a new
        column which is the delta of the ranking with the old CMC ranking dataset
        """
        
        # Compute the delta_rank dataframe
        index = []
        delta_rank = []
        for i in self.df_old.index:
            if i in self.df_fresh.index:
                index.append(i)
                delta_rank.append(self.df_old['rank'].loc[i] - self.df_fresh['rank'].loc[i])
        delta_df = pd.DataFrame(data={'delta_rank': delta_rank}, index=index, dtype=np.int64)

        # Merge this dataframe with the freshest CMC top100 data
        df_delta_rank = self.df_fresh.merge(delta_df, how='left', left_index=True, right_index=True)
        return df_delta_rank
    
    def pct_change_market_cap(self):
   
        """
        This function returns the freshest CMC ranking dataframe with a new 
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
        
        # Merge this dataframe with the freshest CMC top100 data
        df_pct_change_market_cap = self.df_fresh.merge(pct_df, how='left', left_index=True, right_index=True)
        return df_pct_change_market_cap 
    
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
        
        
