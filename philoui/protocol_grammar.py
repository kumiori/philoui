"""Read and validate declarative protocol grammars.

The grammar describes who may act, from which state, and which state follows.
It intentionally contains no UI or protocol-specific execution classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, TextIO

import yaml


SCHEMA_ID = "tebka.protocol-grammar/v0.1"
SPECIAL_ACTORS = frozenset({"system", "protocol"})
SPECIAL_TARGETS = frozenset({"all", "system", "protocol"})


class ProtocolGrammarError(ValueError):
    """Raised when a protocol grammar is malformed or internally inconsistent."""

    def __init__(self, errors: list[str] | tuple[str, ...]):
        self.errors = tuple(errors)
        super().__init__("Invalid protocol grammar:\n- " + "\n- ".join(self.errors))


@dataclass(frozen=True)
class Role:
    name: str
    minimum: int
    maximum: int | None = None

    @property
    def exact_count(self) -> int | None:
        return self.minimum if self.maximum == self.minimum else None


@dataclass(frozen=True)
class Action:
    name: str
    actors: tuple[str, ...]
    targets: tuple[str, ...]
    from_states: tuple[str, ...]
    to_state: str
    remains: bool = False
    emits: str | None = None
    aggregation: Mapping[str, Any] | None = None
    extensions: Mapping[str, Any] = field(default_factory=dict)

    def permits(self, state: str, actor: str | None = None) -> bool:
        return state in self.from_states and (actor is None or actor in self.actors)


@dataclass(frozen=True)
class AutomaticTransition:
    condition: Mapping[str, Any]
    to_state: str
    extensions: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Grammar:
    name: str
    title: str
    description: str
    roles: Mapping[str, Role]
    initial_state: str
    states: tuple[str, ...]
    actions: Mapping[str, Action]
    terminal_states: tuple[str, ...]
    visibility: Mapping[str, Any] = field(default_factory=dict)
    rules: Mapping[str, Any] = field(default_factory=dict)
    automatic_transitions: tuple[AutomaticTransition, ...] = ()
    extensions: Mapping[str, Any] = field(default_factory=dict)

    def available_actions(self, state: str, actor: str | None = None) -> tuple[Action, ...]:
        """Return actions permitted for a state and, optionally, a role."""
        if state not in self.states:
            raise KeyError(f"Unknown state {state!r} in grammar {self.name!r}")
        return tuple(
            action for action in self.actions.values() if action.permits(state, actor)
        )

    def transition(self, state: str, action_name: str, actor: str | None = None) -> str:
        """Resolve one declared transition without applying side effects."""
        try:
            action = self.actions[action_name]
        except KeyError as error:
            raise KeyError(f"Unknown action {action_name!r} in grammar {self.name!r}") from error
        if not action.permits(state, actor):
            qualifier = f" for actor {actor!r}" if actor else ""
            raise ValueError(
                f"Action {action_name!r} is not permitted from {state!r}{qualifier}"
            )
        return action.to_state

    def is_terminal(self, state: str) -> bool:
        return state in self.terminal_states


@dataclass(frozen=True)
class ProtocolGrammarDocument:
    schema: str
    grammars: Mapping[str, Grammar]
    extensions: Mapping[str, Any] = field(default_factory=dict)

    def grammar(self, name: str) -> Grammar:
        try:
            return self.grammars[name]
        except KeyError as error:
            raise KeyError(f"Unknown grammar {name!r}") from error


def load_protocol_grammar(source: str | Path | TextIO) -> ProtocolGrammarDocument:
    """Load a grammar document from a filesystem path or readable text stream."""
    if hasattr(source, "read"):
        return parse_protocol_grammar(source.read())
    path = Path(source)
    try:
        return parse_protocol_grammar(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ProtocolGrammarError([f"Could not read {path}: {error}"]) from error


def parse_protocol_grammar(text: str) -> ProtocolGrammarDocument:
    """Parse a YAML protocol-grammar document using the safe YAML loader."""
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise ProtocolGrammarError([f"YAML could not be parsed: {error}"]) from error
    return protocol_grammar_from_mapping(raw)


def protocol_grammar_from_mapping(raw: Any) -> ProtocolGrammarDocument:
    errors: list[str] = []
    if not isinstance(raw, Mapping):
        raise ProtocolGrammarError(["document must be a mapping"])

    schema = raw.get("schema")
    if schema != SCHEMA_ID:
        errors.append(f"schema must be {SCHEMA_ID!r}, got {schema!r}")

    raw_grammars = raw.get("grammars")
    if not isinstance(raw_grammars, Mapping) or not raw_grammars:
        errors.append("grammars must be a non-empty mapping")
        raw_grammars = {}

    grammars: dict[str, Grammar] = {}
    for name, value in raw_grammars.items():
        if not isinstance(name, str) or not name:
            errors.append(f"grammar name must be a non-empty string, got {name!r}")
            continue
        grammar = _parse_grammar(name, value, errors)
        if grammar is not None:
            grammars[name] = grammar

    if errors:
        raise ProtocolGrammarError(errors)

    extensions = {key: value for key, value in raw.items() if key not in {"schema", "grammars"}}
    return ProtocolGrammarDocument(schema=schema, grammars=grammars, extensions=extensions)


def _parse_grammar(name: str, raw: Any, errors: list[str]) -> Grammar | None:
    prefix = f"grammars.{name}"
    if not isinstance(raw, Mapping):
        errors.append(f"{prefix} must be a mapping")
        return None

    states = _string_tuple(raw.get("states"), f"{prefix}.states", errors)
    if not states:
        errors.append(f"{prefix}.states must not be empty")
    if len(set(states)) != len(states):
        errors.append(f"{prefix}.states contains duplicates")
    state_set = set(states)

    initial_state = raw.get("initial_state")
    if initial_state not in state_set:
        errors.append(f"{prefix}.initial_state {initial_state!r} is not declared in states")

    terminal = _string_tuple(raw.get("terminal", []), f"{prefix}.terminal", errors)
    for state in terminal:
        if state not in state_set:
            errors.append(f"{prefix}.terminal references unknown state {state!r}")

    roles = _parse_roles(raw.get("roles"), prefix, errors)
    actions = _parse_actions(raw.get("actions"), prefix, state_set, set(roles), errors)
    automatic = _parse_automatic_transitions(
        raw.get("automatic_transitions", []), prefix, state_set, errors
    )

    visibility = raw.get("visibility", {})
    if not isinstance(visibility, Mapping):
        errors.append(f"{prefix}.visibility must be a mapping")
        visibility = {}
    else:
        for subject, policy in visibility.items():
            if not isinstance(policy, Mapping):
                errors.append(f"{prefix}.visibility.{subject} must be a role mapping")
                continue
            for role in policy:
                if role not in roles:
                    errors.append(
                        f"{prefix}.visibility.{subject} references unknown role {role!r}"
                    )

    rules = raw.get("rules", {})
    if not isinstance(rules, Mapping):
        errors.append(f"{prefix}.rules must be a mapping")
        rules = {}

    known = {
        "title", "description", "roles", "initial_state", "states", "actions",
        "terminal", "visibility", "rules", "automatic_transitions",
    }
    return Grammar(
        name=name,
        title=str(raw.get("title", name)),
        description=str(raw.get("description", "")),
        roles=roles,
        initial_state=str(initial_state),
        states=states,
        actions=actions,
        terminal_states=terminal,
        visibility=dict(visibility),
        rules=dict(rules),
        automatic_transitions=automatic,
        extensions={key: value for key, value in raw.items() if key not in known},
    )


def _parse_roles(raw: Any, prefix: str, errors: list[str]) -> dict[str, Role]:
    if not isinstance(raw, Mapping) or not raw:
        errors.append(f"{prefix}.roles must be a non-empty mapping")
        return {}
    roles: dict[str, Role] = {}
    for name, config in raw.items():
        path = f"{prefix}.roles.{name}.count"
        if not isinstance(name, str) or not name:
            errors.append(f"{prefix}.roles contains an invalid name {name!r}")
            continue
        if not isinstance(config, Mapping):
            errors.append(f"{prefix}.roles.{name} must be a mapping")
            continue
        count = config.get("count")
        if _positive_int(count):
            roles[name] = Role(name, count, count)
            continue
        if isinstance(count, Mapping):
            minimum = count.get("min")
            maximum = count.get("max")
            if not _positive_int(minimum):
                errors.append(f"{path}.min must be a positive integer")
                continue
            if maximum is not None and (
                not _positive_int(maximum) or maximum < minimum
            ):
                errors.append(f"{path}.max must be an integer greater than or equal to min")
                continue
            roles[name] = Role(name, minimum, maximum)
            continue
        errors.append(f"{path} must be a positive integer or a min/max mapping")
    return roles


def _parse_actions(
    raw: Any,
    prefix: str,
    states: set[str],
    roles: set[str],
    errors: list[str],
) -> dict[str, Action]:
    if not isinstance(raw, Mapping) or not raw:
        errors.append(f"{prefix}.actions must be a non-empty mapping")
        return {}
    actions: dict[str, Action] = {}
    for name, config in raw.items():
        path = f"{prefix}.actions.{name}"
        if not isinstance(name, str) or not name or not isinstance(config, Mapping):
            errors.append(f"{path} must be a named mapping")
            continue
        actors = _string_tuple(config.get("actor"), f"{path}.actor", errors)
        targets = _string_tuple(config.get("target"), f"{path}.target", errors)
        from_states = _string_tuple(config.get("from"), f"{path}.from", errors)
        for actor in actors:
            if actor not in roles | SPECIAL_ACTORS:
                errors.append(f"{path}.actor references unknown role {actor!r}")
        for target in targets:
            if target not in roles | SPECIAL_TARGETS:
                errors.append(f"{path}.target references unknown role {target!r}")
        for state in from_states:
            if state not in states:
                errors.append(f"{path}.from references unknown state {state!r}")

        has_to = "to" in config
        has_remains = "remains" in config
        if has_to == has_remains:
            errors.append(f"{path} must declare exactly one of 'to' or 'remains'")
            destination = ""
        else:
            destination = config.get("to") if has_to else config.get("remains")
            if destination not in states:
                errors.append(f"{path} references unknown destination state {destination!r}")

        aggregation = config.get("aggregation")
        if aggregation is not None:
            if not isinstance(aggregation, Mapping):
                errors.append(f"{path}.aggregation must be a mapping")
            elif "minimum" in aggregation and not _positive_int(aggregation["minimum"]):
                errors.append(f"{path}.aggregation.minimum must be a positive integer")

        known = {"actor", "target", "from", "to", "remains", "emits", "aggregation"}
        actions[name] = Action(
            name=name,
            actors=actors,
            targets=targets,
            from_states=from_states,
            to_state=str(destination),
            remains=has_remains,
            emits=str(config["emits"]) if config.get("emits") is not None else None,
            aggregation=dict(aggregation) if isinstance(aggregation, Mapping) else None,
            extensions={key: value for key, value in config.items() if key not in known},
        )
    return actions


def _parse_automatic_transitions(
    raw: Any, prefix: str, states: set[str], errors: list[str]
) -> tuple[AutomaticTransition, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        errors.append(f"{prefix}.automatic_transitions must be a list")
        return ()
    result = []
    for index, item in enumerate(raw):
        path = f"{prefix}.automatic_transitions[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        condition = item.get("when")
        destination = item.get("to")
        if not isinstance(condition, Mapping) or not condition:
            errors.append(f"{path}.when must be a non-empty mapping")
            condition = {}
        if destination not in states:
            errors.append(f"{path}.to references unknown state {destination!r}")
        result.append(
            AutomaticTransition(
                condition=dict(condition),
                to_state=str(destination),
                extensions={key: value for key, value in item.items() if key not in {"when", "to"}},
            )
        )
    return tuple(result)


def _string_tuple(raw: Any, path: str, errors: list[str]) -> tuple[str, ...]:
    values = raw if isinstance(raw, list) else [raw]
    if raw is None or not values or any(not isinstance(value, str) or not value for value in values):
        errors.append(f"{path} must be a non-empty string or list of strings")
        return ()
    return tuple(values)


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0
