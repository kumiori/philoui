import streamlit as st


st.set_page_config(page_title="Protocol grammar inspector", page_icon="🧩", layout="wide")

from philoui.protocol_grammar import ProtocolGrammarError, parse_protocol_grammar


SAMPLE = """schema: tebka.protocol-grammar/v0.1
grammars:
  proposal:
    title: Proposal
    description: One participant proposes; another accepts or rejects.
    roles:
      proposer: {count: 1}
      respondent: {count: 1}
    initial_state: idle
    states: [idle, proposed, accepted, rejected]
    actions:
      propose:
        actor: proposer
        target: respondent
        from: idle
        to: proposed
      accept:
        actor: respondent
        target: proposer
        from: proposed
        to: accepted
      reject:
        actor: respondent
        target: proposer
        from: proposed
        to: rejected
    terminal: [accepted, rejected]
"""


st.title("Protocol grammar inspector")
st.caption("The YAML defines the grammar. This page only validates and renders it.")

uploaded = st.file_uploader("Protocol grammar YAML", type=["yaml", "yml"])
if uploaded is not None:
    try:
        source = uploaded.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("The uploaded file must be UTF-8 text.")
        st.stop()
else:
    source = st.text_area("YAML source", SAMPLE, height=380)

try:
    document = parse_protocol_grammar(source)
except ProtocolGrammarError as error:
    st.error("The grammar is not valid.")
    for issue in error.errors:
        st.write(f"- {issue}")
    st.stop()

st.success(f"Valid {document.schema} document")
grammar_name = st.selectbox("Grammar", list(document.grammars))
grammar = document.grammar(grammar_name)

st.header(grammar.title)
st.write(grammar.description)
roles_metric, states_metric, actions_metric, terminal_metric = st.columns(4)
roles_metric.metric("Roles", len(grammar.roles))
states_metric.metric("States", len(grammar.states))
actions_metric.metric("Actions", len(grammar.actions))
terminal_metric.metric("Terminal states", len(grammar.terminal_states))

roles_tab, transitions_tab, policy_tab, raw_tab = st.tabs(
    ["Roles", "Transitions", "Policy extensions", "Normalised model"]
)

with roles_tab:
    st.dataframe(
        [
            {
                "role": role.name,
                "minimum": role.minimum,
                "maximum": role.maximum if role.maximum is not None else "unbounded",
            }
            for role in grammar.roles.values()
        ],
        hide_index=True,
        use_container_width=True,
    )

with transitions_tab:
    st.write(f"Initial state: `{grammar.initial_state}`")
    st.dataframe(
        [
            {
                "action": action.name,
                "actor": ", ".join(action.actors),
                "target": ", ".join(action.targets),
                "from": ", ".join(action.from_states),
                "to": action.to_state,
                "emits": action.emits or "",
                "terminal": grammar.is_terminal(action.to_state),
            }
            for action in grammar.actions.values()
        ],
        hide_index=True,
        use_container_width=True,
    )

with policy_tab:
    st.subheader("Visibility")
    st.json(grammar.visibility)
    st.subheader("Rules")
    st.json(grammar.rules)
    st.subheader("Automatic transitions")
    st.json(
        [
            {"when": transition.condition, "to": transition.to_state}
            for transition in grammar.automatic_transitions
        ]
    )
    st.subheader("Preserved extensions")
    st.json(grammar.extensions)

with raw_tab:
    st.json(
        {
            "name": grammar.name,
            "initial_state": grammar.initial_state,
            "states": grammar.states,
            "terminal": grammar.terminal_states,
            "available_from_initial": [
                action.name for action in grammar.available_actions(grammar.initial_state)
            ],
        }
    )
