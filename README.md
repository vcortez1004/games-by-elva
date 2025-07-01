# Binaural Beat Generator

This Streamlit app generates custom binaural beats mixed with selectable background tracks. It can be embedded into a Wix page using an `<iframe>`.

## Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your `.mp3` background tracks in the project root.

## Running
Start the app locally with:
```bash
streamlit run main.py
```
The generated sessions will be logged in `session_log.csv`.

## Embedding in Wix
Deploy the Streamlit app (e.g., using Streamlit Community Cloud or your own host) and embed it on your Wix site with:
```html
<iframe src="YOUR_DEPLOYED_URL" width="100%" height="600" frameborder="0"></iframe>
```
Replace `YOUR_DEPLOYED_URL` with the URL of your running Streamlit app.
