import { supabase } from './supabase.js'

export default async function handler(req, res) {
  const body = req.body

  const { error } = await supabase
    .from('transactions')
    .delete()
    .eq('id', body.id)

  if (error) return res.status(500).json({ error: error.message })

  return res.status(200).json({ success: true })
}
