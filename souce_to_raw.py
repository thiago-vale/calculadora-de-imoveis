import pandas as pd
from utils.webscraping import Scraping
from utils.clean import Clean

extract = Scraping()
clean = Clean()

#extract

bairro = ["Bela Vista","Liberdade","Saúde","Ipiranga","Broklin"]
url = [
    "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/bela-vista/apartamento_residencial/",
    "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/liberdade/apartamento_residencial/",
    "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/saude/apartamento_residencial/",
    "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/ipiranga/apartamento_residencial/",
    "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/brooklin/apartamento_residencial/"
]

df_list = []  # Lista para armazenar os DataFrames gerados

for b, u in zip(bairro, url):
    results = extract.extract_apartment_data(b, u, 30)
    df = pd.DataFrame(results)  # Cria um DataFrame a partir dos resultados de cada iteração
    df_list.append(df)  # Adiciona o DataFrame à lista df_list

df= pd.concat(df_list, ignore_index=True)  # Combina os DataFrames usando concat

extract.close()

#tansform


#laod
df.to_csv('./data/raw/imoveis.csv')
