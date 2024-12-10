import matplotlib.pyplot as plt

import pandas as pd

vehicles_df = pd.read_csv("vehicles_cleaned.csv")

vehicles_df['Vehicle Make'].value_counts().head(10).plot(kind='bar', title='Top 10 Vehicle Makes')
plt.show()
