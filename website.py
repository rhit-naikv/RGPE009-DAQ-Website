from numpy import int64
import pandas as pd
import matplotlib.pyplot as plt
import math

#CLASSES
class Message500:
    def __init__(self, df):
        self.df = df[df['ID'] == '500'].copy()
        self.df['START'] = self.df['B0'].apply(lambda x: x[1]).apply(lambda x: int(x, 2))
        self.df['STOP'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['ESTOP'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['Rotary Position Switch'] = self.df['B0'].apply(lambda x: x[4 : 8]).apply(lambda x: int(x, 2))

class Message504:
    def __init__(self, df):
        self.df = df[df['ID'] == '504'].copy()
        self.df['ARBR Down'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['ARBR Up'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['ARBF Down'] = self.df['B0'].apply(lambda x: x[4]).apply(lambda x: int(x, 2))
        self.df['ARBF Up'] = self.df['B0'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Shift Down'] = self.df['B0'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Shift Up'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Clutch Potentiometer'] = (self.df['B2'].apply(lambda x: x[4:8]) + self.df['B1']).apply(lambda x: int(x, 2))
        self.df['CallFlag'] = self.df['B2'] = self.df['B2'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))

class Message508:
    def __init__(self, df):
        self.df = df[df['ID'] == '508'].copy()
        self.df['Engine RPM'] = (self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['TPS'] = (self.df['B3'] + self.df['B2']).apply(lambda x: int(x, 2))
        self.df['Shiftcut'] = self.df['B4'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Brake Light'] = self.df['B4'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Neutral'] = self.df['B4'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message509:
    def __init__(self, df):
        self.df = df[df['ID'] == '509'].copy()
        self.df['MAP'] = (self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['AFR'] = (self.df['B3'] + self.df['B2']).apply(lambda x: int(x, 2))
        self.df['Fuel Pressure'] = (self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message50C:
    def __init__(self, df):
        self.df = df[df['ID'] == '50C'].copy()
        self.df['Brake Pressure'] = (self.df['B1'].apply(lambda x: x[4:8]) + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Pressed'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message50D:
    def __init__(self, df):
        self.df = df[df['ID'] == '50D'].copy()
        self.df['Accel X'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Accel Y'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))


#FUNCTIONS

def hex_to_binary(my_hexdata):
    scale = 16 ## equals to hexadecimal
    num_of_bits = 8
#     print(my_hexdata)
    return bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
#   Taken from this StackOverflow post: https://stackoverflow.com/questions/1425493/convert-hex-to-binary

def preprocessData(fileName):
    df = pd.read_csv(fileName)

    df = df.set_index('Millis')

    df = df.fillna('0')

    df['B0'] = df['B0'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B1'] = df['B1'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B2'] = df['B2'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')    
    df['B3'] = df['B3'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B4'] = df['B4'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B5'] = df['B5'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B6'] = df['B6'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')
    df['B7'] = df['B7'].apply(lambda x: int(float(x)) if isinstance(x, float) else x).astype('object')

    for k in range(len(df.columns.values)):
        new_col = df.columns.values[k].strip()
        old_col = df.columns.values[k]
        df[new_col] = df[old_col]
        df.drop(old_col, axis=1)

    df.loc[:,['B0','B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']] = df.loc[:,['B0','B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']].applymap(str).applymap(hex_to_binary)
    
    return df


df = preprocessData('log01.csv')
