import matplotlib.pyplot as plt
import seaborn as sns

class Plot():

    def __init__(self):
        self.plt = plt
        self.sns = sns

    def stripplot_bairro(self,df, var_name):
        """
        Gera um strip plot com os dados de uma variável específica em relação aos bairros.

        Parâmetros:
            df (DataFrame): O DataFrame contendo os dados.
            var_name (str): O nome da variável a ser plotada.

        Retorna:
            matplotlib.axes._subplots.AxesSubplot: O objeto do subplot do strip plot.
        """
        order = df[["crawler", var_name]].groupby("crawler").mean().sort_values(by=var_name).index
        plt.figure(figsize=(10,10))
        return self.sns.stripplot(data=df, 
                            x=var_name, y="crawler", 
                            order=order)

    def boxplot_crawler(self,df, var_name):
        """
        Gera um box plot com os dados de uma variável específica em relação aos bairros.

        Parâmetros:
            df (DataFrame): O DataFrame contendo os dados.
            var_name (str): O nome da variável a ser plotada.

        Retorna:
            matplotlib.axes._subplots.AxesSubplot: O objeto do subplot do box plot.

        """
        order = df[["crawler", var_name]].groupby("crawler").mean().sort_values(by=var_name).index
        plt.figure(figsize=(10, 10))
        return self.sns.boxplot(data=df,
                        x=var_name, y="crawler",
                        order=order)
