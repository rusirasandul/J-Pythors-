import matplotlib.pyplot as plt

# Vehicle Make Distribution
vehicles_df['Vehicle Make'].value_counts().head(10).plot(kind='bar', title='Top 10 Vehicle Makes')
plt.show()
