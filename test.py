import pandas as pd
import numpy as np
df = pd.DataFrame(columns=['id', 'id_validator'], data=np.random.randn(3, 2))
# df.set_index('id', inplace=True)
# df.append([1, 2])
df.to_csv('test2.csv')