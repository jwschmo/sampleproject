from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.opt import ibConnection, message
import time

def watcher(msg):
    print(msg)

def contractDetailsHandler(msg):
    contracts.append(msg.contractDetails.m_summary)

def contractDetailsEndHandler(msg):
    global DataWait
    DataWait =  False

con = ibConnection()
con.registerAll(watcher)
con.register(contractDetailsHandler, 'ContractDetails')
con.register(contractDetailsEndHandler, 'ContractDetailsEnd')

con.connect()

contract = Contract()
contract.m_exchange     = "SMART"
contract.m_secType      =  "OPT"
contract.m_symbol       = "VTR"
#contract.m_multiplier   = "100"
contract.m_currency     = "USD"


con.reqContractDetails(1, contract)

contracts = [] # to store all the contracts

DataWait = True  ;  i = 0
while DataWait and i < 90:
    i += 1 ; print(i),
    time.sleep(1)

con.disconnect()
con.close()

print(contracts)