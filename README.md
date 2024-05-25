# Bird Watcher


# Setup

First, we can make a virtual environment to install the necessary packages. 

```bash
python -m venv env_birds
```

Then, we can activate the virtual environment. 

```bash
source env_birds/bin/activate
```

Then, we can install the necessary packages. 

```bash
pip install -r requirements.txt
```

## Instructions

Run main.py to get the continually updating bird tracker. 

Run streamlit app to get the bird tracker with a GUI. 

```bash
streamlit run app.py
```

Set up ngrok to get the streamlit app online. 

```bash
ngrok http 8501
```
