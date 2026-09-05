# Online Python & Deep Learning Quiz

80 MCQs, 90 minutes, student result screen, teacher login, persistent Google
Sheets storage, local CSV fallback, teacher result list, search and CSV download.

## Run
pip install -r requirements.txt
streamlit run app.py

## Google Sheets
1. Create a Google Sheet.
2. Create a Google Cloud service account and key.
3. Share the Sheet with the service account email as Editor.
4. Put the spreadsheet URL/ID and service-account credentials into Streamlit Secrets.
5. The app creates a `Results` worksheet automatically.
6. Each completed quiz is appended as one result row.

## Teacher
Set `TEACHER_PASSWORD` in Streamlit Secrets. The password is never stored in
the Python source.

## Deploy
Push the project to GitHub and deploy `app.py` through Streamlit Community Cloud.
Put the real secrets in the deployment's Advanced Settings > Secrets.
