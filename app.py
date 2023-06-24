from flask import Flask, render_template, request, send_file, make_response, flash
import pandas as pd
import time
from data_cleaning import data_cleaning
from plotting import plotting
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey' #for flash messages
df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def data_cleaning_route():
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

                # Data cleaning operations
                if handle_missing_values:
                    df = data_cleaning.handle_missing_values(df)
                if drop_duplicates:
                    df = data_cleaning.drop_duplicates(df)
                if normalize_data:
                    df = data_cleaning.normalize_data(df)
                if encode_categorical:
                    df = data_cleaning.encode_categorical(df)
                if filter_outliers:
                    df = data_cleaning.filter_outliers(df)

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
                plots = []
                numerical_columns = df.select_dtypes(include=[np.number]).columns
                plot_type = request.form.get('plot_type')
                for col in numerical_columns[:2]:
                    print(f"Generating {plot_type} for {col}")
                    start_time = time.time()
                    fig = plotting.get_plot(df, plot_type, col)
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
