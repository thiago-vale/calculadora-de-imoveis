import matplotlib.pyplot as plt
import seaborn as sns

class Plot():

    def __init__(self):
        self.plt = plt
        self.sns = sns

    def plot_stripplot(self,df, var_name):
        order = df[["crawler", var_name]].groupby("crawler").mean().sort_values(by=var_name).index
        plt.figure(figsize=(10,10))
        return self.sns.stripplot(data=df, 
                            x=var_name, y="crawler", 
                            order=order)

    def boxplot_crawler(self,df, var_name):
        order = df[["crawler", var_name]].groupby("crawler").mean().sort_values(by=var_name).index
        plt.figure(figsize=(10, 10))
        return self.sns.boxplot(data=df,
                        x=var_name, y="crawler",
                        order=order)
