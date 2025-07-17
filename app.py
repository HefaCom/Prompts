from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from math import ceil

app = Flask(__name__)

# Load the prompts dataset
try:
    df = pd.read_csv("prompts.csv")
    print(f"Loaded {len(df)} prompts successfully")
except Exception as e:
    print(f"Error loading dataset: {e}")
    # Create sample data if dataset fails to load
    df = pd.DataFrame({
        'act': ['Linux Terminal', 'English Translator', 'JavaScript Console'],
        'prompt': [
            'I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show.',
            'I want you to act as an English translator, spelling corrector and improver.',
            'I want you to act as a javascript console. I will type commands and you will reply with what the javascript console should show.'
        ]
    })

@app.route('/')
def index():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 12
    search_query = request.args.get('search', '')
    
    # Filter prompts based on search query
    filtered_df = df.copy()
    if search_query:
        filtered_df = df[
            df['act'].str.contains(search_query, case=False, na=False) |
            df['prompt'].str.contains(search_query, case=False, na=False)
        ]
    
    # Calculate pagination
    total_prompts = len(filtered_df)
    total_pages = ceil(total_prompts / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    prompts = filtered_df.iloc[start_idx:end_idx].to_dict('records')
    
    return render_template('index.html', 
                         prompts=prompts,
                         current_page=page,
                         total_pages=total_pages,
                         total_prompts=total_prompts,
                         search_query=search_query,
                         has_prev=page > 1,
                         has_next=page < total_pages)

@app.route('/api/prompts')
def api_prompts():
    search_query = request.args.get('search', '')
    
    filtered_df = df.copy()
    if search_query:
        filtered_df = df[
            df['act'].str.contains(search_query, case=False, na=False) |
            df['prompt'].str.contains(search_query, case=False, na=False)
        ]
    
    return jsonify({
        'prompts': filtered_df.to_dict('records'),
        'total': len(filtered_df)
    })

if __name__ == '__main__':
    app.run(debug=True)

# Create templates directory and files
templates_dir = 'templates'
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)


# Save the HTML template
with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Flask application created successfully!")
print("\nTo run the application:")
print("1. Install required packages: pip install flask pandas")
print("2. Run the application: python app.py")
print("3. Open your browser and go to: http://127.0.0.1:5000")