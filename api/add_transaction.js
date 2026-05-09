import { supabase } from './supabase.js'

export default async function handler(req, res) {
  const body = req.body

  const { data, error } = await supabase
    .from('transactions')
    .insert({
      title: body.title,
      amount: body.amount,
      category: body.category,
      date: body.date
    })
    .select()

  if (error) return res.status(500).json({ error: error.message })

  return res.status(200).json({ transaction: data })
}
