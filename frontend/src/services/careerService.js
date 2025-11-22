import api from './api'

export async function getScore(){
  const res = await api.get('/career/score')
  return res.data
}

export async function getRecommendations(){
  const res = await api.get('/career/recommendations')
  return res.data
}

export async function getAIRecommendations(){
  const res = await api.get('/career/ai-recommendations')
  return res.data
}
