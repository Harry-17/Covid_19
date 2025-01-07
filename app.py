from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

# Initialize Flask app
app = Flask(__name__)

# Load and process the data
data_path = 'covid_data.csv'  # Path to your CSV file
df = pd.read_csv(data_path)

# Add additional columns (e.g., recovery rate)
df['Recovery Rate'] = (df['Recovered'] / df['Confirmed']) * 100
df['Mortality Rate'] = (df['Deaths'] / df['Confirmed']) * 100

@app.route('/')
def home():
    
    stats = df.describe().to_html(classes='table table-bordered')
    return render_template('index.html', stats=stats)

@app.route('/country', methods=['GET', 'POST'])
def country_analysis():
    if request.method == 'POST':
        country = request.form.get('country')
        country_data = df[df['Country/Region'] == country]
        if country_data.empty:
            return f"<h3>No data available for {country}</h3>"
        else:
            return country_data.to_html(classes='table table-bordered')

    return '''
        <form method="post">
            Country: <input type="text" name="country">
            <button type="submit">Submit</button>
        </form>
    '''

@app.route('/visualization')
def visualize():
    # Prepare data for confirmed cases chart (Top 10)
    top_10_confirmed = df.groupby('Country/Region').sum().sort_values('Confirmed', ascending=False).head(10)
    confirmed_cases = top_10_confirmed['Confirmed'].tolist()
    countries = top_10_confirmed.index.tolist()

    return jsonify({"countries": countries, "confirmed_cases": confirmed_cases})

@app.route('/rates-visualization')
def rates_visualization():
    # Get average recovery and mortality rates
    avg_recovery_rate = df['Recovery Rate'].mean()
    avg_mortality_rate = df['Mortality Rate'].mean()
    return jsonify({"recovery_rate": avg_recovery_rate, "mortality_rate": avg_mortality_rate})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
