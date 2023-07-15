import pandas as pd
import numpy as np



class Clean():

    def __init__(self):
        pass

    def iqr(self,df):
        """
        Calcula o intervalo interquartil (IQR) e identifica outliers em um DataFrame.

        Parâmetros:
            df (DataFrame): O DataFrame contendo os dados para análise.

        Retorna:
            tuple: Uma tupla contendo os limites inferior e superior do intervalo interquartil (lower_bound, upper_bound)
            float: A porcentagem de outliers presentes nos dados.
        """
        q1,q3 = df.quantile([.25 , .75])
        iqr= q3-q1
        lower_bound= q1 - 1.5*iqr
        upper_bound= q3 + 1.5*iqr
        pct_outliers = sum(~df.between(lower_bound, upper_bound))/len(df)
        return lower_bound , upper_bound, round(pct_outliers,2)
    

    def percentiles(self,df, percentiles_levels=0.1):
        """
        Calcula os percentis e identifica outliers em um DataFrame.

        Parâmetros:
            df (DataFrame): O DataFrame contendo os dados para análise.
            percentiles_levels (float or list): Níveis dos percentis a serem calculados. Pode ser um valor único ou uma lista de valores.

        Retorna:
            tuple: Uma tupla contendo os limites inferior e superior dos percentis (lower_bound, upper_bound).
            float: A porcentagem de outliers presentes nos dados.
        """
        lower_bound, upper_bound = df.quantile([percentiles_levels, 1-percentiles_levels])
        pct_outliers = sum(~df.between(lower_bound, upper_bound))/len(df)
        return lower_bound, upper_bound, round(pct_outliers,2)
    
    def cleancode(self,df):
        """
        Realiza um processo de limpeza e transformação dos dados em um DataFrame.

        Parâmetros:
            df (DataFrame): O DataFrame contendo os dados a serem limpos e transformados.

        Retorna:
            DataFrame: O DataFrame resultante após o processo de limpeza e transformação dos dados.
        """
        df = df.drop_duplicates(keep="first", subset=[coluna for coluna in df.columns if coluna!="crawled_at"]).reset_index(drop=True)
        filtro_de_anuncios = [str(_id).isnumeric() for _id in df["id"]]
        df = df[filtro_de_anuncios].reset_index(drop=True)
        df["Quarto"] = (df["rooms"].str.split(" ").str[0].str.replace("--","0").astype(int))
        df["Banheiro"] = (df["bathrooms"].str.split(" ").str[0].str.replace("--","0").astype(int))
        df["Garagem"] = (df["garages"].str.split(" ").str[0].str.replace("--","0").astype(int))
        df["condo"] = df["condo"].fillna("MISSING")
        df["condominio"] = [int(w.split("R$ ")[1].replace(".","")) if w!="MISSING" else np.nan for w in df["condo"]]
        df["preço"] = [int(w.split("R$ ")[1].split(" /")[0].split("\n")[0].replace(".","")) for w in df["price"]]
        df["area_limpo"] = df["area"].astype(int)
        df["crawled_at"] = pd.to_datetime(df["crawled_at"], format="%Y-%m-%d %H:%M")
        df = df.drop(columns = ["area", "rooms", "bathrooms", "garages", "price", "condo"])
        df["bairro"] = (df["address"].str.split("- ").str[1].str.split(",").str[0])
        df.loc[df["bairro"].isin(["RJ"]), "bairro"] = (df.loc[df["bairro"].isin(["RJ"]), "address"].str.split(",").str[0])
        df.loc[df["crawler"]!=df["bairro"],"bairro"].unique()
        df["crawler"] = (df["crawler"].str.lower().str.replace(" ","_"))
        df["bairro"] = (df["bairro"].str.lower().str.replace(" ","_").str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8"))
        df = df.drop(columns="bairro")
        df["amenities"] = df["amenities"].str.split("\n")
        df["amenities"] = df["amenities"].fillna("")
        amenities = []
        for am in df["amenities"]:
            if am != "":
                amenities = amenities + am
        unico_amenities = list(set(amenities))
        df["amenities"] = df["amenities"].str.join(", ")
        for amenity in unico_amenities:
            print(amenity)
            df[amenity]=0
            df.loc[df["amenities"].str.contains(amenity), amenity] = 1
        return df
    
    def remove_outliers_bairro(self,df,coluna,percent_outliers):
        """
        Remove outliers em uma coluna específica para cada bairro presente no DataFrame.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame contendo os dados.
            coluna (str): O nome da coluna em que os outliers serão removidos.
            percent_outliers (float): A porcentagem máxima permitida de outliers.

        Retorna:
            pandas.DataFrame: O DataFrame resultante após a remoção dos outliers.
            """
        for bairro in df["crawler"].unique(): # Loop pelos bairros únicos presentes no DataFrame
            metodo = "iqr"  # Método inicialmente definido como "iqr"
            
            # Cálculo dos limites e porcentagem de outliers usando o método IQR
            lower_bound, upper_bound, pct_outliers = self.iqr(df.loc[df["crawler"]==bairro, coluna])
            print(f'{bairro},{pct_outliers}')  # Imprime o bairro e a porcentagem de outliers
            if pct_outliers > percent_outliers:  # Verifica se a porcentagem de outliers é maior que 10%
                metodo = "percentile"  # Método alterado para "percentile"
                lower_bound, upper_bound, pct_outliers = self.percentiles(df.loc[df["crawler"]==bairro, coluna]) # Cálculo dos limites e porcentagem de outliers usando o método "percentile"
                print(f"Coluna: {coluna}, bairro: {bairro}, metodo: {metodo}, pct_outliers: {pct_outliers}") # Impressão das informações sobre o método e porcentagem de outliers
                df.loc[(df["crawler"]==bairro) & (~df[coluna].between(lower_bound, upper_bound)), coluna] = np.nan # Remoção dos outliers com base nos limites calculados pelo método "percentile"
        return df