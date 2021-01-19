from pandas import read_csv,read_excel,read_table, DataFrame

class Reader(object):
    def __init__(self,path,filename):
        ext = filename.split(".")[-1]
        self.path = path
        self.filename = filename
        self.extensions = ["csv", "txt"]
        if ext.lower() == "csv":
            self.df = read_csv(path)
        elif ext.lower() == "txt":
            self.df = read_table(path)
        else:
            raise Warning("Solo se admiten las extensiones " + ",".join(self.extensions))

    def get_head(self):
        return self.df.head()
    
    def get_columns(self):
        return list(self.df.columns.values)

    def get_supported_ext(self):
        return self.extensions

    def get_df_len(self):
        return len(self.df.index)

    def topytorch(self):
        columns = list(self.df.columns.values)
        output_df = self.df.rename(columns={columns[0]: "review"})
        return output_df