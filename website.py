from numpy import int64
import pandas as pd
import matplotlib.pyplot as plt
import math

#CLASSES
class Message:
    def __init__(self, df, id):
        self.df = df[df['ID'] == id].copy()
    def plot(self):
        try:
            pt = pd.pivot_table(self.df, values=self.df.columns.drop('ID').drop('B0').drop('B1').drop('B2').drop('B3').drop('B4').drop('B5').drop('B6').drop('B7'), index='Millis')
            plt.axes(pt.plot())
            plt.show()
        except(TypeError):
            print("This message doesn't have any data")

class Message500(Message):
    def __init__(self, df):
        Message.__init__(self, df, '500')
        self.df['START'] = self.df['B0'].apply(lambda x: x[1]).apply(lambda x: int(x, 2))
        self.df['STOP'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['ESTOP'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['Rotary Position Switch'] = self.df['B0'].apply(lambda x: x[4 : 8]).apply(lambda x: int(x, 2))

class Message504(Message):
    def __init__(self, df):
        Message.__init__(self, df, '504')
        self.df['ARBR Down'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['ARBR Up'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['ARBF Down'] = self.df['B0'].apply(lambda x: x[4]).apply(lambda x: int(x, 2))
        self.df['ARBF Up'] = self.df['B0'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Shift Down'] = self.df['B0'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Shift Up'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Clutch Potentiometer'] = (self.df['B2'].apply(lambda x: x[4:8]) + self.df['B1']).apply(lambda x: int(x, 2))
        self.df['CallFlag'] = self.df['B2'] = self.df['B2'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))

class Message508(Message):
    def __init__(self, df):
        Message.__init__(self, df, '508')
        self.df['Engine RPM'] = (self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['TPS'] = (self.df['B3'] + self.df['B2']).apply(lambda x: int(x, 2))
        self.df['Shiftcut'] = self.df['B4'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Brake Light'] = self.df['B4'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Neutral'] = self.df['B4'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message509(Message):
    def __init__(self, df):
        Message.__init__(self, df, '509')
        self.df['MAP'] = (self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['AFR'] = (self.df['B3'] + self.df['B2']).apply(lambda x: int(x, 2))
        self.df['Fuel Pressure'] = (self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message50C(Message):
    def __init__(self, df):
        Message.__init__(self, df, '50C')
        self.df['Brake Pressure'] = (self.df['B1'].apply(lambda x: x[4:8]) + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Pressed'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message50D(Message):
    def __init__(self, df):
        Message.__init__(self, df, '50D')
        self.df['Front Accel X'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Front Accel Y'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message50E(Message):
    def __init__(self, df):
        Message.__init__(self, df, '50E')
        self.df['Front Gyro Roll'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Front Gyro Pitch'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message50F(Message):
    def __init__(self, df):
        Message.__init__(self, df, '50F')
        self.df['Front Gyro Yaw'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Front Accel Z'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message510(Message):
    def __init__(self, df):
        Message.__init__(self, df, '510')
        self.df['Clutch Position'] = (self.df['B1'].apply(lambda x: x[4:8]) + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Disengaged'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message511(Message):
    def __init__(self, df):
        Message.__init__(self, df, '511')
        self.df['Middle Accel X'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Middle Accel Y'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message512(Message):
    def __init__(self, df):
        Message.__init__(self, df, '512')
        self.df['Wheelspeed Front Left'] = (self.df['B0'] + self.df['B1']).apply(lambda x: int(x, 2))
        self.df['Wheelspeed Front Right'] = (self.df['B2'] + self.df['B3']).apply(lambda x: int(x, 2))

class Message513(Message):
    def __init__(self, df):
        Message.__init__(self, df, '513')
        self.df['Wheelspeed Back Left'] = (self.df['B0'] + self.df['B1']).apply(lambda x: int(x, 2))
        self.df['Wheelspeed Back Right'] = (self.df['B2'] + self.df['B3']).apply(lambda x: int(x, 2))

class Message514(Message):
    def __init__(self, df):
        Message.__init__(self, df, '514')
        self.df['Gear Position'] = self.df['B0'].apply(lambda x: int(x, 2))
        self.df['Gear Position Quality Factor'] = self.df['B1'].apply(lambda x: int(x, 2))
        self.df['In progress'] = self.df['B2'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['DOWN'] = self.df['B2'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['UP'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message515(Message):
    def __init__(self, df):
        Message.__init__(self, df, '515')
        self.df['Middle Gyro Roll'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Middle Gyro Pitch'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message516(Message):
    def __init__(self, df):
        Message.__init__(self, df, '516')
        self.df['Middle Gyro Yaw'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Middle Accel Z'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message517(Message):
    def __init__(self, df):
        Message.__init__(self, df, '517')
        self.df['Rear Accel X'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Rear Accel Y'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message518(Message):
    def __init__(self, df):
        Message.__init__(self, df, '518')
        self.df['Front ARB'] = self.df['B0'].apply(lambda x: int(x, 2))

class Message519(Message):
    def __init__(self, df):
        Message.__init__(self, df, '519')
        self.df['Rear Gyro Roll'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Rear Gyro Pitch'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message51A(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51A')
        self.df['Rear Gyro Yaw'] = (self.df['B3'] + self.df['B2'] + self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Rear Accel Z'] = (self.df['B7'] + self.df['B6'] + self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))

class Message51B(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51B')
        self.df['Front Left Tire Temp 1'] = self.df['B0'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 2'] = self.df['B1'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 3'] = self.df['B2'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 4'] = self.df['B3'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 5'] = self.df['B4'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 6'] = self.df['B5'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 7'] = self.df['B6'].apply(lambda x: int(x, 2))
        self.df['Front Left Tire Temp 8'] = self.df['B7'].apply(lambda x: int(x, 2))

class Message51C(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51C')
        self.df['Rear ARB'] = self.df['B0'].apply(lambda x: int(x, 2))

class Message51D(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51D')
        self.df['Front Right Tire Temp 1'] = self.df['B0'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 2'] = self.df['B1'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 3'] = self.df['B2'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 4'] = self.df['B3'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 5'] = self.df['B4'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 6'] = self.df['B5'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 7'] = self.df['B6'].apply(lambda x: int(x, 2))
        self.df['Front Right Tire Temp 8'] = self.df['B7'].apply(lambda x: int(x, 2))

class Message51E(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51E')
        self.df['Rear Left Tire Temp 1'] = self.df['B0'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 2'] = self.df['B1'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 3'] = self.df['B2'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 4'] = self.df['B3'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 5'] = self.df['B4'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 6'] = self.df['B5'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 7'] = self.df['B6'].apply(lambda x: int(x, 2))
        self.df['Rear Left Tire Temp 8'] = self.df['B7'].apply(lambda x: int(x, 2))

class Message51F(Message):
    def __init__(self, df):
        Message.__init__(self, df, '51F')
        self.df['Rear Right Tire Temp 1'] = self.df['B0'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 2'] = self.df['B1'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 3'] = self.df['B2'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 4'] = self.df['B3'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 5'] = self.df['B4'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 6'] = self.df['B5'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 7'] = self.df['B6'].apply(lambda x: int(x, 2))
        self.df['Rear Right Tire Temp 8'] = self.df['B7'].apply(lambda x: int(x, 2))

class Message520(Message):
    def __init__(self, df):
        Message.__init__(self, df, '520')
        self.df['Engine PDM Output Status Ch0 Flags'] = self.df['B0'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch0'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch1 Flags'] = self.df['B1'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch1'] = self.df['B1'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch2 Flags'] = self.df['B2'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch2'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch3 Flags'] = self.df['B3'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch3'] = self.df['B3'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch4 Flags'] = self.df['B4'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch4'] = self.df['B4'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch5 Flags'] = self.df['B5'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch5'] = self.df['B5'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch6 Flags'] = self.df['B6'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch6'] = self.df['B6'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch7 Flags'] = self.df['B7'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Output Status Ch7'] = self.df['B7'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message524(Message):
    def __init__(self, df):
        Message.__init__(self, df, '524')
        self.df['Actuation PDM Output Status Ch0 Flags'] = self.df['B0'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch0'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch1 Flags'] = self.df['B1'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch1'] = self.df['B1'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch2 Flags'] = self.df['B2'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch2'] = self.df['B2'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch3 Flags'] = self.df['B3'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch3'] = self.df['B3'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch4 Flags'] = self.df['B4'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch4'] = self.df['B4'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch5 Flags'] = self.df['B5'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch5'] = self.df['B5'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch6 Flags'] = self.df['B6'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch6'] = self.df['B6'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch7 Flags'] = self.df['B7'].apply(lambda x: x[0:7]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Output Status Ch7'] = self.df['B7'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message528(Message):
    def __init__(self, df):
        Message.__init__(self, df, '528')
        self.df['Engine PDM SWM'] = self.df['B0'].apply(lambda x: x[0]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Rear ARB'] = self.df['B0'].apply(lambda x: x[1]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Front ARB'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['Engine PDM EIM'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Shift'] = self.df['B0'].apply(lambda x: x[4]).apply(lambda x: int(x, 2))
        self.df['Engine PDM Clutch'] = self.df['B0'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Engine PDM A-PDM'] = self.df['B0'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Engine PDM FCM'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))

class Message52C(Message):
    def __init__(self, df):
        Message.__init__(self, df, '52C')
        self.df['Actuation PDM SWM'] = self.df['B0'].apply(lambda x: x[0]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Rear ARB'] = self.df['B0'].apply(lambda x: x[1]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Front ARB'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM EIM'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Shift'] = self.df['B0'].apply(lambda x: x[4]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM Clutch'] = self.df['B0'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM E-PDM'] = self.df['B0'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Actuation PDM FCM'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))   

class Message530(Message):
    def __init__(self, df):
        Message.__init__(self, df, '530')
        self.df['Front Controls SWM'] = self.df['B0'].apply(lambda x: x[0]).apply(lambda x: int(x, 2))
        self.df['Front Controls Rear ARB'] = self.df['B0'].apply(lambda x: x[1]).apply(lambda x: int(x, 2))
        self.df['Front Controls Front ARB'] = self.df['B0'].apply(lambda x: x[2]).apply(lambda x: int(x, 2))
        self.df['Front Controls EIM'] = self.df['B0'].apply(lambda x: x[3]).apply(lambda x: int(x, 2))
        self.df['Front Controls Shift'] = self.df['B0'].apply(lambda x: x[4]).apply(lambda x: int(x, 2))
        self.df['Front Controls Clutch'] = self.df['B0'].apply(lambda x: x[5]).apply(lambda x: int(x, 2))
        self.df['Front Controls A-PDM'] = self.df['B0'].apply(lambda x: x[6]).apply(lambda x: int(x, 2))
        self.df['Front Controls E-PDM'] = self.df['B0'].apply(lambda x: x[7]).apply(lambda x: int(x, 2))  

class Message534(Message):
    def __init__(self, df):
        Message.__init__(self, df, '534')
        self.df['Engine PDM Battery Voltage'] = self.df['B0'].apply(lambda x: int(x, 2))

class Message538(Message):
    def __init__(self, df):
        Message.__init__(self, df, '538')
        self.df['ECU Battery Voltage'] = (self.df['B1'] + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['Coolant Temp'] = (self.df['B3'] + self.df['B2']).apply(lambda x: int(x, 2))
        self.df['Oil Temp'] = (self.df['B5'] + self.df['B4']).apply(lambda x: int(x, 2))
        self.df['Oil Pressure'] = (self.df['B7'] + self.df['B6']).apply(lambda x: int(x, 2))

class Message53C(Message):
    def __init__(self, df):
        Message.__init__(self, df, '53C')
        self.df['BMM Batery Voltage'] = (self.df['B1'].apply(lambda x: x[4:8]) + self.df['B0']).apply(lambda x: int(x, 2))
        self.df['BMM Car Current'] = (self.df['B3'].apply(lambda x: x[4:8]) + self.df['B2']).apply(lambda x: int(x, 2))




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
message = Message538(df)
print(df.columns)
message.plot()