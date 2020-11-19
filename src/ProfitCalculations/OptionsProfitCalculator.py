import requests

class OptionsProfitCalculator:
    def __init__(self):
        self.web_session = requests.Session()
        
        #Bullish Spreads
        #Buy a Call - Bullish (Up)
        #Call Debit Spread - Bullish (Up) - Buying a Call (lower strike price)(Short Leg) and Selling a Call (higher strike price)(Long Leg)
        #Put Credit Spread - Bullish (Stay same or Up) - Selling a Put (higher stirke price) and Buying a Put (lower strike price)
        
        #Bearish Spreads
        #Buy a Put - Bearish (Down)
        #Call Credit Spread - Bearish (Stay same or Down) - Selling a Call(lower strike price)(Short Leg) and Buying a Call (higher strike price)(Long Leg)
        #Put Debit Spread - Bearish (Down) - Buying a Put(higher strike price) and Selling a Put(lower strike price)
        self.web_session.get('https://www.optionsprofitcalculator.com/calculator/covered-call.html')
        #cookie_obj = requests.cookies.create_cookie(domain='https://www.optionsprofitcalculator.com',name='COOKIE_NAME',value='the cookie works')
        #s.cookies.set_cookie(cookie_obj)
        self.base_url = "https://www.optionsprofitcalculator.com/ajax"
        self.base_getStockPrice = "https://www.optionsprofitcalculator.com/ajax/getStockPrice?"
        self.base_getOptionPrice = "https://www.optionsprofitcalculator.com/ajax/getOptions?"
        self.base_calculate = "/calculate?"
        #Basic
        self.covered_call = 'https://www.optionsprofitcalculator.com/calculator/covered-call.html'
        #https://www.optionsprofitcalculator.com/ajax/calculate?underlying-symbol=F&underlying-curPrice=9.305&underlying-act=buy&underlying-price=9.305&underlying-num=1&option-act=buy&option-price=4.80&option-curPrice=4.80&option-num=1&option-opType=c&option-expiry=2020-01-03&option-strike=4.50&option-iv=(auto)&agree_tc=1&graph-priceMin=&graph-priceMax=&graph-type=roiRisk&graph-date=(today)&tabId=6&reqId=3
        self.naked_call = 'https://www.optionsprofitcalculator.com/calculator/short-call.html' #bearish
        self.long_call = 'https://www.optionsprofitcalculator.com/calculator/long-call.html'   #bullish
        self.naked_put = 'https://www.optionsprofitcalculator.com/calculator/short-put.html'   #bullish
        self.long_put = 'https://www.optionsprofitcalculator.com/calculator/long-put.html'     #bearish
        #Spread
        self.credit_spread = 'https://www.optionsprofitcalculator.com/calculator/credit-spread.html'
        self.call_spread = 'https://www.optionsprofitcalculator.com/calculator/call-spread.html'
        self.put_spread = 'https://www.optionsprofitcalculator.com/calculator/put-spread.html'
        self.calendar_spread = 'https://www.optionsprofitcalculator.com/calculator/calendar-spread.html'
        #Advanced
        self.butterfly = 'https://www.optionsprofitcalculator.com/calculator/butterfly.html'
        self.collar = 'https://www.optionsprofitcalculator.com/calculator/collar.html'
        self.diagonal_spread = 'https://www.optionsprofitcalculator.com/calculator/diagonal-spread.html'
        self.double_diag = 'https://www.optionsprofitcalculator.com/calculator/double-diagonal-spread.html'
        self.iron_condor = 'https://www.optionsprofitcalculator.com/calculator/iron-condor.html'
        self.straddle = 'https://www.optionsprofitcalculator.com/calculator/straddle.html'
        self.strangle = 'https://www.optionsprofitcalculator.com/calculator/strangle.html'
        self.covered_strangle = 'https://www.optionsprofitcalculator.com/calculator/covered_strangle.html'
        #Custom
        self.sixLegs = ""
        self.fiveLegs = ""
        self.fourLegs = ""
        self.threeLegs = ""
        self.twoLegs = ""
        #State Parameters
        self.reqID = 1
        self.underlying_symbol = ""
        self.underlying_curPrice = 0
        self.underlying_act = ""
        self.underlying_price = 0
        self.underlying_num = 0
        self.option_act = ""
        self.option_price = 0
        self.option_curPrice = 0
        self.option_num = 0
        self.option_opType = ""
        self.option_expiry = ""
        self.option_strike = 0
        self.option_iv = "(auto)"
        self.option_long_act = ""
        self.option_long_price = 0
        self.option_long_curPrice = 0
        self.option_long_num = 0
        self.option_long_opType = "" 
        self.option_long_expiry = ""
        self.option_long_strike = 0
        self.option_long_iv = "(auto)"
        self.option_short_act = ""
        self.option_short_price = 0
        self.option_short_curPrice = 0
        self.option_short_num = 0
        self.option_short_opType = "" 
        self.option_short_expiry = ""
        self.option_short_strike = 0
        self.option_short_iv = "(auto)"
        self.agree_tc = 1
        self.graph_priceMin = ""
        self.graph_priceMax = ""
        self.graph_type = "roiRisk"
        self.graph_date = "(today)"
        self.tabID = 1
        self.option_prices = []
        self.option_curPrices = []
        self.option_expiries = []
        self.option_strikes = []
        self.option_opTypes = []
        
    
    def getStockPrice(self, stock = "F", act = "buy", num = 1, reqID = -1):
        r = self.web_session.get(url = self.base_getStockPrice + "stock=" + stock + "&reqId=" + str(self.reqID))
        rjson = r.json()
        self.underlying_symbol = stock
        self.underlying_price = rjson["price"]["last"]
        self.underlying_act = act
        self.underlying_num = num
        self.reqID = self.reqID + 1
        return r.json()
    def getOptionsDates(self, stock = "F"):
    	self.getOptionsPrice(stock)
    	return self.option_expiries
    def getOptionsStrikePrices(self, stock = "F"):
    	self.getOptionsPrice(stock)
    	return self.option_strikes
    def getOptionsPrice(self, stock = "F", optionAct = "buy", reqID = -1):
        r = self.web_session.get(url = self.base_getOptionPrice +"stock=" + stock + "&reqId=" + str(self.reqID))
        rjson = r.json()
        self.option_act = optionAct
        self.option_prices = rjson
        self.option_curPrices = rjson
        #self.option_num = 
        self.option_opTypes = ['c','p']
        self.option_expiries = list(rjson['options'].keys())
        self.option_expiries = self.option_expiries[:-1]
        #print(self.option_opTypes)
        #print(self.option_expiries)
        self.option_strikes = list(rjson['options'][self.option_expiries[0]][self.option_opTypes[0]].keys())
        #self.option_iv = 
        self.reqID = self.reqID + 1
        return r.json()
    def getCoveredCall(self, stock = "F", stockAction = "buy", numOptions = 1, optionAction = "buy", optionType = "c", reqID = -1):
        self.getStockPrice(stock = stock, act = stockAction, num = numOptions)
        self.getOptionsPrice(stock = stock, optionAct = optionAction)
        self.option_act = optionAction
        self.option_num = numOptions
        self.option_opType = optionType
        self.option_expiry = self.option_expiries[0]
        self.option_strike = self.option_strikes[0]
        self.option_price = self.option_prices['options'][self.option_expiry][self.option_opType][self.option_strike]['a']
        self.option_curPrice = self.option_prices['options'][self.option_expiry][self.option_opType][self.option_strike]['a']
        r = self.web_session.get(url = self.formCoveredCall())
        self.reqID = self.reqID + 1
        return r.json()
        
    def getCallCreditSpread(self, stock = "F", expiry_date = "2020-01-03", long_strike = 4.00, short_strike = 3.00,num = 1):
        self.getStockPrice(stock = stock)
        self.getOptionsPrice(stock = stock)
        self.option_long_act = "buy"
        self.option_short_act = "sell"
        self.option_long_opType = "c"
        self.option_short_opType = "c"
        
        if long_strike < short_strike:
            return "Incorrect Strike Price for Call Credit Spread"
        #"{:.2f}".format(5)
        self.option_long_price = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_curPrice = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_num = num 
        self.option_long_expiry = expiry_date
        self.option_long_strike = long_strike
        self.option_long_iv = "(auto)"
        self.option_short_price = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_curPrice = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_num = num 
        self.option_short_expiry = expiry_date
        self.option_short_strike = short_strike
        self.option_short_iv = "(auto)"
        
        self.web_session.get(url = self.credit_spread)
        r = self.web_session.get(url = self.formCallCreditSpread())
        return r.json()
    
    
    def getCallDebitSpread(self, stock = "F", expiry_date = "2020-01-03", long_strike = 4.00, short_strike = 3.00,num = 1):
        self.getStockPrice(stock = stock)
        self.getOptionsPrice(stock = stock)
        self.option_long_act = "sell"
        self.option_short_act = "buy"
        self.option_long_opType = "c"
        self.option_short_opType = "c"
        
        if long_strike < short_strike:
            return "Incorrect Strike Price for Call Debit Spread"
        #"{:.2f}".format(5)
        self.option_long_price = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_curPrice = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_num = num 
        self.option_long_expiry = expiry_date
        self.option_long_strike = long_strike
        self.option_long_iv = "(auto)"
        self.option_short_price = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_curPrice = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_num = num 
        self.option_short_expiry = expiry_date
        self.option_short_strike = short_strike
        self.option_short_iv = "(auto)"
        
        self.web_session.get(url = self.credit_spread)
        r = self.web_session.get(url = self.formCallCreditSpread())
        return r.json()
    def getPutCreditSpread(self, stock = "F", expiry_date = "2020-01-03", long_strike = 4.00, short_strike = 3.00,num = 1):
        self.getStockPrice(stock = stock)
        self.getOptionsPrice(stock = stock)
        self.option_long_act = "buy"
        self.option_short_act = "sell"
        self.option_long_opType = "p"
        self.option_short_opType = "p"
        
        if long_strike < short_strike:
            return "Incorrect Strike Price for Put Credit Spread"
        #"{:.2f}".format(5)
        self.option_long_price = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_curPrice = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_num = num 
        self.option_long_expiry = expiry_date
        self.option_long_strike = long_strike
        self.option_long_iv = "(auto)"
        self.option_short_price = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_curPrice = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_num = num 
        self.option_short_expiry = expiry_date
        self.option_short_strike = short_strike
        self.option_short_iv = "(auto)"
        
        self.web_session.get(url = self.credit_spread)
        r = self.web_session.get(url = self.formCallCreditSpread())
        return r.json()
    def getPutDebitSpread(self, stock = "F", expiry_date = "2020-01-03", long_strike = 4.00, short_strike = 3.00,num = 1):
        self.getStockPrice(stock = stock)
        self.getOptionsPrice(stock = stock)
        self.option_long_act = "sell"
        self.option_short_act = "buy"
        self.option_long_opType = "p"
        self.option_short_opType = "p"
        
        if long_strike < short_strike:
            return "Incorrect Strike Price for Put Debit Spread"
        #"{:.2f}".format(5)
        self.option_long_price = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_curPrice = self.option_prices['options'][expiry_date][self.option_long_opType]["{:.2f}".format(long_strike)]['a']
        self.option_long_num = num 
        self.option_long_expiry = expiry_date
        self.option_long_strike = long_strike
        self.option_long_iv = "(auto)"
        self.option_short_price = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_curPrice = self.option_prices['options'][expiry_date][self.option_short_opType]["{:.2f}".format(short_strike)]['a']
        self.option_short_num = num 
        self.option_short_expiry = expiry_date
        self.option_short_strike = short_strike
        self.option_short_iv = "(auto)"
        
        self.web_session.get(url = self.credit_spread)
        r = self.web_session.get(url = self.formCallCreditSpread())
        return r.json()
    def formCoveredCall(self):
        self.formedRequest = (self.base_url + 
            self.base_calculate + 
            "underlying-symbol=" + self.underlying_symbol + 
            "&underlying-curPrice=" + str(self.underlying_price) + 
            "&underlying-act=" + self.underlying_act + 
            "&underlying_price=" + str(self.underlying_price) + 
            "&underlying-num=" + str(self.underlying_num) + 
            "&option-act=" + self.option_act + 
            "&option-price=" + str(self.option_price) + 
            "&option-curPrice=" + str(self.option_curPrice) + 
            "&option-num=" + str(self.option_num) + 
            "&option-opType=" + self.option_opType + 
            "&option-expiry=" + self.option_expiry + 
            "&option-strike=" + self.option_strike + 
            "&option-iv=" + self.option_iv + 
            "&agree_tc=" + str(self.agree_tc) + 
            "&graph-priceMin=" + self.graph_priceMin + 
            "&graph-priceMax=" + self.graph_priceMax + 
            "&graph-type=" + self.graph_type + 
            "&graph-date=" + self.graph_date + 
            "&tabId=" + str(self.tabID) + 
            "&reqId=" + str(self.reqID)
            )
        return self.formedRequest
        #https://www.optionsprofitcalculator.com/ajax/calculate?underlying-symbol=F&underlying-curPrice=9.305&underlying-act=buy&underlying-price=9.305&underlying-num=1&option-act=buy&option-price=4.80&option-curPrice=4.80&option-num=1&option-opType=c&option-expiry=2020-01-03&option-strike=4.50&option-iv=(auto)&agree_tc=1&graph-priceMin=&graph-priceMax=&graph-type=roiRisk&graph-date=(today)&tabId=6&reqId=3 
#    def formRequest(self,requestType = "coveredCall"):
    def formCallCreditSpread(self):
        temp = self.formSpread()
        self.tabID = self.tabID +1
        self.reqID = self.reqID +1
        return temp
    def formCallDebitSpread(self):
        temp = self.formSpread()
        self.tabID = self.tabID +1
        self.reqID = self.reqID +1
        return temp
    def formPutCreditSpread(self):
        temp = self.formSpread()
        self.tabID = self.tabID +1
        self.reqID = self.reqID +1
        return temp
    def formPutDebitSpread(self):
        temp = self.formSpread()
        self.tabID = self.tabID +1
        self.reqID = self.reqID +1
        return temp
        
    
    def formSpread(self):
        self.formedRequest = (self.base_url +
            self.base_calculate + 
            "underlying-symbol=" + self.underlying_symbol + 
            "&underlying-curPrice=" + str(self.underlying_price) + 
            "&long-act=" + self.option_long_act +
            "&long-price=" + str(self.option_long_price) +
            "&long-curPrice=" + str(self.option_long_curPrice) +
            "&long-num=" + str(self.option_long_num) + 
            "&long-opType=" + self.option_long_opType + 
            "&long-expiry=" + self.option_long_expiry + 
            "&long-strike=" + str(self.option_long_strike) +
            "&long-iv=" + self.option_long_iv +
            "&short-act=" + self.option_short_act +
            "&short-price=" + str(self.option_short_price) +
            "&short-curPrice=" + str(self.option_short_curPrice) +
            "&short-num=" + str(self.option_short_num) + 
            "&short-opType=" + self.option_short_opType + 
            "&short-expiry=" + self.option_short_expiry + 
            "&short-strike=" + str(self.option_short_strike) +
            "&short-iv=" + self.option_short_iv +
            "&agree_tc=" + str(self.agree_tc) + 
            "&graph-priceMin=" + self.graph_priceMin + 
            "&graph-priceMax=" + self.graph_priceMax + 
            "&graph-type=" + self.graph_type + 
            "&graph-date=" + self.graph_date + 
            "&tabId=" + str(self.tabID) + 
            "&reqId=" + str(self.reqID)
            )
        return self.formedRequest
        
        #https://www.optionsprofitcalculator.com/ajax/calculate?
        #underlying-symbol=F&underlying-curPrice=9.21&long-act=buy&long-price=5.25&long-curPrice=5.25&long-num=1&
        #long-opType=c&long-expiry=2020-01-10&long-strike=4.00&long-iv=(auto)&short-act=sell&short-price=2.67&short-curPrice=2.67&
        #short-num=1&short-opType=c&short-expiry=2020-01-10&short-strike=6.50&short-iv=(auto)&graph-priceMin=&graph-priceMax=&graph-type=roiRisk&graph-date=(today)&tabId=29&reqId=22
