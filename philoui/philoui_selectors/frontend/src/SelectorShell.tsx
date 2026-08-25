import React, { ReactNode } from "react"

type Props = { label?: string; question?: string; children: ReactNode }

export const palette = {
  text: "var(--text-color, #31333f)",
  surface: "var(--secondary-background-color, #f0f2f6)",
}

export default function SelectorShell({ label, question, children }: Props) {
  return (
    <section style={{ color: palette.text, fontFamily: "var(--font, sans-serif)", padding: "2px 4px 10px" }}>
      {label && <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{label}</div>}
      {question && <div style={{ fontSize: 14, lineHeight: 1.4, marginBottom: 14 }}>{question}</div>}
      {children}
    </section>
  )
}
