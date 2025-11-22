import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  User,
  FileText,
  TrendingUp,
  Award,
  Database,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  Clock,
  BarChart3
} from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'
import api from '../services/api'
import { useJourney } from '../contexts/JourneyContext'
import ProgressTracker from '../components/ProgressTracker'
import JourneyMilestones from '../components/JourneyMilestones'
import SmartCTAs from '../components/SmartCTAs'
import NotificationPanel from '../components/NotificationPanel'

const StatCard = ({ icon: Icon, title, value, subtitle, color, href, delay = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.5 }}
    className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
  >
    <div className="flex items-center justify-between mb-4">
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <ArrowRight className="w-5 h-5 text-gray-400" />
    </div>
    <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
    <p className="text-gray-600 text-sm mb-3">{title}</p>
    <p className="text-xs text-gray-500">{subtitle}</p>
    {href && (
      <a
        href={href}
        className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-800 font-medium text-sm"
      >
        View Details <ArrowRight className="w-4 h-4 ml-1" />
      </a>
    )}
  </motion.div>
)

const ScoreGauge = ({ score }) => {
  const data = [
    { name: 'Score', value: score, fill: score >= 70 ? '#10b981' : score >= 40 ? '#f59e0b' : '#ef4444' },
    { name: 'Remaining', value: 100 - score, fill: '#e5e7eb' }
  ]

  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            startAngle={180}
            endAngle={0}
            innerRadius={60}
            outerRadius={80}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl font-bold text-gray-900">{score}</div>
          <div className="text-sm text-gray-600">Career Score</div>
        </div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  // Journey context
  const journey = useJourney()

  const [data, setData] = useState({
    profile: false,
    docs: 0,
    reports: 0,
    score: null,
    breakdown: null,
    recentActivity: []
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const [p, d, s, r] = await Promise.all([
          api.get('/students/me').catch(() => ({ data: null })),
          api.get('/documents/').catch(() => ({ data: [] })),
          api.get('/career/score').catch(() => ({ data: null })),
          api.get('/reports/').catch(() => ({ data: [] })),
        ])

        setData({
          profile: !!p.data,
          docs: (d.data || []).length,
          reports: (r.data || []).length,
          score: s.data?.score ?? null,
          breakdown: s.data?.breakdown || null,
          recentActivity: [
            { action: 'Profile Updated', time: '2 hours ago', status: 'completed' },
            { action: 'Documents Uploaded', time: '1 day ago', status: 'completed' },
            { action: 'Career Analysis', time: '3 days ago', status: 'pending' }
          ]
        })
      } catch (err) {
        setError('Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Intelligence Dashboard</h1>
          <p className="text-gray-600">Track your career readiness and development progress</p>
        </motion.div>

        {/* Journey Progress Tracker */}
        {!journey.loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <ProgressTracker
              percentage={journey.completion}
              stage={journey.stage}
            />
          </motion.div>
        )}

        {/* Notification Panel */}
        {!journey.loading && journey.encouragingMessage && (
          <NotificationPanel
            encouragingMessage={journey.encouragingMessage}
          />
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={User}
            title="Profile Status"
            value={data.profile ? "Complete" : "Incomplete"}
            subtitle={data.profile ? "All sections filled" : "Complete your profile"}
            color={data.profile ? "bg-green-500" : "bg-orange-500"}
            href="/profile"
            delay={0.1}
          />
          <StatCard
            icon={FileText}
            title="Documents"
            value={data.docs}
            subtitle={`${data.docs} files uploaded`}
            color="bg-blue-500"
            href="/documents"
            delay={0.2}
          />
          <StatCard
            icon={TrendingUp}
            title="Career Score"
            value={data.score !== null ? `${data.score}/100` : "N/A"}
            subtitle={data.score !== null ? "Career readiness" : "Generate your score"}
            color={data.score >= 70 ? "bg-green-500" : data.score >= 40 ? "bg-orange-500" : "bg-red-500"}
            href="/career-analysis"
            delay={0.3}
          />
          <StatCard
            icon={Award}
            title="Reports"
            value={data.reports}
            subtitle={`${data.reports} reports generated`}
            color="bg-purple-500"
            href="/reports"
            delay={0.4}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Career Score Visualization */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="lg:col-span-2 bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Career Readiness Analysis</h2>
              <BarChart3 className="w-5 h-5 text-gray-400" />
            </div>

            {data.score !== null ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <ScoreGauge score={data.score} />
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Score Breakdown</h3>
                  {data.breakdown && (
                    <div className="space-y-3">
                      {Object.entries(data.breakdown)
                        .filter(([key]) => key.endsWith('_score'))
                        .map(([key, value]) => {
                          const label = key.replace('_score', '').replace('_', ' ')
                          const percentage = Math.round(value * 100)
                          return (
                            <div key={key} className="flex items-center justify-between">
                              <span className="text-sm text-gray-600 capitalize">{label}</span>
                              <div className="flex items-center space-x-2">
                                <div className="w-20 bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: `${percentage}%` }}
                                  ></div>
                                </div>
                                <span className="text-sm font-medium text-gray-900">{percentage}%</span>
                              </div>
                            </div>
                          )
                        })}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Career Analysis Yet</h3>
                <p className="text-gray-600 mb-6">Complete your profile and upload documents to get your career readiness score</p>
                <a
                  href="/career-analysis"
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Start Analysis <ArrowRight className="w-4 h-4 ml-2" />
                </a>
              </div>
            )}
          </motion.div>

          {/* Journey Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="space-y-6"
          >
            {/* Journey Milestones */}
            {!journey.loading && (
              <JourneyMilestones
                currentStage={journey.stage}
                canAccessStages={journey.canAccessStages}
              />
            )}

            {/* Smart CTAs */}
            {!journey.loading && journey.nextActions && journey.nextActions.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <SmartCTAs nextActions={journey.nextActions} />
              </div>
            )}
          </motion.div>
        </div>

        {/* Knowledge Base Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mt-8 bg-white rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <Database className="w-6 h-6 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Knowledge Base</h2>
            </div>
            <a
              href="/knowledge-base"
              className="text-blue-600 hover:text-blue-800 font-medium text-sm"
            >
              Explore All Roles
            </a>
          </div>
          <p className="text-gray-600 mb-4">
            Explore our comprehensive database of career paths, skills, and market insights to guide your professional development.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">26+</div>
              <div className="text-sm text-gray-600">Job Roles</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">7</div>
              <div className="text-sm text-gray-600">Industry Clusters</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">17</div>
              <div className="text-sm text-gray-600">Job Families</div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
