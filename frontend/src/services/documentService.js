import api from './api'

export async function listDocuments(){
  const res = await api.get('/documents/')
  return res.data
}

export async function uploadDocument(file){
  const form = new FormData()
  form.append('file', file)
  const res = await api.post('/documents/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  return res.data
}

export async function ocrDocument(id){
  const res = await api.post(`/documents/${id}/ocr`)
  return res.data
}

