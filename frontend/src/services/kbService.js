import api from './api'

export async function kbUpload(file){
  const form = new FormData()
  form.append('file', file)
  const res = await api.post('/kb/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  return res.data
}

export async function kbSearch(query, limit=5){
  const res = await api.post('/kb/search', { query, limit })
  return res.data
}

export async function kbRefresh(){
  const res = await api.post('/kb/refresh')
  return res.data
}

export async function kbGetAll(){
  const res = await api.get('/kb/all')
  return res.data
}

export async function kbDeleteEntry(entryId){
  const res = await api.delete(`/kb/entry/${entryId}`)
  return res.data
}

