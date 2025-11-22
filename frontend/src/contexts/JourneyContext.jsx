import React, { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

const JourneyContext = createContext()

export function JourneyProvider({ children }) {
    const { isAuthenticated } = useAuth()
    const [journeyState, setJourneyState] = useState({
        stage: 1,
        completion: 0,
        nextActions: [],
        encouragingMessage: '',
        canAccessStages: {
            1: true,
            2: false,
            3: false,
            4: false,
            5: false
        },
        loading: false,
        error: null
    })

    const refreshJourney = async () => {
        // Only fetch if user is authenticated
        if (!isAuthenticated) {
            return
        }
        try {
            setJourneyState(prev => ({ ...prev, loading: true, error: null }))
            const response = await api.get('/journey/status')
            setJourneyState({
                ...response.data,
                loading: false,
                error: null
            })
        } catch (error) {
            console.error('Failed to fetch journey status:', error)
            setJourneyState(prev => ({
                ...prev,
                loading: false,
                error: 'Failed to load journey status'
            }))
        }
    }

    useEffect(() => {
        refreshJourney()
    }, [isAuthenticated])

    return (
        <JourneyContext.Provider value={{ ...journeyState, refreshJourney }}>
            {children}
        </JourneyContext.Provider>
    )
}

export const useJourney = () => {
    const context = useContext(JourneyContext)
    if (!context) {
        throw new Error('useJourney must be used within a JourneyProvider')
    }
    return context
}
