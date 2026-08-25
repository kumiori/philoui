import io
import tempfile
import unittest
from pathlib import Path

from philoui.protocol_grammar import (
    ProtocolGrammarError,
    load_protocol_grammar,
    parse_protocol_grammar,
)


VALID_GRAMMAR = """
schema: tebka.protocol-grammar/v0.1
source_note: preserved extension
grammars:
  tcp-handshake:
    title: TCP handshake
    description: Minimal three-message connection establishment.
    roles:
      client: {count: 1}
      server: {count: 1}
    initial_state: closed
    states: [closed, syn-sent, syn-received, established]
    actions:
      syn:
        actor: client
        target: server
        from: closed
        to: syn-sent
        emits: SYN
      syn-ack:
        actor: server
        target: client
        from: syn-sent
        to: syn-received
        emits: SYN_ACK
      ack:
        actor: client
        target: server
        from: syn-received
        to: established
        emits: ACK
    terminal: [established]
  decentralised-escrow:
    title: Decentralised escrow
    description: Threshold-based release or refund.
    roles:
      buyer: {count: 1}
      seller: {count: 1}
      arbiter:
        count: {min: 1, max: 3}
    initial_state: open
    states: [open, funded, voting, released, refunded]
    visibility:
      ballot:
        buyer: private
        seller: hidden
        arbiter: visible
    rules:
      release_threshold: 2
      refund_threshold: 2
    actions:
      fund:
        actor: buyer
        target: protocol
        from: open
        to: funded
      open-vote:
        actor: [buyer, seller, arbiter]
        target: all
        from: funded
        to: voting
      vote-release:
        actor: [buyer, seller, arbiter]
        target: protocol
        from: voting
        remains: voting
        contributes_to: release_threshold
        aggregation: {minimum: 2}
    automatic_transitions:
      - when: {threshold_met: release_threshold}
        to: released
      - when: {threshold_met: refund_threshold}
        to: refunded
    terminal: [released, refunded]
"""


class ProtocolGrammarTests(unittest.TestCase):
    def test_parses_and_normalises_core_grammar(self):
        document = parse_protocol_grammar(VALID_GRAMMAR)
        grammar = document.grammar("tcp-handshake")

        self.assertEqual(document.schema, "tebka.protocol-grammar/v0.1")
        self.assertEqual(document.extensions["source_note"], "preserved extension")
        self.assertEqual(grammar.roles["client"].exact_count, 1)
        self.assertEqual(grammar.actions["syn"].actors, ("client",))
        self.assertEqual(grammar.actions["syn"].emits, "SYN")
        self.assertEqual(grammar.transition("closed", "syn", "client"), "syn-sent")
        self.assertTrue(grammar.is_terminal("established"))

    def test_preserves_orthogonal_protocol_features(self):
        grammar = parse_protocol_grammar(VALID_GRAMMAR).grammar("decentralised-escrow")

        self.assertEqual(grammar.roles["arbiter"].minimum, 1)
        self.assertEqual(grammar.roles["arbiter"].maximum, 3)
        self.assertEqual(grammar.visibility["ballot"]["seller"], "hidden")
        self.assertEqual(grammar.rules["release_threshold"], 2)
        self.assertEqual(
            grammar.actions["vote-release"].extensions["contributes_to"],
            "release_threshold",
        )
        self.assertTrue(grammar.actions["vote-release"].remains)
        self.assertEqual(grammar.transition("voting", "vote-release"), "voting")
        self.assertEqual(grammar.automatic_transitions[0].to_state, "released")

    def test_filters_available_actions_by_state_and_actor(self):
        grammar = parse_protocol_grammar(VALID_GRAMMAR).grammar("decentralised-escrow")

        self.assertEqual(
            [action.name for action in grammar.available_actions("voting", "buyer")],
            ["vote-release"],
        )
        self.assertEqual(grammar.available_actions("open", "seller"), ())

    def test_loads_from_path_and_text_stream(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "grammar.yaml"
            path.write_text(VALID_GRAMMAR, encoding="utf-8")
            self.assertIn("tcp-handshake", load_protocol_grammar(path).grammars)

        self.assertIn(
            "decentralised-escrow",
            load_protocol_grammar(io.StringIO(VALID_GRAMMAR)).grammars,
        )

    def test_reports_all_cross_reference_errors(self):
        invalid = VALID_GRAMMAR.replace("initial_state: closed", "initial_state: missing")
        invalid = invalid.replace("target: server", "target: stranger", 1)
        invalid = invalid.replace("to: established", "to: nowhere", 1)

        with self.assertRaises(ProtocolGrammarError) as context:
            parse_protocol_grammar(invalid)

        message = str(context.exception)
        self.assertIn("initial_state 'missing'", message)
        self.assertIn("unknown role 'stranger'", message)
        self.assertIn("unknown destination state 'nowhere'", message)

    def test_rejects_unsafe_yaml_tags(self):
        with self.assertRaises(ProtocolGrammarError):
            parse_protocol_grammar("!!python/object/apply:os.system ['echo unsafe']")


if __name__ == "__main__":
    unittest.main()
