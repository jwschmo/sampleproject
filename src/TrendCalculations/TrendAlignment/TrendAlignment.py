from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import quandl as qdl
from scipy.stats import linregress
from datetime import date

# get AAPL 10 years data
#                   Use for                 Investor        SwingTrader     DayTrader
# Primary Trend     Idea Generation         Week            Day             30 Minute
# Secondary Trend   Establish Risk/Reward   Day             30 Minute       10/5 Minute
# Minor Trend       Fine Tune Timing        30 Minute       10/5 Minute     2/1 Minute
# Total Days        Stage Idenfication      150 Days        30 Days         10 Days
# Moving Averages   Stage Idenfication                      10|20|50 Day    20

# Stage 1 - Accumulation - Accumulation follows a period of decline; it is the process of buyers fighting for control of the trend. It is a neutral period marked by contraction of price ranges that offer no tradable edge for a trend trader.
# Stage 2 - MarkUp - Once Buyers have gained control fo the stock and a pattern of higher highs and higher lows has been established, the path of least resistance is higher. It is a bull market and traders should be trading the long side aggressively as price expands higher in search of supply.
# Stage 3 - Distribution - After the market has exhausted the majority of buying demand, sellers become more aggressive, which turns the market neutral. This period of price contraction precedes a decline.
# Stage 4 - Decline - When the lows of stage 3 are breached, prcie expands to the downside in search of demand to satisy the aggressive supply being offered. The pattern of lower highs and lower lows is the hallmark of a bear market, and the only appropriate strategy for a trend trader is to sell short.


# Stage     Name            Stage Time Previous     High Label      Low Label   Combo Label         Price Trend
# Stage 1   Accumulation    Stage 4                 Neutral         Neutral     Pos|Neg Neg|Pos     Contraction
# Stage 2   MarkUp          Stage 1 | Stage 3       Positive        Postive     Pos|Pos             Rising
# Stage 3   Distribution    Stage 2                 Neutral         Neutral     Pos|Neg Neg|Pos     Contraction
# Stage 4   Decline         Stage 3 | Stage 1       Negative        Negative    Neg|Neg             Falling

class TrendAlignment():
    def __init__(self,dataSource = "AlphaVantage", key = "MIMIX4BAIRUQMJ4Y",output_format = "pandas", trader = "SwingTrader"):
        self.dataSource = dataSource
        self.apiKey = key
        self.output_format = output_format
        #print(dataSource)
        if trader == "SwingTrader":
            self.maNow = 10
            self.maNear = 20
            self.maFar = 50
            self.totalDays = 30
            self.time = "Days"
            self.primeT = "Day"
            self.secT = "30 Minute"
            self.minorT = "5 Minute"
        if dataSource == "AlphaVantage":
        	#print("Here")
        	self.ts = TimeSeries(key='MIMIX4BAIRUQMJ4Y', output_format='pandas')

    def getTrendLines(self, symbol = "MSFT"):
        today = date.today()
        data, meta_data = self.ts.get_daily_adjusted(symbol, outputsize='compact')
        data0 = data[:self.totalDays].copy()
        data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
        data0['date_id'] = data0['date_id'].dt.days + 1
        data1 = data0.copy()
        while len(data1)>3:
            #print("here")
            #print(data1.size)
            reg = linregress(
                            x=data1['date_id'],
                            y=data1['2. high'],
                            )
            data1 = data1.loc[data1['2. high'] > reg[0] * data1['date_id'] + reg[1]]
        
        reg = linregress(
                            x=data1['date_id'],
                            y=data1['2. high'],
                            )
        
        data0['high_trend'] = reg[0] * data0['date_id'] + reg[1]
        ht_slope = reg[0]
        ht_offset = reg[1]
        
        # low trend line
        
        data1 = data0.copy()
        
        while len(data1)>3:
            #print("here2")
            #print(data1.size)
            reg = linregress(
                            x=data1['date_id'],
                            y=data1['3. low'],
                            )
            data1 = data1.loc[data1['3. low'] < reg[0] * data1['date_id'] + reg[1]]
        
        reg = linregress(
                        x=data1['date_id'],
                        y=data1['3. low'],
                        )
        
        data0['low_trend'] = reg[0] * data0['date_id'] + reg[1]
        lt_slope = reg[0]
        lt_offset = reg[1]

        trend_metrics = [ht_slope, ht_offset, lt_slope, lt_offset]

        return data0, trend_metrics
    
    def getStageEst(self, symbol = "MSFT"):
        today = date.today()
        data0, trend_metrics = self.getTrendLines(symbol)
        data1 = self.getMAarray(symbol)
        confidence_factor = 0
        if trend_metrics[0] > 0 and trend_metrics[2] > 0:
            stageEst = "MarkUp"
            confidence_factor = (trend_metrics[0] + trend_metrics[2])/2
        elif trend_metrics[0] < 0 and trend_metrics[2] < 0:
            stageEst = "Decline"
        else:
        	stageEst = "Unknown"
        return symbol, stageEst, confidence_factor
    
    def getMAarray(self, symbol = "MSFT"):
        today = date.today()
        data, meta_data = self.ts.get_daily_adjusted(symbol, outputsize='compact')
        data0 = data.copy()
        data0 = data0.reindex(index=data0.index[::-1])
        data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
        data0['date_id'] = data0['date_id'].dt.days + 1
        #data1 = data0.copy()
        data0['MA50'] = data0['4. close'].rolling(window=50).mean()
        data0['MA20'] = data0['4. close'].rolling(window=20).mean()
        data0['MA10'] = data0['4. close'].rolling(window=10).mean()
        data0 = data0.reindex(index=data0.index[::-1])
        
        return data0[:self.totalDays].copy()

    def getSPYMAarray(self):
    	return self.getMAarray("SPY")

    def getStockSupport(self, symbol = "MSFT"):
    	min52 = 0
    	max52 = 0
    	min30day = 0
    	max30day = 0
    	return min52, max52, min30day, max30day

    def getStockSupRes(self, symbol = "MSFT",n = 28, min_touches = 1, stat_likeness_percent = 15, bounce_percent = 2):
        """Support and Resistance Testing
        Identifies support and resistance levels of provided price action data.
        Args:
            n(int): Number of frames to evaluate
            low(pandas.Series): A pandas Series of lows from price action data.
            high(pandas.Series): A pandas Series of highs from price action data.
            min_touches(int): Minimum # of touches for established S&R.
            stat_likeness_percent(int/float): Acceptable margin of error for level.
            bounce_percent(int/float): Percent of price action for established bounce.
        
        ** Note **
            If you want to calculate support and resistance without regard for
            candle shadows, pass close values for both low and high.
        Returns:
            sup(float): Established level of support or None (if no level)
            res(float): Established level of resistance or None (if no level)
        """
        # Setting default values for support and resistance to None
        sup = None
        res = None
    
        #data, meta_data = self.ts.get_daily_adjusted(symbol, outputsize='compact')
        data, meta_data = self.ts.get_daily_adjusted(symbol)
        data = data.iloc[::-1].copy()
        #data0 = data.copy()
    
        low = data['3. low']
        high = data['2. high']
        
        # Collapse into dataframe
        df = pd.concat([high, low], keys = ['high', 'low'], axis=1)
        df['sup'] = pd.Series(np.zeros(len(low)))
        df['res'] = pd.Series(np.zeros(len(low)))
        df['sup_break'] = pd.Series(np.zeros(len(low)))
        df['sup_break'] = 0
        df['res_break'] = pd.Series(np.zeros(len(high)))
        df['res_break'] = 0
        
        for x in range((n-1)+n, len(df)):
            # Split into defined timeframes for analysis
            tempdf = df[x-n:x+1]
            
            # Setting default values for support and resistance to None
            sup = None
            res = None
            
            # Identifying local high and local low
            maxima = tempdf.high.max()
            minima = tempdf.low.min()
            
            # Calculating distance between max and min (total price movement)
            move_range = maxima - minima
            
            # Calculating bounce distance and allowable margin of error for likeness
            move_allowance = move_range * (stat_likeness_percent / 100)
            bounce_distance = move_range * (bounce_percent / 100)
            
            # Test resistance by iterating through data to check for touches delimited by bounces
            touchdown = 0
            awaiting_bounce = False
            for y in range(0, len(tempdf)):
                if abs(maxima - tempdf.high.iloc[y]) < move_allowance and not awaiting_bounce:
                    touchdown = touchdown + 1
                    awaiting_bounce = True
                elif abs(maxima - tempdf.high.iloc[y]) > bounce_distance:
                    awaiting_bounce = False
            if touchdown >= min_touches:
                res = maxima
            # Test support by iterating through data to check for touches delimited by bounces
            touchdown = 0
            awaiting_bounce = False
            for y in range(0, len(tempdf)):
                if abs(tempdf.low.iloc[y] - minima) < move_allowance and not awaiting_bounce:
                    touchdown = touchdown + 1
                    awaiting_bounce = True
                elif abs(tempdf.low.iloc[y] - minima) > bounce_distance:
                    awaiting_bounce = False
            if touchdown >= min_touches:
                sup = minima
            if sup:
                df['sup'].iloc[x] = sup
            if res:
                df['res'].iloc[x] = res
        res_break_indices = list(df[(np.isnan(df['res']) & ~np.isnan(df.shift(1)['res'])) & (df['high'] > df.shift(1)['res'])].index)
        for index in res_break_indices:
            df['res_break'].at[index] = 1
        sup_break_indices = list(df[(np.isnan(df['sup']) & ~np.isnan(df.shift(1)['sup'])) & (df['low'] < df.shift(1)['sup'])].index)
        for index in sup_break_indices:
            df['sup_break'].at[index] = 1
        ret_df = pd.concat([df['sup'], df['res'], df['sup_break'], df['res_break']], keys = ['sup', 'res', 'sup_break', 'res_break'], axis=1)
        return ret_df