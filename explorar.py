import pandas as pd
from pathlib import Path

for arquivo in sorted(Path("dados").glob("*.csv")):
    df = pd.read_csv(arquivo)
    print(f"\n=== {arquivo.name} ===")
    print(f"Linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")