import React from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, Circle, Lock } from 'lucide-react'

export default function JourneyMilestones({ currentStage, canAccessStages }) {
    const stages = [
        { id: 1, name: 'Profile Onboarding', description: 'Complete your profile' },
        { id: 2, name: 'Upload & Verification', description: 'Add certificates' },
        { id: 3, name: 'CRS Generation', description: 'Get your score' },
        { id: 4, name: 'Pathway Navigation', description: 'Explore careers' },
        { id: 5, name: 'Improvement Actions', description: 'Start upskilling' }
    ]

    const getStageStatus = (stageId) => {
        if (stageId < currentStage) return 'completed'
        if (stageId === currentStage) return 'current'
        if (canAccessStages && canAccessStages[stageId]) return 'unlocked'
        return 'locked'
    }

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Your Journey</h3>

            <div className="space-y-4">
                {stages.map((stage, index) => {
                    const status = getStageStatus(stage.id)
                    const isCompleted = status === 'completed'
                    const isCurrent = status === 'current'
                    const isLocked = status === 'locked'

                    return (
                        <div key={stage.id} className="relative">
                            {/* Connector Line */}
                            {index < stages.length - 1 && (
                                <div
                                    className={`absolute left-5 top-12 w-0.5 h-8 ${isCompleted ? 'bg-green-500' : 'bg-gray-300'
                                        }`}
                                />
                            )}

                            {/* Stage Item */}
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`flex items-start p-3 rounded-lg transition-colors ${isCurrent ? 'bg-blue-50 border-2 border-blue-500' : 'hover:bg-gray-50'
                                    }`}
                            >
                                {/* Icon */}
                                <div className="flex-shrink-0 mr-3">
                                    {isCompleted && (
                                        <CheckCircle className="w-10 h-10 text-green-500" />
                                    )}
                                    {isCurrent && (
                                        <Circle className="w-10 h-10 text-blue-500 fill-blue-100" />
                                    )}
                                    {isLocked && (
                                        <Lock className="w-10 h-10 text-gray-400" />
                                    )}
                                </div>

                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex items-center">
                                        <span className="text-xs font-semibold text-gray-500 mr-2">
                                            STAGE {stage.id}
                                        </span>
                                        {isCurrent && (
                                            <span className="px-2 py-0.5 text-xs font-semibold text-blue-700 bg-blue-100 rounded-full">
                                                Current
                                            </span>
                                        )}
                                    </div>
                                    <h4 className={`font-semibold mt-1 ${isLocked ? 'text-gray-400' : 'text-gray-900'
                                        }`}>
                                        {stage.name}
                                    </h4>
                                    <p className={`text-sm mt-0.5 ${isLocked ? 'text-gray-400' : 'text-gray-600'
                                        }`}>
                                        {stage.description}
                                    </p>
                                </div>
                            </motion.div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
