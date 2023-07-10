import pandas as pd
from utils.clean import Clean

clean = Clean()


# Extract

df = pd.read_csv('./data/raw/imoveis.csv')

# Transform

df = clean.cleancode(df)

# Load
df.to_csv('./data/trusted/imoveis.csv')