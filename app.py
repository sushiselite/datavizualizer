from flask import Flask, render_template, request, send_file, make_response, flash
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # needed for flashing messages
df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def data_cleaning():
    global df
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_csv(file.stream)
                
                # Get user choices
                handle_missing_values = request.form.get('handle_missing_values') == 'on'
                drop_duplicates = request.form.get('drop_duplicates') == 'on'
                normalize_data = request.form.get('normalize_data') == 'on'
                encode_categorical = request.form.get('encode_categorical') == 'on'
                filter_outliers = request.form.get('filter_outliers') == 'on'

                # Handling missing values
                if handle_missing_values:
                    df = df.fillna(method='ffill')
                
                # Dropping duplicates
                if drop_duplicates:
                    df = df.drop_duplicates()

                # Normalizing data
                if normalize_data:
                    min_max_scaler = preprocessing.MinMaxScaler()
                    df = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns)

                # Encoding categorical values
                if encode_categorical:
                    df = pd.get_dummies(df)

                # Filtering outliers using Z-score
                if filter_outliers:
                    df = df[(np.abs(stats.zscore(df.select_dtypes(include=[np.number]))) < 3).all(axis=1)]

                # Create a download link for the cleaned data
                cleaned_data_download_link = f'<a href="/download">Download Cleaned Data</a>'
                
                return render_template('data_cleaning.html', cleaned_data=df.to_html(index=False), download_link=cleaned_data_download_link)
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('data_cleaning.html', error_message=error_message)
    return render_template('data_cleaning.html')

@app.route('/data-analysis', methods=['GET', 'POST'])
def data_analysis():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                start_time = time.time()
                df = pd.read_csv(file.stream)
                print(f"Time taken to read file: {time.time() - start_time} seconds")

                max_rows = 1000
                if df.shape[0] > max_rows:
                    flash(f'File is too large, only processing the first {max_rows} rows')
                    df = df.head(max_rows)

                plots = []
                numerical_columns = df.select_dtypes(include=[np.number]).columns
                for col in numerical_columns[:2]:
                    print(f"Generating histogram for {col}")  # Logging
                    start_time = time.time()
                    fig = px.histogram(df, x=col)
                    plot_html = fig.to_html(full_html=False)
                    plots.append(plot_html)
                    print(f"Time taken for {col}: {time.time() - start_time} seconds")

                return render_template('data_analysis.html', plots=plots)
            except Exception as e:
                error_message = f"Error occurred during data analysis: {str(e)}"
                flash(error_message)
                return render_template('data_analysis.html', error_message=error_message)

    return render_template('data_analysis.html')

@app.route('/download')
def download():
    global df
    cleaned_data_csv = df.to_csv(index=False)
    cleaned_data_csv = bytes(cleaned_data_csv, 'utf-8')
    response = make_response(cleaned_data_csv)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='cleaned_data.csv')
    return response

if __name__ == '__main__':
    app.run(debug=True)
