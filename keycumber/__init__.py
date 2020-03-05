import pandas as pd

destinations = pd.read_csv('data/destinations.csv')
modifiers = pd.read_csv('data/modifiers.csv')

index = pd.MultiIndex.from_product([destinations.destination.tolist(), modifiers.kw.tolist()], names=['destinations', 'modifiers'])
df = pd.DataFrame(index=index).reset_index()
df['output_1'] = df.destinations + ' ' + df.modifiers
df['output_2'] = df.modifiers + ' ' + df.destinations

# TODO: only one column, batch by 700 rows maximum
df[['output_1', 'output_2']].to_csv('data/output.csv', index=False)
