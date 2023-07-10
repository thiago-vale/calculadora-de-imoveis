import pandas as pd
from utils.clean import Clean

clean = Clean()


# Extract

df = pd.read_csv('./data/trusted/imoveis.csv')

# Transform

coluna = "preço"
df = clean.remove_outliers_bairro(df,coluna,0.20)

coluna = "condominio"
df = clean.remove_outliers_bairro(df,coluna,0.20)

# Load
df.to_csv('./data/refined/imoveis.csv')