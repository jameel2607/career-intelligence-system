import React from 'react'
import { motion } from 'framer-motion'

export default function ProgressTracker({ percentage, stage }) {
    const radius = 70
    const circumference = 2 * Math.PI * radius
    const offset = circumference - (percentage / 100) * circumference

    return (
        <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between">
                {/* Progress Circle */}
                <div className="relative">
                    <svg className="transform -rotate-90" width="160" height="160">
                        {/* Background circle */}
                        <circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="rgba(255, 255, 255, 0.2)"
                            strokeWidth="12"
                            fill="none"
                        />
                        {/* Progress circle */}
                        <motion.circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="white"
                            strokeWidth="12"
                            fill="none"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                            strokeLinecap="round"
                            initial={{ strokeDashoffset: circumference }}
                            animate={{ strokeDashoffset: offset }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                        />
                    </svg>
                    {/* Percentage Text */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <motion.span
                            className="text-4xl font-bold"
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5 }}
                        >
                            {Math.round(percentage)}%
                        </motion.span>
                        <span className="text-sm opacity-90">Complete</span>
                    </div>
                </div>

                {/* Info */}
                <div className="flex-1 ml-6">
                    <h3 className="text-2xl font-bold mb-2">Profile Completion</h3>
                    <p className="text-blue-100 mb-4">
                        You're on Stage {stage} of 5
                    </p>

                    {/* Progress Bar */}
                    <div className="w-full bg-white/20 rounded-full h-2 mb-2">
                        <motion.div
                            className="bg-white h-2 rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${percentage}%` }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                        />
                    </div>

                    <p className="text-sm text-blue-100">
                        {percentage < 30 && "Just getting started! Keep going 🚀"}
                        {percentage >= 30 && percentage < 60 && "Great progress! You're doing well 💪"}
                        {percentage >= 60 && percentage < 90 && "Almost there! Keep it up 🌟"}
                        {percentage >= 90 && "Excellent! You're nearly done ✨"}
                    </p>
                </div>
            </div>
        </div>
    )
}
