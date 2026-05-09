import { supabase } from './supabase.js'

// Helper: get current YYYY-MM
function currentMonth() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

// Helper: subtract 2 months from YYYY-MM
function subtractTwoMonths(ym) {
  let [y, m] = ym.split('-').map(Number)
  m -= 2
  if (m <= 0) {
    m += 12
    y -= 1
  }
  return `${y}-${String(m).padStart(2, '0')}`
}

export default async function handler(req, res) {
  const query = req.query || {}

  let start = query.start
  let end = query.end || currentMonth()

  // If no start provided → default to 2 months before end
  if (!start) {
    start = subtractTwoMonths(end)
  }

  // Build date range
  const startDate = `${start}-01`
  const endDate = `${end}-31`

  const { data, error } = await supabase
    .from('transactions')
    .select('*')
    .gte('date', startDate)
    .lte('date', endDate)
    .order('date', { ascending: false })

  if (error) {
    return res.status(500).json({ error: error.message })
  }

  return res.status(200).json({ transactions: data })
}
