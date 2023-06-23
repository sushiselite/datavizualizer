from flask import Flask, render_template, request, send_file, make_response
import pandas as pd

app = Flask(__name__)
df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def data_cleaning():
    global df
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                df = pd.read_csv(file.stream)

                dataset_type = detect_dataset_type(df)
                # Generate statistics
                initial_rows = df.shape[0]
                cleaned_df = df.dropna().drop_duplicates()
                cleaned_rows = initial_rows - cleaned_df.shape[0]
                percentage_rows_dropped = (cleaned_rows / initial_rows) * 100 if initial_rows > 0 else 0

                # Create a download link for the cleaned data
                cleaned_data_download_link = f'<a href="/download">Download Cleaned Data</a>'
                
                # Pass the cleaned data, dataset type, and statistics to the template
                return render_template('data_cleaning.html', cleaned_data=cleaned_df.to_html(index=False),
                                       dataset_type=dataset_type,
                                       statistics={'rows_dropped': cleaned_rows,
                                                   'percentage_rows_dropped': percentage_rows_dropped},
                                       download_link=cleaned_data_download_link)
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('data_cleaning.html', error_message=error_message)
    return render_template('data_cleaning.html')

@app.route('/download')
def download():
    global df
    cleaned_data_csv = df.to_csv(index=False)
    cleaned_data_csv = bytes(cleaned_data_csv, 'utf-8')
    response = make_response(cleaned_data_csv)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='cleaned_data.csv')
    return response

def detect_dataset_type(df):
    # Identify dataset type based on the characteristics of the DataFrame
    if all(df.dtypes.isin(['int64', 'float64'])):
        return 'Numerical'
    elif len(df.columns) == 2 and all(df.apply(lambda col: len(col.unique()) == 2)):
        return 'Bivariate'
    elif len(df.columns) > 2 and df.dtypes.nunique() > 1:
        return 'Multivariate'
    elif any(df.dtypes == 'object'):
        return 'Categorical'
    elif any(df.dtypes.isin(['int64', 'float64'])):
        return 'Correlation'
    else:
        return 'Unknown'

if __name__ == '__main__':
    app.run(debug=True)
