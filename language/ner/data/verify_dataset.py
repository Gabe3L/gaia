import pandas as pd

df = pd.read_csv("language/ner/data/music.csv")

print(df[df['labels'].isna()])