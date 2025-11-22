import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
    Briefcase,
    GraduationCap,
    Rocket,
    TrendingUp,
    DollarSign,
    Award,
    CheckCircle,
    ArrowRight,
    Star,
    Target
} from 'lucide-react'
import api from '../services/api'

const TabButton = ({ active, onClick, icon: Icon, label }) => (
    <button
        onClick={onClick}
        className={`flex items-center px-6 py-3 font-medium rounded-lg transition-all ${active
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
    >
        <Icon className="w-5 h-5 mr-2" />
        {label}
    </button>
)

const RoleCard = ({ role, delay = 0 }) => {
    const matchPercentage = role.skill_match || 75
    const matchColor = matchPercentage >= 80 ? 'text-green-600' : matchPercentage >= 60 ? 'text-yellow-600' : 'text-orange-600'

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay, duration: 0.5 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow"
        >
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-1">{role.title}</h3>
                    <p className="text-sm text-gray-600">{role.category || 'Technology'}</p>
                </div>
                <div className="text-right">
                    <div className={`text-2xl font-bold ${matchColor}`}>{matchPercentage}%</div>
                    <div className="text-xs text-gray-500">Match</div>
                </div>
            </div>

            <div className="flex items-center mb-4 p-3 bg-green-50 rounded-lg">
                <DollarSign className="w-5 h-5 text-green-600 mr-2" />
                <div>
                    <div className="text-sm font-medium text-gray-900">
                        ₹{role.salary_min || '4'} - ₹{role.salary_max || '8'} LPA
                    </div>
                    <div className="text-xs text-gray-600">Expected Salary Range</div>
                </div>
            </div>

            <p className="text-sm text-gray-700 mb-4 line-clamp-3">
                {role.description || 'Exciting opportunity to work with cutting-edge technologies and make an impact.'}
            </p>

            <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900 mb-2">Required Skills</h4>
                <div className="flex flex-wrap gap-2">
                    {(role.required_skills || ['Python', 'React', 'SQL']).slice(0, 5).map((skill, index) => (
                        <span
                            key={index}
                            className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded-full"
                        >
                            {skill}
                        </span>
                    ))}
                </div>
            </div>

            {role.certifications && role.certifications.length > 0 && (
                <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center">
                        <Award className="w-4 h-4 mr-1" />
                        Recommended Certifications
                    </h4>
                    <ul className="space-y-1">
                        {role.certifications.slice(0, 2).map((cert, index) => (
                            <li key={index} className="text-xs text-gray-600 flex items-center">
                                <CheckCircle className="w-3 h-3 mr-1 text-green-500" />
                                {cert}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            <div className="mb-4 p-3 bg-purple-50 rounded-lg">
                <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center">
                    <Target className="w-4 h-4 mr-1 text-purple-600" />
                    Quick Start (2-3 Days)
                </h4>
                <ul className="space-y-1">
                    {(role.quick_tasks || [
                        'Complete online course on fundamentals',
                        'Build a small project',
                        'Update resume with relevant skills'
                    ]).slice(0, 3).map((task, index) => (
                        <li key={index} className="text-xs text-gray-700 flex items-start">
                            <span className="text-purple-600 mr-1">•</span>
                            {task}
                        </li>
                    ))}
                </ul>
            </div>

            <button className="w-full flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all">
                View Full Details
                <ArrowRight className="w-4 h-4 ml-2" />
            </button>
        </motion.div>
    )
}

export default function CareerPathwaysPage() {
    const [activeTab, setActiveTab] = useState('primary')
    const [pathways, setPathways] = useState({
        primary: [],
        alternate: [],
        higher_studies: [],
        entrepreneurship: []
    })
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function loadPathways() {
            try {
                setLoading(true)
                const response = await api.get('/recommendations')
                const roles = response.data.recommendations || []

                setPathways({
                    primary: roles.slice(0, 3),
                    alternate: roles.slice(3, 6),
                    higher_studies: [{
                        title: 'Master of Computer Science',
                        category: 'Higher Education',
                        description: 'Advanced degree focusing on computer science fundamentals',
                        salary_min: '8',
                        salary_max: '15',
                        skill_match: 85,
                        required_skills: ['Programming', 'Mathematics', 'Research'],
                        certifications: ['GRE', 'TOEFL/IELTS'],
                        quick_tasks: ['Research universities', 'Prepare for GRE', 'Draft SOP']
                    }],
                    entrepreneurship: [{
                        title: 'Tech Startup Founder',
                        category: 'Entrepreneurship',
                        description: 'Build and scale your own technology business',
                        salary_min: 'Variable',
                        salary_max: 'Unlimited',
                        skill_match: 70,
                        required_skills: ['Leadership', 'Product Development', 'Strategy'],
                        certifications: ['Startup Accelerator Programs'],
                        quick_tasks: ['Validate idea', 'Build MVP', 'Network with investors']
                    }]
                })
            } catch (err) {
                console.error('Failed to load pathways:', err)
                setError('Failed to load career pathways')
            } finally {
                setLoading(false)
            }
        }
        loadPathways()
    }, [])

    const tabs = [
        { id: 'primary', label: 'Primary Roles', icon: Briefcase },
        { id: 'alternate', label: 'Alternate Paths', icon: TrendingUp },
        { id: 'higher_studies', label: 'Higher Studies', icon: GraduationCap },
        { id: 'entrepreneurship', label: 'Entrepreneurship', icon: Rocket }
    ]

    const currentPathways = pathways[activeTab] || []

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading career pathways...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Pathways</h1>
                    <p className="text-gray-600">
                        Explore personalized career paths based on your profile and skills
                    </p>
                </motion.div>

                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                        {error}
                    </div>
                )}

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="mb-8 flex flex-wrap gap-4"
                >
                    {tabs.map((tab) => (
                        <TabButton
                            key={tab.id}
                            active={activeTab === tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            icon={tab.icon}
                            label={tab.label}
                        />
                    ))}
                </motion.div>

                {currentPathways.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {currentPathways.map((role, index) => (
                            <RoleCard key={index} role={role} delay={index * 0.1} />
                        ))}
                    </div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-12 bg-white rounded-xl shadow-lg"
                    >
                        <Star className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">
                            No pathways available yet
                        </h3>
                        <p className="text-gray-600">
                            Complete your profile and generate your career score to see personalized pathways
                        </p>
                    </motion.div>
                )}
            </div>
        </div>
    )
}
