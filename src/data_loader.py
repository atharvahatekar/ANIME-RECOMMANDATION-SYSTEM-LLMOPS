import pandas as pd

class AnimeDataLoader:
    def __init__(self, original_csv:str, processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()
        required_columns = {'Name', 'Genres','synopsis'}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        df["combined_info"] = (
            'title:' + df["Name"] + "Overview: " + df["synopsis"] + "Genres: " + df["Genres"]
        )

        df[["combined_info"]].to_csv(self.processed_csv, index=False, encoding='utf-8')
        
        return self.processed_csv