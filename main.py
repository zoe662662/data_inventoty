import pandas as pd
from dataReader import read_csv
from dataAnalyzer import analyze_columns
from dataExporter import output_html


def do_inventory(source, output):

    df = read_csv(source)

    # transform data
    df['regist_date'] = pd.to_datetime(df['regist_date'], errors='coerce')
    df = df.astype({'cnts_of_main': int, 'total_prem': 'float'})
    # output html
    s = analyze_columns(df)
    output_html(s, output)


if __name__ == "__main__":
    data_source = './a2cef438-fd90-4974-8ef8-1db8babd7e37.csv'
    output_file = './test2.html'
    do_inventory(data_source, output_file)


