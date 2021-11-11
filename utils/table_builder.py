from beautifultable import BeautifulTable


def build_table(headers, dataRows, row_numbers=False):
    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    table.columns.header = headers
    for row in dataRows:
        table.rows.append(row)
    if row_numbers:
        table.rows.header = [str(n+1) for n in range(len(dataRows))]
    return table
