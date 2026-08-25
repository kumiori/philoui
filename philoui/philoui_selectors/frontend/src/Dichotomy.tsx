import React from "react"
import { ComponentProps, Streamlit } from "streamlit-component-lib"
import SelectorShell, { palette } from "./SelectorShell"
import { valueFromPointer } from "./selectorUtils"

export default function Dichotomy(props: ComponentProps) {
  const { label, question } = props.args
  const gradientWidth = Math.max(0, Math.min(100, Number(props.args.gradientWidth ?? 40)))
  const invert = Boolean(props.args.invert)
  const height = Math.max(44, Math.min(160, Number(props.args.height ?? 80)))
  const dark = invert ? "#ffffff" : "#111111"
  const light = invert ? "#111111" : "#ffffff"
  const edge = (100 - gradientWidth) / 2
  const background = gradientWidth === 0
    ? `linear-gradient(90deg, ${dark} 0 50%, ${light} 50% 100%)`
    : `linear-gradient(90deg, ${dark} 0 ${edge}%, ${light} ${100 - edge}% 100%)`

  React.useEffect(() => Streamlit.setFrameHeight(height + 72), [height, label, question])

  const choose = (event: React.MouseEvent<HTMLButtonElement>) => {
    const rect = event.currentTarget.getBoundingClientRect()
    Streamlit.setComponentValue(valueFromPointer(event.clientX, rect.left, rect.width).toFixed(2))
  }

  return (
    <SelectorShell label={label} question={question}>
      <button
        type="button"
        aria-label={label || "Choose a position"}
        onClick={choose}
        style={{ background, border: `1px solid ${palette.surface}`, borderRadius: 10, cursor: "crosshair", display: "block", height, padding: 0, width: "100%" }}
      />
      <div aria-hidden="true" style={{ display: "flex", fontSize: 12, justifyContent: "space-between", marginTop: 6, opacity: 0.7 }}>
        <span>0</span><span>1</span>
      </div>
    </SelectorShell>
  )
}
