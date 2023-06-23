from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def data_cleaning():
    if request.method == 'POST':
        # Retrieve the uploaded file
        file = request.files['file']

        # Check if a file is selected
        if file:
            try:
                # Read the file using Pandas
                df = pd.read_csv(file)

                # Perform data cleaning operations
                df = df.dropna()  # Drop rows with missing values
                df = df.drop_duplicates()  # Remove duplicate rows

                # Pass the cleaned data to the template
                return render_template('data_cleaning.html', cleaned_data=cleaned_df.to_html())
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('data_cleaning.html', error_message=error_message)

    return render_template('data_cleaning.html')

if __name__ == '__main__':
    app.run(debug=True)
