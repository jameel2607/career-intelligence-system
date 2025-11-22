import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Database, 
  Upload, 
  Search, 
  RefreshCw, 
  FileText,
  Brain,
  CheckCircle,
  AlertCircle,
  Loader2,
  Star,
  Trash2
} from 'lucide-react'
import { kbUpload, kbSearch, kbRefresh, kbGetAll, kbDeleteEntry } from '../services/kbService'
import { toast } from 'react-toastify'

export default function KnowledgeBasePage(){
  const [results, setResults] = useState([])
  const [query, setQuery] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [showSearch, setShowSearch] = useState(false)
  const [deleting, setDeleting] = useState(null)

  const onUpload = async (e) => {
    const file = e.target.files?.[0]
    if(!file) return
    
    setMessage('')
    setUploading(true)
    try {
      const r = await kbUpload(file)
      setMessage(`✅ Uploaded ${r.filename}: ${r.rows} rows, ${r.columns} columns (${Math.round(r.size/1024)} KB)`)
      setUploadedFile({
        name: file.name,
        size: file.size,
        uploadedAt: new Date().toISOString(),
        rows: r.rows,
        columns: r.columns
      })
      toast.success(`Successfully uploaded ${r.rows} knowledge base entries!`)
      // Reload all data after upload
      loadAllData()
    } catch(err) {
      const errorMsg = err.response?.data?.detail || 'Upload failed'
      setMessage(`❌ ${errorMsg}`)
      toast.error(`Upload failed: ${errorMsg}`)
    } finally {
      setUploading(false)
    }
  }

  const onSearch = async () => {
    if (!query.trim()) return
    
    setMessage('')
    setLoading(true)
    try {
      const rows = await kbSearch(query, 5)
      setResults(rows)
      toast.success(`Found ${rows.length} results`)
    } catch(err) {
      setMessage('Search failed')
      toast.error('Search failed')
    } finally {
      setLoading(false)
    }
  }

  const onRefresh = async () => {
    setMessage('')
    setRefreshing(true)
    try {
      await kbRefresh()
      setMessage('Embeddings refreshed')
      toast.success('Embeddings refreshed successfully!')
    } catch(err) {
      setMessage('Refresh failed')
      toast.error('Failed to refresh embeddings')
    } finally {
      setRefreshing(false)
    }
  }

  const loadAllData = async () => {
    setLoading(true)
    try {
      const data = await kbGetAll()
      setResults(data)
      setMessage(`Showing ${data.length} knowledge base entries`)
    } catch(err) {
      setMessage('Failed to load knowledge base data')
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const onDelete = async (index) => {
    if (!confirm('Are you sure you want to delete this entry?')) return
    
    setDeleting(index)
    try {
      await kbDeleteEntry(index)
      toast.success('Entry deleted successfully!')
      // Reload data after deletion
      loadAllData()
    } catch(err) {
      toast.error('Failed to delete entry')
    } finally {
      setDeleting(null)
    }
  }

  // Load all data on component mount
  useEffect(() => {
    loadAllData()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg mr-4">
                <Database className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Knowledge Base Management
                </h1>
                <p className="text-gray-600">
                  Upload, view, and manage your career intelligence knowledge base
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowSearch(!showSearch)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  showSearch 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {showSearch ? 'View All' : 'Search Mode'}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Upload & Refresh Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <FileText className="w-5 h-5 mr-2" />
            Manage Knowledge Base
          </h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Knowledge Base File
              </label>
              <div className="relative">
                <input
                  type="file"
                  accept=".xlsx,.xls"
                  onChange={onUpload}
                  disabled={uploading}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
                />
                {uploading && (
                  <div className="absolute right-2 top-2">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  </div>
                )}
              </div>
              
              {/* Show uploaded file info */}
              {uploadedFile && (
                <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                    <div className="text-sm">
                      <p className="font-medium text-green-800">{uploadedFile.name}</p>
                      <p className="text-green-600">
                        {(uploadedFile.size / 1024).toFixed(1)} KB • Uploaded {new Date(uploadedFile.uploadedAt).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex items-end">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onRefresh}
                disabled={refreshing}
                className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {refreshing ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 mr-2" />
                )}
                Refresh Embeddings
              </motion.button>
            </div>
          </div>
        </motion.div>

        {/* Search Section - Only show when in search mode */}
        {showSearch && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Brain className="w-5 h-5 mr-2" />
            Search Knowledge Base
          </h2>
          
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyPress={e => e.key === 'Enter' && onSearch()}
                placeholder="Search for job roles, skills, or career information..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onSearch}
              disabled={loading || !query.trim()}
              className="flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              ) : (
                <Search className="w-5 h-5 mr-2" />
              )}
              Search
            </motion.button>
          </div>
        </motion.div>
        )}

        {/* Status Message */}
        {message && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mb-6 p-4 rounded-xl flex items-center ${
              message.includes('failed') 
                ? 'bg-red-50 border border-red-200 text-red-700' 
                : 'bg-green-50 border border-green-200 text-green-700'
            }`}
          >
            {message.includes('failed') ? (
              <AlertCircle className="w-5 h-5 mr-3" />
            ) : (
              <CheckCircle className="w-5 h-5 mr-3" />
            )}
            {message}
          </motion.div>
        )}

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {showSearch ? `Search Results (${results.length})` : `Knowledge Base Entries (${results.length})`}
          </h2>
          
          {results.length === 0 ? (
            <div className="text-center py-8">
              <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">
                {showSearch 
                  ? "No results found. Try searching for job roles or skills." 
                  : "No knowledge base data found. Upload an Excel file to get started."
                }
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 mr-3">
                          {result.job_role || result['Job Role']}
                        </h3>
                        {(result.level || result['Level']) && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                            {result.level || result['Level']}
                          </span>
                        )}
                      </div>
                      
                      {(result.cluster || result['Cluster']) && (
                        <p className="text-sm text-gray-500 mb-1">
                          <span className="font-medium">Cluster:</span> {result.cluster || result['Cluster']} • {result.job_family || result['Job Family']}
                        </p>
                      )}
                      
                      {(result.qualifications || result['Qualifications / Degrees']) && (
                        <p className="text-sm text-gray-600 mb-2">
                          <span className="font-medium">Qualifications:</span> {result.qualifications || result['Qualifications / Degrees']}
                        </p>
                      )}
                      
                      <p className="text-gray-600 mb-2">
                        <span className="font-medium">Technical Skills:</span> {result.technical_skills || result['Technical Skills']}
                      </p>
                      
                      {(result.soft_skills || result['Soft Skills']) && (
                        <p className="text-gray-600 mb-2">
                          <span className="font-medium">Soft Skills:</span> {result.soft_skills || result['Soft Skills']}
                        </p>
                      )}
                      
                      {(result.domain_skills || result['Domain / Functional Skills']) && (
                        <p className="text-gray-600 mb-2">
                          <span className="font-medium">Domain Skills:</span> {result.domain_skills || result['Domain / Functional Skills']}
                        </p>
                      )}
                      
                      {(result.description || result['Job Description Summary']) && (
                        <p className="text-gray-700 mb-2 text-sm">
                          <span className="font-medium">Description:</span> {result.description || result['Job Description Summary']}
                        </p>
                      )}
                      
                      {(result.experience_range || result['Experience Range']) && (
                        <p className="text-sm text-gray-500 mb-1">
                          <span className="font-medium">Experience:</span> {result.experience_range || result['Experience Range']}
                        </p>
                      )}
                      
                      {(result.average_salary || result['Average Salary (India / Global)']) && (
                        <p className="text-sm text-green-600 mb-1">
                          <span className="font-medium">Salary:</span> {result.average_salary || result['Average Salary (India / Global)']}
                        </p>
                      )}
                      
                      {(result.sources || result['Primary Data Sources (with URLs)']) && (
                        <p className="text-sm text-blue-600">
                          <span className="font-medium">Sources:</span> 
                          <a href={(result.sources || result['Primary Data Sources (with URLs)']).split('|')[0].trim()} target="_blank" rel="noopener noreferrer" className="ml-1 hover:underline">
                            View Sources
                          </a>
                        </p>
                      )}
                    </div>
                    <div className="flex items-center ml-4 space-x-2">
                      {result.score && (
                        <div className="flex items-center">
                          <Star className="w-4 h-4 text-yellow-500 mr-1" />
                          <span className="text-sm font-medium text-gray-700">
                            {result.score.toFixed(2)}
                          </span>
                        </div>
                      )}
                      <button
                        onClick={() => onDelete(index)}
                        disabled={deleting === index}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                        title="Delete this entry"
                      >
                        {deleting === index ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <Trash2 className="w-4 h-4" />
                        )}
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
