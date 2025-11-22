import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, AlertCircle, Info, CheckCircle } from 'lucide-react'

export default function SmartCTAs({ nextActions }) {
    if (!nextActions || nextActions.length === 0) {
        return (
            <div className="bg-green-50 border border-green-200 rounded-xl p-6">
                <div className="flex items-center">
                    <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
                    <div>
                        <h3 className="font-semibold text-green-900">All caught up!</h3>
                        <p className="text-sm text-green-700">You've completed all recommended actions.</p>
                    </div>
                </div>
            </div>
        )
    }

    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'high':
                return 'from-red-500 to-orange-500'
            case 'medium':
                return 'from-yellow-500 to-amber-500'
            case 'low':
                return 'from-blue-500 to-cyan-500'
            default:
                return 'from-gray-500 to-gray-600'
        }
    }

    const getPriorityIcon = (priority) => {
        switch (priority) {
            case 'high':
                return <AlertCircle className="w-5 h-5" />
            case 'medium':
                return <Info className="w-5 h-5" />
            default:
                return <CheckCircle className="w-5 h-5" />
        }
    }

    return (
        <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Next Steps</h3>

            {nextActions.map((action, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                >
                    <Link
                        to={action.link}
                        className="block group"
                    >
                        <div className={`bg-gradient-to-r ${getPriorityColor(action.priority)} p-0.5 rounded-xl hover:shadow-lg transition-shadow`}>
                            <div className="bg-white rounded-xl p-4 hover:bg-gray-50 transition-colors">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start flex-1">
                                        <div className={`bg-gradient-to-r ${getPriorityColor(action.priority)} text-white p-2 rounded-lg mr-3`}>
                                            {getPriorityIcon(action.priority)}
                                        </div>
                                        <div className="flex-1">
                                            <h4 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                                                {action.title}
                                            </h4>
                                            <p className="text-sm text-gray-600 mt-1">
                                                {action.description}
                                            </p>
                                            {action.priority === 'high' && (
                                                <span className="inline-block mt-2 px-2 py-1 text-xs font-semibold text-red-700 bg-red-100 rounded-full">
                                                    High Priority
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0 ml-2" />
                                </div>
                            </div>
                        </div>
                    </Link>
                </motion.div>
            ))}
        </div>
    )
}
