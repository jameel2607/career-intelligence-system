import api from './api'

export async function listReports(){
  const res = await api.get('/reports/')
  return res.data
}

export async function generateReport(){
  const res = await api.post('/reports/generate')
  return res.data
}

export async function downloadReport(id){
  const res = await api.get(`/reports/${id}/download`, { responseType: 'blob' })
  return res.data
}

