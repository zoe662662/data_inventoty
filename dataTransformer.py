import pandas as pd


def transform_to_datetime(col, **kwargs):
    tmp =  pd.to_datetime(col, errors='coerce', **kwargs)
    errors = df[tmp.isna()][col]
    errors = f'{len(errors)} errors\n' + '\n'.join(errors[:5].values.tolist())
    return tmp, errors


def transform_to_number(col, **kwargs):
    tmp = pd.to_numeric(col, errors='coerce', **kwargs)
    errors = col[tmp.isna()]
    errors = f'{len(errors)} errors\n' + '\n'.join(errors[:5].values.tolist())
    return tmp, errors


def transfrom_dtype(df, convert_dict):
    # convert_dict = {columna: dtype}}
    converter = {
        'int': transform_to_number,
        'datetime': transform_to_datetime()
    }

    s = df.dtypes.astype('string')
    s = pd.DataFrame(s, columns=['analyze_dtype'])

    for k, v in convert_dict.items():
        func = converter[v]
        res = func(df[k])
        df[k] = res[0]

    return df

if __name__ == "__main__":
    df = pd.DataFrame([['1'], ['2'], ['a']], columns=['col'])
    a = 1
    b = 2