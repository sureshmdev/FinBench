# FinBench

FinBench is an interactive web app that benchmarks bank users based on the Bank Marketing dataset. Users can input their age, job, marital status, and loan information to see their standing among other users.

### Features

- Age categorization using MongoDB `$bucket`
- Job + Marital status aggregation using MongoDB `$group`
- Interactive charts showing user distribution
- Built with Python, Streamlit, and MongoDB Atlas

### Setup

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/FinBench.git
   cd FinBench
   ```

2. Create a virtual environment

   Windows:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   macOS / Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with:

   ```bash
   MONGODB_CONNECTION_URL=your_mongodb_connection_url
   ```

5. Load dataset into MongoDB:

   ```bash
   python load_bank_data.py
   ```

6. Run the app:
   ```bash
   streamlit run app.py
   ```
