import React, { useEffect, useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { listDocuments, uploadDocument, ocrDocument } from '../services/documentService'
import api from '../services/api'
import { toast } from 'react-toastify'
import {
  Upload,
  FileText,
  Eye,
  Loader,
  AlertCircle,
  CheckCircle,
  Sparkles,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Building,
  Tag,
  Edit2
} from 'lucide-react'

export default function DocumentsPage() {
  const [docs, setDocs] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [processingIds, setProcessingIds] = useState(new Set())

  const load = async () => {
    setLoading(true)
    try {
      const data = await listDocuments()
      setDocs(data)
      setError('')
    } catch (e) {
      setError('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const onFileUpload = async (e) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    setUploading(true)
    setError('')

    try {
      for (const file of files) {
        await uploadDocument(file)
      }
      await load()
      toast.success(`${files.length} file(s) uploaded successfully`)
    } catch (e) {
      setError('Upload failed')
      toast.error('Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const onOcr = async (id) => {
    setProcessingIds(prev => new Set(prev).add(id))
    setError('')

    try {
      await ocrDocument(id)
      await load()
      toast.success('OCR completed successfully')
    } catch (e) {
      setError('OCR processing failed')
      toast.error('OCR failed')
    } finally {
      setProcessingIds(prev => {
        const newSet = new Set(prev)
        newSet.delete(id)
        return newSet
      })
    }
  }

  const onExtractSkills = async () => {
    if (docs.length === 0) {
      toast.warning('No documents available for skill extraction')
      return
    }

    try {
      const ids = docs.map(d => d.id)
      const res = await api.post('/documents/extract-skills', { document_ids: ids })
      toast.success(`Extracted skills: ${res.data.skills.join(', ')}`)
    } catch (e) {
      setError('Skill extraction failed')
      toast.error('Skill extraction failed')
    }
  }

  const getFileIcon = (mimeType) => {
    return FileText // Simplified to avoid icon import issues
  }

  const formatConfidence = (confidence) => {
    if (typeof confidence !== 'number') return '—'
    const percent = Math.round(confidence * 100)
    return `${percent}%`
  }

  const getConfidenceColor = (confidence) => {
    if (typeof confidence !== 'number') return 'text-gray-500'
    const percent = confidence * 100
    if (percent >= 80) return 'text-green-600'
    if (percent >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getVerificationBadge = (status) => {
    const badges = {
      verified: { icon: ShieldCheck, color: 'bg-green-100 text-green-700', label: 'Verified' },
      low_trust: { icon: ShieldAlert, color: 'bg-yellow-100 text-yellow-700', label: 'Low Trust' },
      needs_action: { icon: Shield, color: 'bg-red-100 text-red-700', label: 'Needs Action' },
      pending: { icon: Shield, color: 'bg-gray-100 text-gray-700', label: 'Pending' }
    }
    return badges[status] || badges.pending
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Document Management</h1>
            <p className="text-gray-600">
              Upload your certificates, resumes, and other documents for AI-powered analysis
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center"
            >
              <AlertCircle className="w-5 h-5 text-red-500 mr-3" />
              <p className="text-red-700">{error}</p>
            </motion.div>
          )}

          {/* Upload Section */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 mb-8">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Upload className="w-6 h-6 text-blue-600 mr-3" />
                  <h2 className="text-xl font-semibold text-gray-900">Upload Documents</h2>
                </div>
                {docs.length > 0 && (
                  <button
                    onClick={onExtractSkills}
                    className="flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-blue-700 transition-colors"
                  >
                    <Sparkles className="w-4 h-4 mr-2" />
                    Extract Skills
                  </button>
                )}
              </div>
            </div>

            <div className="p-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                {uploading ? (
                  <div className="flex flex-col items-center">
                    <Loader className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                    <p className="text-lg font-medium text-gray-900">Uploading...</p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <Upload className="w-12 h-12 text-gray-400 mb-4" />
                    <p className="text-lg font-medium text-gray-900 mb-2">Upload Documents</p>
                    <p className="text-gray-500 mb-4">Select files to upload</p>
                    <input
                      type="file"
                      multiple
                      accept=".pdf,.png,.jpg,.jpeg,.gif,.bmp,.tiff"
                      onChange={onFileUpload}
                      className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                    <p className="text-sm text-gray-400 mt-2">
                      Supports PDF, PNG, JPG, JPEG, GIF, BMP, TIFF
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Documents List */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center">
                <FileText className="w-6 h-6 text-blue-600 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Your Documents</h2>
                <span className="ml-3 px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
                  {docs.length}
                </span>
              </div>
            </div>

            <div className="p-6">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader className="w-8 h-8 text-blue-600 animate-spin mr-3" />
                  <p className="text-gray-600">Loading documents...</p>
                </div>
              ) : docs.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-lg text-gray-500 mb-2">No documents uploaded yet</p>
                  <p className="text-gray-400">Upload your first document to get started</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Document</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Provider</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Verification</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Skills</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {docs.map((doc, index) => {
                        const FileIcon = getFileIcon(doc.mime_type)
                        const isProcessing = processingIds.has(doc.id)

                        return (
                          <motion.tr
                            key={doc.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.1 }}
                            className="border-b border-gray-100 hover:bg-gray-50"
                          >
                            <td className="py-4 px-4">
                              <div className="flex items-center">
                                <FileIcon className="w-5 h-5 text-gray-500 mr-3" />
                                <div>
                                  <p className="font-medium text-gray-900">{doc.filename}</p>
                                  {doc.ocr_text && (
                                    <p className="text-sm text-gray-500 truncate max-w-xs">
                                      {doc.ocr_text.slice(0, 60)}...
                                    </p>
                                  )}
                                </div>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              {doc.provider ? (
                                <div className="flex items-center">
                                  <Building className="w-4 h-4 text-blue-600 mr-2" />
                                  <span className="text-sm font-medium text-gray-900">{doc.provider}</span>
                                </div>
                              ) : (
                                <span className="text-sm text-gray-400">Not detected</span>
                              )}
                            </td>
                            <td className="py-4 px-4">
                              {(() => {
                                const badge = getVerificationBadge(doc.verification_status)
                                const Icon = badge.icon
                                return (
                                  <div className="flex items-center">
                                    <span className={`flex items-center px-2 py-1 rounded-full text-xs font-semibold ${badge.color}`}>
                                      <Icon className="w-3 h-3 mr-1" />
                                      {badge.label}
                                    </span>
                                  </div>
                                )
                              })()}
                            </td>
                            <td className="py-4 px-4">
                              {doc.extracted_skills && doc.extracted_skills.length > 0 ? (
                                <div className="flex flex-wrap gap-1">
                                  {doc.extracted_skills.slice(0, 3).map((skill, idx) => (
                                    <span key={idx} className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
                                      {skill}
                                    </span>
                                  ))}
                                  {doc.extracted_skills.length > 3 && (
                                    <span className="text-xs text-gray-500">+{doc.extracted_skills.length - 3}</span>
                                  )}
                                </div>
                              ) : (
                                <span className="text-sm text-gray-400">None</span>
                              )}
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center space-x-2">
                                <button
                                  onClick={() => onOcr(doc.id)}
                                  disabled={isProcessing}
                                  className="flex items-center px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                  {isProcessing ? (
                                    <Loader className="w-4 h-4 animate-spin" />
                                  ) : (
                                    <Eye className="w-4 h-4" />
                                  )}
                                  <span className="ml-1">
                                    {isProcessing ? 'Processing...' : 'Run OCR'}
                                  </span>
                                </button>
                              </div>
                            </td>
                          </motion.tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* Tips Section */}
          <div className="mt-8 bg-blue-50 rounded-xl p-6 border border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-4">💡 Document Tips</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-800">
              <div>
                <strong>Best Quality:</strong> Upload clear, high-resolution images or PDFs for better OCR results
              </div>
              <div>
                <strong>Supported Formats:</strong> PDF files and common image formats work best
              </div>
              <div>
                <strong>File Size:</strong> Keep files under 20MB for optimal processing speed
              </div>
              <div>
                <strong>Multiple Files:</strong> You can drag and drop multiple files at once
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
