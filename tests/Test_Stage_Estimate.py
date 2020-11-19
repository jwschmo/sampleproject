from TrendCalculations.TrendAlignment.TrendAlignment import TrendAlignment
import matplotlib.pyplot as plt

#import unittest

#class TestSimple(unittest.TestCase):
#
#    def test_add_one(self):
#        self.assertEqual(add_one(5), 6)
#
#
#if __name__ == '__main__':
#    unittest.main()



trendAlign = TrendAlignment()
#data0, trendMetrics = trendAlign.getTrendLines(symbol = "AAPL")
#data1 = trendAlign.getMAarray(symbol = "AAPL")
print(trendAlign.getStageEst(symbol = "DIS"))

#data0['4. close'].plot(color = 'tab:blue')
#data0['high_trend'].plot(color = 'tab:green')
#data0['low_trend'].plot(color = 'tab:red')
#data1['MA50'].plot(color = 'tab:blue')
#data1['MA20'].plot(color = 'tab:green')
#data1['MA10'].plot(color = 'tab:red')


#print(trendMetrics[0])
#print(trendMetrics[1])
#print(trendMetrics[2])
#print(trendMetrics[3])

#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.plot(data0['date_id'], data0['4. close'], color='tab:blue')
#ax.plot(data0['date_id'], data0['low_trend'], color='tab:red')
#ax.plot(data0['date_id'], data0['high_trend'], color='tab:green')
#ax.plot(data1['date_id'], data1['MA50'], color='tab:blue')
#ax.plot(data1['date_id'], data1['MA20'], color='tab:green')
#ax.plot(data1['date_id'], data1['MA10'], color='tab:red')

#plt.show()
#weighted_Stock = IVList.algoPopHRankSymbol()
