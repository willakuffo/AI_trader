from datetime import datetime
import MetaTrader5 as mt5
import pytz
import pandas as pd
import pickle 
import os 
from colorama import Fore,Style
import numpy as np


class dataEngine:
    def __init__(self):
        pd.set_option('display.max_columns', 500) # number of columns to be displayed
        pd.set_option('display.width', 1500)      # max table width to display
        # set time zone to UTC
        self.timezone = pytz.timezone("Etc/UTC")
        self.start_date =  datetime(2020, 1, 10, tzinfo=self.timezone)
        self.to_date = datetime(datetime.today().year, 
            datetime.today().month,
            datetime.today().day-1, tzinfo=self.timezone)


        
    def getHistoricalData(self,symbol):
        print(Fore.YELLOW+'Getting Historical data on symbol:', symbol)
        # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
        ticks = None
        try:
            ticks = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M10, self.start_date, self.to_date)
            print(Fore.BLUE+"Ticks received:",len(ticks))
            # shut down connection to the MetaTrader 5 terminal
        except TypeError:
            print(Fore.RED+'failed to get data on symbol:',symbol,'with error:',mt5.last_error())
            print(Style.RESET_ALL)
            os.system('taskkill /f /im terminal64.exe')

            exit()
        mt5.shutdown()
        # display data on each tick on a new line
        print("Display obtained ticks 'as is'")
        #count = 0
        #for tick in ticks:
        #    count+=1
        #    print(tick)
        #    if count >= 10:
        #        break
        # create DataFrame out of the obtained data
        ticks_frame = pd.DataFrame(ticks)
        # convert time in seconds into the datetime format
        ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
        # display data
        print("\nDisplay dataframe with ticks")
        print(ticks_frame.head,ticks_frame.shape) 
        print(ticks_frame.info())
        return ticks_frame

    def save_locally(self,data,filename):
        filename = filename+'-'+str(self.to_date).split()[0]
        print(Fore.YELLOW+'Saving data to: ',os.path.join(os.getcwd(),filename))
        with open(filename+'.pickle','wb') as f:
            pickle.dump(data,f)
            f.close()
        #data.to_csv(filename+'.csv',index = True)
        print(Fore.GREEN+'Done!')
        