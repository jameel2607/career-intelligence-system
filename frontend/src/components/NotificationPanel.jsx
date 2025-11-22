import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Bell, Sparkles } from 'lucide-react'

export default function NotificationPanel({ encouragingMessage, alerts = [] }) {
    const [dismissed, setDismissed] = useState(false)

    if (dismissed || (!encouragingMessage && alerts.length === 0)) {
        return null
    }

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-4 mb-6"
            >
                <div className="flex items-start justify-between">
                    <div className="flex items-start flex-1">
                        <div className="bg-gradient-to-r from-purple-500 to-blue-500 text-white p-2 rounded-lg mr-3">
                            <Sparkles className="w-5 h-5" />
                        </div>
                        <div className="flex-1">
                            {encouragingMessage && (
                                <p className="text-gray-900 font-medium">
                                    {encouragingMessage}
                                </p>
                            )}
                            {alerts.length > 0 && (
                                <div className="mt-2 space-y-1">
                                    {alerts.map((alert, index) => (
                                        <div key={index} className="flex items-center text-sm text-gray-700">
                                            <Bell className="w-4 h-4 mr-2 text-purple-500" />
                                            {alert}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                    <button
                        onClick={() => setDismissed(true)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>
            </motion.div>
        </AnimatePresence>
    )
}
