import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
    BookOpen,
    TrendingUp,
    Award,
    Clock,
    Star,
    CheckCircle,
    Play,
    Filter,
    Search
} from 'lucide-react'
import api from '../services/api'

const CourseCard = ({ course, onEnroll, delay = 0 }) => {
    const [enrolled, setEnrolled] = useState(false)

    const handleEnroll = () => {
        setEnrolled(true)
        if (onEnroll) onEnroll(course)
    }

    const categoryColors = {
        soft_skill: 'bg-blue-100 text-blue-700',
        domain: 'bg-purple-100 text-purple-700',
        project: 'bg-green-100 text-green-700'
    }

    const difficultyColors = {
        beginner: 'text-green-600',
        intermediate: 'text-yellow-600',
        advanced: 'text-red-600'
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay, duration: 0.5 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow"
        >
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${categoryColors[course.category] || 'bg-gray-100 text-gray-700'}`}>
                            {course.category?.replace('_', ' ').toUpperCase()}
                        </span>
                        <span className={`text-xs font-medium ${difficultyColors[course.difficulty] || 'text-gray-600'}`}>
                            {course.difficulty?.charAt(0).toUpperCase() + course.difficulty?.slice(1)}
                        </span>
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 mb-1">{course.title}</h3>
                </div>
                {course.score_impact && (
                    <div className="text-right">
                        <div className="text-2xl font-bold text-green-600">+{course.score_impact}</div>
                        <div className="text-xs text-gray-500">Score Boost</div>
                    </div>
                )}
            </div>

            <p className="text-sm text-gray-700 mb-4 line-clamp-2">
                {course.description || 'Enhance your skills with this comprehensive course'}
            </p>

            <div className="flex items-center gap-4 mb-4 text-sm text-gray-600">
                <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    {course.duration_hours || 10}h
                </div>
                <div className="flex items-center">
                    <Award className="w-4 h-4 mr-1" />
                    {course.provider || 'Online Platform'}
                </div>
            </div>

            {course.target_component && (
                <div className="mb-4 p-2 bg-yellow-50 rounded-lg">
                    <p className="text-xs text-yellow-800">
                        <strong>Improves:</strong> {course.target_component.replace('_', ' ')}
                    </p>
                </div>
            )}

            {enrolled ? (
                <div className="flex items-center justify-center px-4 py-2 bg-green-50 text-green-700 font-medium rounded-lg">
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Enrolled
                </div>
            ) : (
                <button
                    onClick={handleEnroll}
                    className="w-full flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
                >
                    <Play className="w-4 h-4 mr-2" />
                    Start Learning
                </button>
            )}
        </motion.div>
    )
}

export default function UpskillingPage() {
    const [courses, setCourses] = useState([])
    const [filteredCourses, setFilteredCourses] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('all')
    const [searchQuery, setSearchQuery] = useState('')

    useEffect(() => {
        async function loadCourses() {
            try {
                setLoading(true)

                // Mock courses data (in production, this would come from API)
                const mockCourses = [
                    // Soft Skills
                    {
                        id: 1,
                        title: 'Effective Communication Skills',
                        category: 'soft_skill',
                        description: 'Master verbal and written communication for professional success',
                        duration_hours: 8,
                        score_impact: 5,
                        target_component: 'soft_skills',
                        difficulty: 'beginner',
                        provider: 'Coursera',
                        is_active: true
                    },
                    {
                        id: 2,
                        title: 'Leadership & Team Management',
                        category: 'soft_skill',
                        description: 'Develop leadership skills and learn to manage teams effectively',
                        duration_hours: 12,
                        score_impact: 6,
                        target_component: 'soft_skills',
                        difficulty: 'intermediate',
                        provider: 'LinkedIn Learning',
                        is_active: true
                    },
                    {
                        id: 3,
                        title: 'Time Management & Productivity',
                        category: 'soft_skill',
                        description: 'Optimize your workflow and boost productivity',
                        duration_hours: 6,
                        score_impact: 4,
                        target_component: 'soft_skills',
                        difficulty: 'beginner',
                        provider: 'Udemy',
                        is_active: true
                    },
                    {
                        id: 4,
                        title: 'Problem Solving & Critical Thinking',
                        category: 'soft_skill',
                        description: 'Enhance analytical and problem-solving abilities',
                        duration_hours: 10,
                        score_impact: 5,
                        target_component: 'soft_skills',
                        difficulty: 'intermediate',
                        provider: 'edX',
                        is_active: true
                    },
                    // Domain Skills
                    {
                        id: 5,
                        title: 'Python for Data Science',
                        category: 'domain',
                        description: 'Learn Python programming for data analysis and machine learning',
                        duration_hours: 40,
                        score_impact: 10,
                        target_component: 'technical_skills',
                        difficulty: 'intermediate',
                        provider: 'DataCamp',
                        is_active: true
                    },
                    {
                        id: 6,
                        title: 'Full Stack Web Development',
                        category: 'domain',
                        description: 'Master frontend and backend web development technologies',
                        duration_hours: 60,
                        score_impact: 12,
                        target_component: 'technical_skills',
                        difficulty: 'advanced',
                        provider: 'freeCodeCamp',
                        is_active: true
                    },
                    {
                        id: 7,
                        title: 'Cloud Computing with AWS',
                        category: 'domain',
                        description: 'Learn cloud infrastructure and services with Amazon Web Services',
                        duration_hours: 30,
                        score_impact: 8,
                        target_component: 'technical_skills',
                        difficulty: 'intermediate',
                        provider: 'AWS Training',
                        is_active: true
                    },
                    {
                        id: 8,
                        title: 'Machine Learning Fundamentals',
                        category: 'domain',
                        description: 'Introduction to ML algorithms and practical applications',
                        duration_hours: 35,
                        score_impact: 10,
                        target_component: 'technical_skills',
                        difficulty: 'intermediate',
                        provider: 'Coursera',
                        is_active: true
                    },
                    // Projects
                    {
                        id: 9,
                        title: 'Build a Portfolio Website',
                        category: 'project',
                        description: 'Create a professional portfolio to showcase your work',
                        duration_hours: 15,
                        score_impact: 7,
                        target_component: 'projects',
                        difficulty: 'beginner',
                        provider: 'YouTube Tutorial',
                        is_active: true
                    },
                    {
                        id: 10,
                        title: 'Data Analysis Project',
                        category: 'project',
                        description: 'Complete end-to-end data analysis project with real datasets',
                        duration_hours: 20,
                        score_impact: 8,
                        target_component: 'projects',
                        difficulty: 'intermediate',
                        provider: 'Kaggle',
                        is_active: true
                    }
                ]

                setCourses(mockCourses)
                setFilteredCourses(mockCourses)
            } catch (err) {
                console.error('Failed to load courses:', err)
                setError('Failed to load courses')
            } finally {
                setLoading(false)
            }
        }
        loadCourses()
    }, [])

    useEffect(() => {
        let filtered = courses

        if (selectedCategory !== 'all') {
            filtered = filtered.filter(course => course.category === selectedCategory)
        }

        if (searchQuery) {
            filtered = filtered.filter(course =>
                course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                course.description.toLowerCase().includes(searchQuery.toLowerCase())
            )
        }

        setFilteredCourses(filtered)
    }, [selectedCategory, searchQuery, courses])

    const handleEnroll = (course) => {
        console.log('Enrolled in:', course.title)
        // In production, this would call the API to enroll the user
    }

    const categories = [
        { id: 'all', label: 'All Courses', count: courses.length },
        { id: 'soft_skill', label: 'Soft Skills', count: courses.filter(c => c.category === 'soft_skill').length },
        { id: 'domain', label: 'Domain Skills', count: courses.filter(c => c.category === 'domain').length },
        { id: 'project', label: 'Projects', count: courses.filter(c => c.category === 'project').length }
    ]

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading courses...</p>
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
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Upskilling & Courses</h1>
                    <p className="text-gray-600">
                        Boost your career score with recommended courses and projects
                    </p>
                </motion.div>

                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                        {error}
                    </div>
                )}

                <div className="mb-8 flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search courses..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>
                    <div className="flex gap-2 flex-wrap">
                        {categories.map((category) => (
                            <button
                                key={category.id}
                                onClick={() => setSelectedCategory(category.id)}
                                className={`px-4 py-2 rounded-lg font-medium transition-all ${selectedCategory === category.id
                                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                                    }`}
                            >
                                {category.label} ({category.count})
                            </button>
                        ))}
                    </div>
                </div>

                {filteredCourses.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredCourses.map((course, index) => (
                            <CourseCard
                                key={course.id}
                                course={course}
                                onEnroll={handleEnroll}
                                delay={index * 0.1}
                            />
                        ))}
                    </div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-12 bg-white rounded-xl shadow-lg"
                    >
                        <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">
                            No courses found
                        </h3>
                        <p className="text-gray-600">
                            Try adjusting your search or filter criteria
                        </p>
                    </motion.div>
                )}
            </div>
        </div>
    )
}
