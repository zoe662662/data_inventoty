import pandas as pd
from .dataReader import read_csv
from .dataAnalyzer import analyze_columns
from .dataExporter import output_html
from .dataTransformer import transfrom_dtype

def do_inventory(source, output):

    df = read_csv(source)

    # transform data
    df['regist_date'] = pd.to_datetime(df['regist_date'], errors='coerce')
    df = df.astype({'cnts_of_main': int, 'total_prem': 'float'})
    # output html
    s = analyze_columns(df)
    output_html(s, output)
