# Luganda Bridge

An English-to-Luganda translator built with Streamlit.

## Run it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the app at [http://localhost:8501](http://localhost:8501).

The app includes an offline phrasebook and word matcher. When **Use online** is enabled, it tries MyMemory first and falls back to the local phrasebook if the request fails.
