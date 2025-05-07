import pandas as pd

df = pd.read_csv("language/ner/data/val.csv")

print(df[df['labels'].isna()])