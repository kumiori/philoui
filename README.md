# philoui

Philosophically informed interactive interfaces for Streamlit.

## Installation

Install the released package:

```bash
pip install philoui
```

For local development:

```bash
python -m pip install -e .
```

Equivalently, for tools that expect a requirements file:

```bash
python -m pip install -r requirements.txt
```

Both commands use `pyproject.toml` as the dependency source of truth and allow
pip to choose versions compatible with the active Python interpreter.

Audio support is optional because it requires system audio libraries:

```bash
python -m pip install -e '.[audio]'
```

## Frontend development

The built selector frontend is included in Python distributions. To work on
the React component itself:

```bash
cd philoui/philoui_selectors/frontend/
npm install
npm start
```

Set `PHILOUI_COMPONENT_URL=http://localhost:3001` while running a Streamlit app
to use that development server. Run `npm run build` before publishing.
