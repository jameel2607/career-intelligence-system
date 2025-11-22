import api from './api'

export async function getMe(){
  const res = await api.get('/students/me')
  return res.data
}

export async function createMe(data){
  const res = await api.post('/students/me', data)
  return res.data
}

export async function updateMe(data){
  const res = await api.put('/students/me', data)
  return res.data
}

