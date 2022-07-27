import pandas as pd
import numpy as np

pd.MultiIndex.from_tuples([('basic', 'id'), ('basic', 'id_validator'), ('basic', 'price'), ('spec', 'core'), ('spec', 'clock')])
df = pd.DataFrame(columns=['id', 'id_validator'], data=np.random.randn(3, 2))
df.set_index('id', inplace=True)

print(df)
df.columns = pd.MultiIndex.from_product([['basic'], df.columns])
df[('basic', 'price')] = np.NaN
a = df.iloc[2].name
df.loc[a, ('basic', 'asdf')] = 1

for k, v in df.iterrows():
    v[('basic', 'price')] = 30

print(df.loc[df[('basic', 'id_validator')] < 0])