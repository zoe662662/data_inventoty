def output_html(df, file):
    p = '"&char(10)&"'
    df = df.applymap(lambda d: '="' + d.replace("\n", p) + '"' if type(d) == str else d)
    df = df.applymap(lambda d: d.replace(' ', '"&char(32)&"') if type(d) == str else d)
    df = df.fillna('')
    with open(file, 'w') as f:
        f.write(df.to_html())

