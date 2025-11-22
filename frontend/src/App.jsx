import React from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'
import { JourneyProvider } from './contexts/JourneyContext'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Header from './components/common/Header'
import Footer from './components/common/Footer'
import ErrorBoundary from './components/common/ErrorBoundary'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ProfilePage from './pages/ProfilePage'
import DocumentsPage from './pages/DocumentsPage'
import CareerAnalysisPage from './pages/CareerAnalysisPage'
import CareerPathwaysPage from './pages/CareerPathwaysPage'
import UpskillingPage from './pages/UpskillingPage'
import ReportPage from './pages/ReportPage'
import KnowledgeBasePage from './pages/KnowledgeBasePage'
import NotFoundPage from './pages/NotFoundPage'
import ProtectedRoute from './components/auth/ProtectedRoute'

// Layout component that conditionally shows header/footer
function Layout({ children }) {
  const location = useLocation()
  const isAuthPage = ['/login', '/register'].includes(location.pathname)

  if (isAuthPage) {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <JourneyProvider>
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
                <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
                <Route path="/documents" element={<ProtectedRoute><DocumentsPage /></ProtectedRoute>} />
                <Route path="/career-analysis" element={<ProtectedRoute><CareerAnalysisPage /></ProtectedRoute>} />
                <Route path="/career-pathways" element={<ProtectedRoute><CareerPathwaysPage /></ProtectedRoute>} />
                <Route path="/upskilling" element={<ProtectedRoute><UpskillingPage /></ProtectedRoute>} />
                <Route path="/reports" element={<ProtectedRoute><ReportPage /></ProtectedRoute>} />
                <Route path="/knowledge-base" element={<ProtectedRoute><KnowledgeBasePage /></ProtectedRoute>} />
                {/* Catch all route - redirect to home */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </Layout>
            <ToastContainer
              position="top-right"
              autoClose={3000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
              className="toast-container"
            />
          </JourneyProvider>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  )
}

export default App
