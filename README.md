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

## Protocol grammars

`philoui` can read the declarative `tebka.protocol-grammar/v0.1` YAML format.
The loader validates role, state, action, transition, visibility, aggregation,
and termination references while preserving optional extensions for an engine
to interpret later.

```python
from philoui import load_protocol_grammar

document = load_protocol_grammar("protocols.yaml")
proposal = document.grammar("proposal")
actions = proposal.available_actions(proposal.initial_state, actor="proposer")
next_state = proposal.transition("idle", "propose", actor="proposer")
```

The loader does not execute actions and does not select a UI. The engine owns
execution semantics; Streamlit or another client may render the normalised
model.

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
