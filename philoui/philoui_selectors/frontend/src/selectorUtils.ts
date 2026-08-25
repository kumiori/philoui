export const clamp = (value: number, minimum = 0, maximum = 1): number =>
  Math.min(maximum, Math.max(minimum, value))

export const valueFromPointer = (clientX: number, left: number, width: number): number =>
  width <= 0 ? 0 : clamp((clientX - left) / width)

export const serialiseValue = (value: unknown): string =>
  typeof value === "string" ? value : JSON.stringify(value)
