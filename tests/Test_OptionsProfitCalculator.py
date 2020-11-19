from ProfitCalculations.OptionsProfitCalculator import OptionsProfitCalculator

OPC = OptionsProfitCalculator()
print(OPC.getStockPrice(stock="F"))
print(OPC.getOptionsPrice(stock="F"))
expiry_dates = OPC.getOptionsDates(stock="F")
strike_prices = OPC.getOptionsStrikePrices(stock="F")
print(expiry_dates)
print(strike_prices)
print(OPC.getCallCreditSpread(stock = "F", expiry_date = expiry_dates[0], long_strike = 2.50, short_strike = 2.00, num = 1))

