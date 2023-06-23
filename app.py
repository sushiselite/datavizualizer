from flask import Flask, render_template, request, send_file
import pandas as pd
import io
from flask import make_response

app = Flask(__name__)
df = pd.DataFrame()  # Define df as a global variable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def data_cleaning():
    global df  # Access the global df variable

    if request.method == 'POST':
        # Retrieve the uploaded file
        file = request.files['file']

        # Check if a file is selected
        if file:
            try:
                # Read the file using Pandas
                df = pd.read_csv(file)

                # Perform data cleaning operations
                initial_rows = df.shape[0]
                df = df.dropna()  # Drop rows with missing values
                df = df.drop_duplicates()  # Remove duplicate rows
                cleaned_rows = df.shape[0]

                # Generate statistics
                num_rows_dropped = initial_rows - cleaned_rows
                percentage_rows_dropped = (num_rows_dropped / initial_rows) * 100

                # Create a download link for the cleaned data
                cleaned_data_csv = df.to_csv(index=False)
                cleaned_data_csv = bytes(cleaned_data_csv, 'utf-8')
                cleaned_data_download_link = f'<a href="/download">Download Cleaned Data</a>'

                # Pass the cleaned data and statistics to the template
                return render_template('data_cleaning.html', cleaned_data=df.to_html(), 
                                       statistics={'rows_dropped': num_rows_dropped, 'percentage_rows_dropped': percentage_rows_dropped},
                                       download_link=cleaned_data_download_link)
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('data_cleaning.html', error_message=error_message)

    return render_template('data_cleaning.html')

@app.route('/download')
def download():
    global df  # Access the global df variable

    # Generate a file-like object of the cleaned data
    cleaned_data_csv = df.to_csv(index=False)
    cleaned_data_csv = bytes(cleaned_data_csv, 'utf-8')

    # Create a download response
    response = make_response(cleaned_data_csv)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='cleaned_data.csv')

    return response

if __name__ == '__main__':
    app.run(debug=True)
