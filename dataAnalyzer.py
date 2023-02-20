import pandas as pd


def summarize_result(index_count, total, top=5, down=5, max_show=10):
    # index_count: pd.DataFrame(columns=['any'], index='any')
    sep = '\n'
    bias = 2
    p = '{index:%s}: {cnt:<%s} ({pct}' % (
        index_count.index.map(lambda d: len(str(d))).max() + bias,
        len(str(index_count.max())) + bias
    ) + '%)'
    tmp1 = [p.format(index=str(row[0]), cnt=row[1], pct=round(row[1]*100/total, 1))
            for row in index_count.reset_index(name='value').values]
    if len(index_count) <= max_show:
        tmp1 = sep.join(tmp1)
    else:
        tmp1 = f'top{sep}' + sep.join(tmp1[:top]) + f'{sep}down{sep}' + sep.join(tmp1[-down:])
    return tmp1


def analyze_string_len(df, colname):
    tmp = df[[colname]].applymap(lambda d: len(str(d))).groupby(colname)[colname].count()
    tmp = tmp.sort_index()
    zfill = len(str(tmp.index.max()))
    tmp.index = tmp.index.map(lambda d: f'len_{str(d).zfill(zfill)}')
    tmp['null'] = df[colname].isna().sum()
    return summarize_result(tmp, len(df))


def analyze_values_distributtion(df, colname):
    tmp = df[[colname]].groupby(colname)[colname].count()
    tmp = tmp.sort_index(ascending=False)
    tmp_index = summarize_result(tmp, len(df))
    #
    tmp['null'] = df[colname].isna().sum()
    tmp = tmp.sort_values(ascending=False)
    tmp_value = summarize_result(tmp, len(df))
    return [tmp_index, tmp_value]


def analyze_datetime_customized(df, colname):
    df['tmp'] = df[colname].dt.strftime('%Y').str[:3] + '?'
    df.loc[df[colname] < '1930-01-01', 'tmp'] = '19??'
    df.loc[df[colname] > '2030-01-01', 'tmp'] = '20??'

    tmp = df[['tmp']].groupby('tmp')['tmp'].count()
    tmp = tmp.sort_index()
    tmp_index = summarize_result(tmp, len(df))
    df.drop('tmp', axis=1, inplace=True)
    return tmp_index


def analyze_columns(df):
    s = df.dtypes.astype('string')
    s = pd.DataFrame(s, columns=['analyze_dtype'])
    s['null'] = df.isna().sum()
    s['unique'] = df.nunique()

    # string
    for c in s.index:
        # print(c)
        s.loc[c, 'len'] = analyze_string_len(df, c)

    for c in df.columns:
        res = analyze_values_distributtion(df, c)
        s.loc[c, 'value(index)'] = res[0]
        s.loc[c, 'value(value)'] = res[1]

    for c in df.select_dtypes('datetime').columns:
        s.loc[c, 'custome'] = analyze_datetime_customized(df, c)

    s['null'] = s['null'] .map(lambda d: ('{index} ({pct}%)').format(index=d, pct=round(d*100/len(df))))
    s['unique'] = s['unique'].map(lambda d: ('{index} ({pct}%)').format(index=d, pct=round(d*100/len(df))))

    return s

