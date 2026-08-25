import React from "react"
import { ComponentProps, Streamlit } from "streamlit-component-lib"
import SelectorShell, { palette } from "./SelectorShell"
import { serialiseValue } from "./selectorUtils"

export default function ParametricQualitativeSelector(props: ComponentProps) {
  const { label, question } = props.args
  const values: unknown[] = Array.isArray(props.args.data_values) ? props.args.data_values : []

  React.useEffect(() => Streamlit.setFrameHeight(112), [label, question, values.length])

  return (
    <SelectorShell label={label} question={question}>
      <div role="group" aria-label={label || "Choose a region"} style={{ display: "grid", gap: 8, gridTemplateColumns: `repeat(${Math.min(values.length, 4) || 1}, minmax(0, 1fr))` }}>
        {values.map((value, index) => (
          <button
            key={`${index}-${serialiseValue(value)}`}
            type="button"
            onClick={() => Streamlit.setComponentValue(serialiseValue(value))}
            style={{ background: index === values.length - 1 ? palette.text : palette.surface, border: `1px solid ${index === values.length - 1 ? palette.text : "transparent"}`, borderRadius: 8, color: index === values.length - 1 ? "var(--background-color, #fff)" : palette.text, cursor: "pointer", minHeight: 48, overflow: "hidden", padding: "8px 10px", textOverflow: "ellipsis" }}
          >
            {String(value)}
          </button>
        ))}
      </div>
    </SelectorShell>
  )
}
