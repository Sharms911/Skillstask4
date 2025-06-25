from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

EXCEL_PATH = '#AISSA RAP Activity Tracker 2023 - 2026 redacted copy (1).xlsx'
xls = pd.ExcelFile(EXCEL_PATH)
sheet_names = xls.sheet_names

@app.route('/')
def index():
    return render_template('index.html', sheets=sheet_names)

@app.route('/sheet/<name>')
def view_sheet(name):
    df = xls.parse(name).fillna('')
    headers = df.columns.tolist()
    rows = df.values.tolist()
    return render_template('sheet.html', sheet_name=name, headers=headers, rows=rows)


@app.route('/sheet/<name>', methods=['POST'])
def save_sheet(name):
    df = xls.parse(name)
    headers = df.columns.tolist()
    rows = df.shape[0]
    cols = df.shape[1]

    # Build updated data
    data = []
    for r in range(rows):
        row = []
        for c in range(cols):
            cell_key = f'cell_{r}_{c}'
            row.append(request.form.get(cell_key, ''))
        data.append(row)

    updated_df = pd.DataFrame(data, columns=headers)

    with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name=name, index=False)

    return redirect(url_for('view_sheet', name=name))

if __name__ == '__main__':
    app.run(debug=True)
