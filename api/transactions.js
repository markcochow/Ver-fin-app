import { supabase } from './supabase.js'

export default async function handler(req, res) {
  const { data, error } = await supabase
    .from('transactions')
    .select('*')
    .order('date', { ascending: false })

  if (error) return res.status(500).json({ error: error.message })

  return res.status(200).json({ transactions: data })
}
