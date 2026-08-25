import React from "react"
import { ComponentProps, Streamlit } from "streamlit-component-lib"
import SelectorShell, { palette } from "./SelectorShell"
import { serialiseValue } from "./selectorUtils"

export default function QualitativeSelector(props: ComponentProps) {
  const { label, question } = props.args
  const values: unknown[] = Array.isArray(props.args.data_values) ? props.args.data_values : []

  React.useEffect(() => Streamlit.setFrameHeight(106), [label, question, values.length])

  return (
    <SelectorShell label={label} question={question}>
      <div role="group" aria-label={label || "Choose a level"} style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {values.map((value, index) => (
          <button
            key={`${index}-${serialiseValue(value)}`}
            type="button"
            onClick={() => Streamlit.setComponentValue(serialiseValue(value))}
            style={{ background: "transparent", border: `1px solid ${palette.text}`, borderRadius: 999, color: palette.text, cursor: "pointer", flex: "1 1 80px", minHeight: 42, padding: "8px 16px" }}
          >
            {String(value)}
          </button>
        ))}
      </div>
    </SelectorShell>
  )
}
