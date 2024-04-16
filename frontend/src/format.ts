export function formatDate(date: string): string {
  const d = new Date(date)
  return `${formatUnit(d.getDate())}.${formatUnit(d.getMonth())}.${formatUnit(d.getFullYear())} ${formatUnit(d.getHours())}:${formatUnit(d.getMinutes())}`
}

function formatUnit(unit: number): string {
  const u = unit.toString()
  return u.length < 2 ? '0' + u : u
}
