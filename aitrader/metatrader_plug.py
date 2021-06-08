from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import pickle
import os
import DataEngine
from colorama import Fore,Style,Back

class plug:
    def __init__(self):
        #print('\nAI_Trader\n-----------------------\n\Using MetaTrader 5\n-----------------------\n')
        os.system("")#allow coloured terminal
        self.default_server = 'MetaQuotes-Demo'
        self.acc_no = None
        self.password = None

    
    def init_terminal(self):
        print(Fore.YELLOW+'starting MetaTrader5 Terminal...')
        if not mt5.initialize():
            print(Fore.RED+'failed to initialize with error:',mt5.last_error())
            mt5.shutdown()
            os.system('taskkill /f /im terminal64.exe')
            return False
        else:
            print(Fore.GREEN+'MT5 terminal connected successfully!\n')
            print(Style.RESET_ALL)
            print(Back.GREEN+'TERMINAL INFORMATION')   
            print(Style.RESET_ALL)

            for k,v in mt5.terminal_info()._asdict().items():
                print('{:>50}'.format(k),v)

            return True


    def login(self):
        print(Fore.BLUE+'\nlogging in...')
        if mt5.login(self.acc_no,password = self.password,server = self.default_server):
            print(Fore.GREEN+'logged in successfully into acc:',self.acc_no,'on server:',self.default_server)
            print(Style.RESET_ALL)  
            print(Back.GREEN+'ACCOUNT INFORMATION') 
            print(Style.RESET_ALL)
  
            for k,v in mt5.account_info()._asdict().items():
                print('{:>50}'.format(k),v)

        else:print(Fore.RED+'log in failure with error:', mt5.last_error())
        print('\n')

if __name__ == '__main__':
    MP = plug()
    MP.init_terminal()
    MP.acc_no = 46127081
    MP.password = 'iixr2jir'
    MP.login()

    DE = DataEngine.dataEngine()
    AUDUSD = DE.getHistoricalData('EURUSD')
    DE.save_locally(AUDUSD,'EURUSD')
    print(Style.RESET_ALL)