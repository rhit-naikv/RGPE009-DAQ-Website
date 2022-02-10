from numpy import int64
import pandas as pd
import matplotlib.pyplot as plt

# importing the CANLOG09 csv file
df = pd.read_csv('CANLOG09.csv')

df[' B0'] = df[' B0'].apply(int, base=16)
df[' B1'] = df[' B1'].apply(int, base=16)
df[' B2'] = df[' B2'].apply(int, base=16)
df[' B3'] = df[' B3'].apply(int, base=16)
df[' B4'] = df[' B4'].apply(int, base=16)
df[' B5'] = df[' B5'].apply(int, base=16)

b16 = lambda x: int(str(x),16)

df[' B6'] = df[' B6'].apply(b16)
df[' B7'] = df[' B7'].apply(b16)

df = df.set_index('Millis')
print(df.loc[df[' ID'] == '534', ' B0'])
plt.plot(df.loc[df[' ID'] == '534', ' B0'])
plt.ylabel('B0')
plt.xlabel('Milliseconds')
plt.title('534')
plt.show()