import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  TrendingUp,
  Target,
  BookOpen,
  Lightbulb,
  Award,
  AlertCircle,
  CheckCircle,
  ArrowRight,
  Brain,
  Zap,
  Star,
  RefreshCw,
  Shield
} from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import { getScore, getRecommendations, getAIRecommendations } from '../services/careerService'

const ScoreCard = ({ score, breakdown, strengths, improvements }) => {
  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 40) return 'text-orange-600'
    return 'text-red-600'
  }

  const getScoreBg = (score) => {
    if (score >= 70) return 'bg-green-50 border-green-200'
    if (score >= 40) return 'bg-orange-50 border-orange-200'
    return 'bg-red-50 border-red-200'
  }

  const radarData = breakdown ? [
    { subject: 'Soft Skills', A: Math.round((breakdown.soft_skills || 0) * 100), fullMark: 100 },
    { subject: 'Technical', A: Math.round((breakdown.skill_coverage || 0) * 100), fullMark: 100 },
    { subject: 'Practical', A: Math.round((breakdown.practical_evidence || 0) * 100), fullMark: 100 },
    { subject: 'Market Fit', A: Math.round((breakdown.market_factor || 0) * 100), fullMark: 100 },
    { subject: 'Confidence', A: Math.round((breakdown.meta_factor || 0) * 100), fullMark: 100 }
  ] : []

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="text-center mb-6">
        <div className={`inline - flex items - center justify - center w - 24 h - 24 rounded - full border - 4 ${getScoreBg(score)} ${getScoreColor(score)} mb - 4`}>
          <span className="text-3xl font-bold">{score}</span>
        </div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Career Readiness Score</h2>
        <p className={`text - lg font - medium ${getScoreColor(score)} `}>
          {score >= 70 ? 'Job Ready!' : score >= 40 ? 'Progressing Well' : 'Getting Started'}
        </p>
      </div>

      {radarData.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Readiness Profile</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} />
              <Radar
                name="Score"
                dataKey="A"
                stroke="#2563eb"
                fill="#2563eb"
                fillOpacity={0.3}
                strokeWidth={2}
              />
            </RadarChart>
          </ResponsiveContainer>

          {/* Factor Details */}
          <div className="grid grid-cols-3 gap-4 mt-4 text-center">
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="text-xs text-gray-500 uppercase font-semibold">Market Factor</div>
              <div className="text-lg font-bold text-blue-700">{Math.round((breakdown?.market_factor || 0) * 100)}%</div>
            </div>
            <div className="p-3 bg-purple-50 rounded-lg">
              <div className="text-xs text-gray-500 uppercase font-semibold">Meta Factor</div>
              <div className="text-lg font-bold text-purple-700">{Math.round((breakdown?.meta_factor || 0) * 100)}%</div>
            </div>
            <div className="p-3 bg-green-50 rounded-lg">
              <div className="text-xs text-gray-500 uppercase font-semibold">Core Score</div>
              <div className="text-lg font-bold text-green-700">
                {Math.round(((breakdown?.soft_skills || 0) * 0.6 + (breakdown?.skill_coverage || 0) * 0.25 + (breakdown?.practical_evidence || 0) * 0.15) * 100)}%
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {strengths && strengths.length > 0 && (
          <div>
            <h3 className="flex items-center text-lg font-semibold text-green-700 mb-3">
              <CheckCircle className="w-5 h-5 mr-2" />
              Strengths
            </h3>
            <ul className="space-y-2">
              {strengths.map((strength, index) => (
                <li key={index} className="flex items-start text-sm text-gray-700">
                  <Star className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  {strength}
                </li>
              ))}
            </ul>
          </div>
        )}

        {improvements && improvements.length > 0 && (
          <div>
            <h3 className="flex items-center text-lg font-semibold text-orange-700 mb-3">
              <Target className="w-5 h-5 mr-2" />
              Areas to Improve
            </h3>
            <ul className="space-y-2">
              {improvements.map((improvement, index) => (
                <li key={index} className="flex items-start text-sm text-gray-700">
                  <ArrowRight className="w-4 h-4 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                  {improvement}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

const QuickWins = ({ score }) => {
  const quickWins = [
    { action: 'Complete your profile', boost: '+5', time: '10 min', link: '/profile' },
    { action: 'Upload certificates', boost: '+8', time: '15 min', link: '/documents' },
    { action: 'Add LinkedIn profile', boost: '+3', time: '5 min', link: '/profile' },
    { action: 'Take a soft skills course', boost: '+5', time: '2 hours', link: '/upskilling' }
  ]

  return (
    <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl shadow-lg p-6 border border-yellow-200">
      <div className="flex items-center mb-4">
        <Zap className="w-6 h-6 text-yellow-600 mr-2" />
        <h3 className="text-xl font-bold text-gray-900">Quick Wins</h3>
      </div>
      <p className="text-sm text-gray-700 mb-4">Boost your score quickly with these actions</p>
      <div className="space-y-3">
        {quickWins.map((win, index) => (
          <motion.a
            key={index}
            href={win.link}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="block p-3 bg-white rounded-lg hover:shadow-md transition-shadow group"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="font-medium text-gray-900 group-hover:text-blue-600">{win.action}</p>
                <p className="text-xs text-gray-500 mt-1">{win.time}</p>
              </div>
              <div className="flex items-center">
                <span className="text-2xl font-bold text-green-600 mr-2">{win.boost}</span>
                <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          </motion.a>
        ))}
      </div>
    </div>
  )
}

const CompletenessMeters = ({ score }) => {
  const metrics = [
    { label: 'Profile Completeness', value: 75, color: 'bg-blue-600' },
    { label: 'Evidence Trust', value: 60, color: 'bg-green-600' },
    { label: 'Skills Coverage', value: 45, color: 'bg-purple-600' }
  ]

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Completeness Indicators</h3>
      <div className="space-y-4">
        {metrics.map((metric, index) => (
          <div key={index}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">{metric.label}</span>
              <span className="text-sm font-bold text-gray-900">{metric.value}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${metric.value}%` }}
                transition={{ duration: 1, delay: index * 0.2 }}
                className={`h-2 rounded-full ${metric.color}`}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const ConfidenceIndicator = ({ score }) => {
  const confidence = score >= 70 ? 'High' : score >= 40 ? 'Medium' : 'Building'
  const color = score >= 70 ? 'text-green-600' : score >= 40 ? 'text-yellow-600' : 'text-orange-600'
  const bgColor = score >= 70 ? 'bg-green-100' : score >= 40 ? 'bg-yellow-100' : 'bg-orange-100'

  return (
    <div className={`${bgColor} rounded-xl p-6 border-2 ${color.replace('text-', 'border-')}`}>
      <div className="flex items-center mb-3">
        <Shield className="w-6 h-6 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">Confidence Level</h3>
      </div>
      <div className="flex items-center">
        <span className={`text-4xl font-bold ${color}`}>{confidence}</span>
        <div className="ml-4 flex-1">
          <p className="text-sm text-gray-700">
            {score >= 70 && 'You have a strong profile ready for job applications'}
            {score >= 40 && score < 70 && 'Keep building your profile to increase confidence'}
            {score < 40 && 'Focus on completing your profile and adding evidence'}
          </p>
        </div>
      </div>
    </div>
  )
}

const RecommendationCard = ({ title, icon: Icon, recommendations, color = "blue" }) => {
  const colorClasses = {
    blue: "bg-blue-50 border-blue-200 text-blue-700",
    green: "bg-green-50 border-green-200 text-green-700",
    purple: "bg-purple-50 border-purple-200 text-purple-700"
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className={`inline - flex items - center px - 3 py - 1 rounded - full border ${colorClasses[color]} mb - 4`}>
        <Icon className="w-4 h-4 mr-2" />
        <span className="text-sm font-medium">{title}</span>
      </div>

      {recommendations.job_roles && recommendations.job_roles.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Recommended Roles</h3>
          <div className="space-y-2">
            {recommendations.job_roles.slice(0, 5).map((role, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">{role}</span>
                <div className="flex items-center text-sm text-gray-600">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  High Match
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {recommendations.skills_to_learn && recommendations.skills_to_learn.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Skills to Develop</h3>
          <div className="flex flex-wrap gap-2">
            {recommendations.skills_to_learn.slice(0, 8).map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default function CareerAnalysisPage() {
  const [score, setScore] = useState(null)
  const [recs, setRecs] = useState(null)
  const [ai, setAI] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [refreshing, setRefreshing] = useState(false)

  const loadData = async () => {
    try {
      setLoading(true)
      setError('')

      const results = await Promise.allSettled([
        getScore(),
        getRecommendations(),
        getAIRecommendations()
      ])

      const [scoreResult, recsResult, aiResult] = results

      // Handle Score
      if (scoreResult.status === 'fulfilled') {
        setScore(scoreResult.value)
      } else if (scoreResult.reason?.response?.status === 404) {
        // Profile not found - this is expected for new users
        setScore(null)
      } else {
        console.error('Failed to load score:', scoreResult.reason)
      }

      // Handle Recommendations
      if (recsResult.status === 'fulfilled') {
        setRecs(recsResult.value)
      }

      // Handle AI Recommendations
      if (aiResult.status === 'fulfilled') {
        setAI(aiResult.value)
      }

      // If we have no score and it wasn't a 404, set a general error
      if (scoreResult.status === 'rejected' && scoreResult.reason?.response?.status !== 404) {
        setError('Failed to load some data. Please try refreshing.')
      }

    } catch (err) {
      console.error('Unexpected error:', err)
      setError('An unexpected error occurred. Please try again.')
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleRefresh = () => {
    setRefreshing(true)
    loadData()
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing your career readiness...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={handleRefresh}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Analysis</h1>
            <p className="text-gray-600">Comprehensive analysis of your career readiness and recommendations</p>
          </div>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w - 4 h - 4 mr - 2 ${refreshing ? 'animate-spin' : ''} `} />
            Refresh Analysis
          </button>
        </motion.div>

        {/* Score Section */}
        {score && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-8"
          >
            <ScoreCard
              score={score.score}
              breakdown={score.breakdown}
              strengths={score.strengths}
              improvements={score.improvements}
            />
          </motion.div>
        )}

        {/* Recommendations Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {recs && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <RecommendationCard
                title="Algorithm-Based Analysis"
                icon={Zap}
                recommendations={recs}
                color="blue"
              />
            </motion.div>
          )}

          {ai && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <RecommendationCard
                title="AI-Powered Insights"
                icon={Brain}
                recommendations={ai}
                color="purple"
              />
            </motion.div>
          )}
        </div>

        {/* AI Career Path & Insights */}
        {ai && (ai.career_path || ai.market_insights || ai.next_steps) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center mb-6">
              <Lightbulb className="w-6 h-6 text-yellow-500 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">AI Career Guidance</h2>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {ai.career_path && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Career Path</h3>
                  <p className="text-gray-700 text-sm leading-relaxed">{ai.career_path}</p>
                </div>
              )}

              {ai.next_steps && ai.next_steps.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Next Steps</h3>
                  <ul className="space-y-2">
                    {ai.next_steps.slice(0, 4).map((step, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-700">
                        <ArrowRight className="w-4 h-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                        {step}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {ai.market_insights && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Market Insights</h3>
                  <p className="text-gray-700 text-sm leading-relaxed">{ai.market_insights}</p>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8 flex flex-wrap gap-4 justify-center"
        >
          <a
            href="/reports"
            className="flex items-center px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Award className="w-5 h-5 mr-2" />
            Generate Detailed Report
          </a>
          <a
            href="/profile"
            className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <BookOpen className="w-5 h-5 mr-2" />
            Update Profile
          </a>
          <a
            href="/documents"
            className="flex items-center px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Target className="w-5 h-5 mr-2" />
            Upload More Documents
          </a>
        </motion.div>
      </div>
    </div>
  )
}
