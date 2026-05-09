import { supabase } from './supabase.js'

export default async function handler(req, res) {
  const { data, error } = await supabase
    .from('transactions')
    .select('*')

  if (error) return res.status(500).json({ error: error.message })

  let income = 0
  let expense = 0

  data.forEach(t => {
    if (t.amount >= 0) income += t.amount
    else expense += Math.abs(t.amount)
  })

  const balance = income - expense

  return res.status(200).json({
    income,
    expense,
    balance
  })
}

