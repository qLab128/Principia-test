# Principia V1.3 Examples

The official quickstart notebook is:

- `principia_v13_tutorial.ipynb`

It demonstrates the full real-LLM workflow:

1. Search 50 real works from public metadata sources.
2. Extract structured features from the top-ranked works.
3. Select evidence for generation.
4. Generate a V1.3 idea.
5. Compare the generated idea against extracted prior ideas.
6. Export visible local files under `principia_project/principia_outputs/latest/`.

## Install

```bash
python -m pip install principia-ai ipykernel
python -m ipykernel install --user --name principia-v13-python --display-name "Python 3.12 (Principia V1.3)"
```

For source development from this repository:

```bash
python -m pip install -e ".[dev]"
python -m ipykernel install --user --name principia-v13-python --display-name "Python 3.12 (Principia V1.3)"
```

In VS Code, open the notebook and select `Python 3.12 (Principia V1.3)`. If the named kernel is not shown, choose the Python interpreter where `principia-ai` and `ipykernel` were installed.

## API Key

The notebook intentionally uses a placeholder:

```python
API_key = "YOUR_SILICONFLOW_API_KEY"
```

Replace it at runtime with your own SiliconFlow key. Do not commit notebooks containing real API keys or executed outputs.

