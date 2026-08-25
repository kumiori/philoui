import { clamp, serialiseValue, valueFromPointer } from "./selectorUtils"

test("clamp keeps values in the unit interval", () => {
  expect(clamp(-0.2)).toBe(0)
  expect(clamp(0.45)).toBe(0.45)
  expect(clamp(1.2)).toBe(1)
})

test("pointer values use viewport coordinates consistently", () => {
  expect(valueFromPointer(100, 100, 400)).toBe(0)
  expect(valueFromPointer(300, 100, 400)).toBe(0.5)
  expect(valueFromPointer(500, 100, 400)).toBe(1)
  expect(valueFromPointer(600, 100, 400)).toBe(1)
})

test("values are serialised without changing labels", () => {
  expect(serialiseValue("inside")).toBe("inside")
  expect(serialiseValue(100)).toBe("100")
})
