# FactCheck

Search leading academics' opinions on issues. Powered by [Microsoft Academic API](https://www.microsoft.com/en-us/research/project/academic-knowledge/).

<p align="center">
  <img src="https://i.imgur.com/ki9yUkV.gif">
</p>

## Setup

Subscribe to [Project Academic Knowledge](https://msr-apis.portal.azure-api.net/products/project-academic-knowledge) and update `secrets.py`
```python
MICROSOFT_ACADEMIC_API_KEY = "YOUR_KEY"
```

Create and activate environment
```bash
conda env create --file environment.yml
conda activate factcheck
```

Run application
```bash
python app.py
```
