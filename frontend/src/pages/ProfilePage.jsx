import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'react-toastify'
import { getMe, createMe, updateMe } from '../services/studentService'
import {
  User,
  GraduationCap,
  Code,
  Heart,
  FileText,
  Save,
  AlertCircle,
  CheckCircle,
  Calendar,
  DollarSign,
  Loader,
  Mail,
  Phone,
  Target,
  BookOpen,
  Award,
  Linkedin,
  Github
} from 'lucide-react'

export default function ProfilePage() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [form, setForm] = useState({
    // Basic fields (existing)
    education_level: '',
    skills: '',
    interests: '',
    bio: '',
    experience_years: '',
    target_salary: '',
    // Enhanced profile fields (new)
    name: '',
    contact_email: '',
    contact_phone: '',
    career_direction: '',
    language_fluency: {},
    medium_of_instruction_10: '',
    medium_of_instruction_12: '',
    gpa_percentile: '',
    linkedin_url: '',
    github_url: ''
  })

  useEffect(() => {
    let mounted = true
    getMe().then(data => {
      if (!mounted) return
      setProfile(data)
      setForm({
        // Basic fields
        education_level: data.education_level || '',
        skills: data.skills || '',
        interests: data.interests || '',
        bio: data.bio || '',
        experience_years: data.experience_years !== null && data.experience_years !== undefined ? data.experience_years : '',
        target_salary: data.target_salary !== null && data.target_salary !== undefined ? data.target_salary : '',
        // Enhanced fields
        name: data.name || '',
        contact_email: data.contact_email || '',
        contact_phone: data.contact_phone || '',
        career_direction: data.career_direction || '',
        language_fluency: data.language_fluency || {},
        medium_of_instruction_10: data.medium_of_instruction_10 || '',
        medium_of_instruction_12: data.medium_of_instruction_12 || '',
        gpa_percentile: data.gpa_percentile !== null && data.gpa_percentile !== undefined ? data.gpa_percentile : '',
        linkedin_url: data.linkedin_url || '',
        github_url: data.github_url || ''
      })
    }).catch(err => {
      console.error('Failed to load profile:', err)
      setProfile(null)
    }).finally(() => setLoading(false))
    return () => { mounted = false }
  }, [])

  const onChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSaving(true)
    setSuccess(false)

    try {
      // Validate required fields
      if (!form.education_level) {
        throw new Error('Please select your education level')
      }
      if (!form.skills || form.skills.length < 10) {
        throw new Error('Please enter at least 10 characters of skills')
      }
      if (form.experience_years === '' || form.experience_years === null) {
        throw new Error('Please enter your years of experience')
      }

      const save = profile ? updateMe : createMe
      const data = await save(form)
      setProfile(data)
      setSuccess(true)
      toast.success('Profile saved successfully!')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to save profile. Please try again.'
      setError(errorMsg)
      toast.error(errorMsg)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading your profile...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Profile</h1>
            <p className="text-gray-600">
              {profile ? 'Update your information to get better AI recommendations' : 'Create your profile to start your career journey'}
            </p>
          </div>

          {/* Success Message */}
          {success && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center"
            >
              <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
              <p className="text-green-700">Profile updated successfully!</p>
            </motion.div>
          )}

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

          {/* Profile Form */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center">
                <User className="w-6 h-6 text-blue-600 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Personal Information</h2>
              </div>
            </div>

            <form onSubmit={onSubmit} className="p-6 space-y-6">
              {/* Education Level */}
              <div>
                <label htmlFor="education_level" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <GraduationCap className="w-4 h-4 mr-2" />
                  Education Level & Degree
                </label>
                <select
                  id="education_level"
                  name="education_level"
                  value={form.education_level}
                  onChange={onChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                >
                  <option value="">Select your education level</option>
                  <optgroup label="High School">
                    <option value="High School">High School Diploma</option>
                    <option value="Secondary">Secondary Education</option>
                  </optgroup>
                  <optgroup label="Diploma & Associate">
                    <option value="Diploma">Diploma</option>
                    <option value="Associate">Associate Degree</option>
                  </optgroup>
                  <optgroup label="Bachelor's Degree">
                    <option value="Bachelor">Bachelor of Science (B.Sc)</option>
                    <option value="BA">Bachelor of Arts (B.A)</option>
                    <option value="BTech">Bachelor of Technology (B.Tech)</option>
                    <option value="BE">Bachelor of Engineering (B.E)</option>
                    <option value="BCA">Bachelor of Computer Applications (BCA)</option>
                    <option value="BCS">Bachelor of Computer Science (BCS)</option>
                    <option value="BBA">Bachelor of Business Administration (BBA)</option>
                    <option value="BCom">Bachelor of Commerce (B.Com)</option>
                    <option value="BDS">Bachelor of Dental Surgery (BDS)</option>
                    <option value="MBBS">Bachelor of Medicine (MBBS)</option>
                  </optgroup>
                  <optgroup label="Master's Degree">
                    <option value="Master">Master of Science (M.Sc)</option>
                    <option value="MA">Master of Arts (M.A)</option>
                    <option value="MBA">Master of Business Administration (MBA)</option>
                    <option value="MTech">Master of Technology (M.Tech)</option>
                    <option value="ME">Master of Engineering (M.E)</option>
                    <option value="MCA">Master of Computer Applications (MCA)</option>
                    <option value="MCom">Master of Commerce (M.Com)</option>
                  </optgroup>
                  <optgroup label="Doctorate">
                    <option value="PhD">Doctor of Philosophy (PhD)</option>
                    <option value="MD">Doctor of Medicine (MD)</option>
                    <option value="Doctorate">Doctorate Degree</option>
                  </optgroup>
                  <optgroup label="Certifications">
                    <option value="Certificate">Professional Certificate</option>
                    <option value="Other">Other</option>
                  </optgroup>
                </select>
                <p className="mt-1 text-sm text-gray-500">Select your highest education qualification</p>
              </div>

              {/* Experience Years */}
              <div>
                <label htmlFor="experience_years" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="w-4 h-4 mr-2" />
                  Years of Experience
                </label>
                <input
                  id="experience_years"
                  name="experience_years"
                  type="number"
                  min="0"
                  max="50"
                  step="0.5"
                  value={form.experience_years}
                  onChange={onChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  placeholder="e.g., 2, 2.5, 3"
                  required
                />
                <p className="mt-1 text-sm text-gray-500">Enter your total years of professional experience (0-50)</p>
              </div>

              {/* Target Salary */}
              <div>
                <label htmlFor="target_salary" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <DollarSign className="w-4 h-4 mr-2" />
                  Target Salary (LPA)
                </label>
                <input
                  id="target_salary"
                  name="target_salary"
                  type="number"
                  min="0"
                  step="0.5"
                  value={form.target_salary}
                  onChange={onChange}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  placeholder="e.g., 8, 10, 12.5"
                />
                <p className="mt-1 text-sm text-gray-500">Enter your expected salary in Lakhs Per Annum (LPA)</p>
              </div>

              {/* Skills */}
              <div>
                <label htmlFor="skills" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <Code className="w-4 h-4 mr-2" />
                  Skills (Required)
                </label>
                <textarea
                  id="skills"
                  name="skills"
                  value={form.skills}
                  onChange={onChange}
                  rows={3}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  placeholder="List your technical and soft skills (e.g., Python, React, Communication, Leadership)"
                  required
                  minLength="10"
                />
                <p className="mt-1 text-sm text-gray-500">
                  {form.skills.length < 10 ? `${10 - form.skills.length} more characters needed` : '✓ Good'}
                  {' • '}Separate skills with commas for better AI analysis
                </p>
              </div>

              {/* Interests */}
              <div>
                <label htmlFor="interests" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <Heart className="w-4 h-4 mr-2" />
                  Career Interests
                </label>
                <textarea
                  id="interests"
                  name="interests"
                  value={form.interests}
                  onChange={onChange}
                  rows={3}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  placeholder="Describe your career interests and goals (e.g., AI, Web Development, Data Science, Product Management)"
                />
                <p className="mt-1 text-sm text-gray-500">
                  {form.interests.length > 0 ? `${form.interests.length} characters` : 'Optional'}
                  {' • '}Help AI understand your career aspirations
                </p>
              </div>

              {/* Bio */}
              <div>
                <label htmlFor="bio" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <FileText className="w-4 h-4 mr-2" />
                  Professional Bio
                </label>
                <textarea
                  id="bio"
                  name="bio"
                  value={form.bio}
                  onChange={onChange}
                  rows={4}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  placeholder="Write a brief professional summary about yourself, your background, and career objectives"
                />
                <p className="mt-1 text-sm text-gray-500">
                  {form.bio.length > 0 ? `${form.bio.length} characters` : 'Optional'}
                  {' • '}Mention projects, achievements, and career goals for better AI analysis
                </p>
              </div>

              {/* NEW SECTION: Personal Information */}
              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h3>

                {/* Name */}
                <div className="mb-4">
                  <label htmlFor="name" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <User className="w-4 h-4 mr-2" />
                    Full Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={form.name}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="Enter your full name"
                  />
                  <p className="mt-1 text-sm text-gray-500">Your name as it appears on official documents</p>
                </div>

                {/* Contact Email */}
                <div className="mb-4">
                  <label htmlFor="contact_email" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Mail className="w-4 h-4 mr-2" />
                    Contact Email
                  </label>
                  <input
                    id="contact_email"
                    name="contact_email"
                    type="email"
                    value={form.contact_email}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="your.email@example.com"
                  />
                  <p className="mt-1 text-sm text-gray-500">Email for career-related communications</p>
                </div>

                {/* Contact Phone */}
                <div className="mb-4">
                  <label htmlFor="contact_phone" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Phone className="w-4 h-4 mr-2" />
                    Contact Phone
                  </label>
                  <input
                    id="contact_phone"
                    name="contact_phone"
                    type="tel"
                    value={form.contact_phone}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="+91 XXXXXXXXXX"
                  />
                  <p className="mt-1 text-sm text-gray-500">Phone number for recruiters to reach you</p>
                </div>
              </div>

              {/* NEW SECTION: Career Direction */}
              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Career Direction</h3>

                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-3">
                    <Target className="w-4 h-4 mr-2" />
                    What's your career path preference?
                  </label>
                  <div className="space-y-3">
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="career_direction"
                        value="job"
                        checked={form.career_direction === 'job'}
                        onChange={onChange}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-900">Job / Employment</span>
                    </label>

                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="career_direction"
                        value="higher_studies_india"
                        checked={form.career_direction === 'higher_studies_india'}
                        onChange={onChange}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-900">Higher Studies (India)</span>
                    </label>

                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="career_direction"
                        value="higher_studies_abroad"
                        checked={form.career_direction === 'higher_studies_abroad'}
                        onChange={onChange}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-900">Higher Studies (Abroad)</span>
                    </label>

                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="career_direction"
                        value="entrepreneurship"
                        checked={form.career_direction === 'entrepreneurship'}
                        onChange={onChange}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-900">Entrepreneurship / Startup</span>
                    </label>

                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="career_direction"
                        value="not_sure"
                        checked={form.career_direction === 'not_sure'}
                        onChange={onChange}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-900">Not Sure Yet</span>
                    </label>
                  </div>
                  <p className="mt-2 text-sm text-gray-500">💡 This helps us provide personalized career pathways</p>
                </div>
              </div>

              {/* NEW SECTION: Languages & Education Background */}
              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Languages & Education Background</h3>

                {/* Medium of Instruction - 10th */}
                <div className="mb-4">
                  <label htmlFor="medium_of_instruction_10" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <BookOpen className="w-4 h-4 mr-2" />
                    Medium of Instruction (10th Grade)
                  </label>
                  <select
                    id="medium_of_instruction_10"
                    name="medium_of_instruction_10"
                    value={form.medium_of_instruction_10}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  >
                    <option value="">Select medium</option>
                    <option value="English">English</option>
                    <option value="Hindi">Hindi</option>
                    <option value="Regional Language">Regional Language</option>
                    <option value="Other">Other</option>
                  </select>
                  <p className="mt-1 text-sm text-gray-500">Language of instruction in 10th standard</p>
                </div>

                {/* Medium of Instruction - 12th */}
                <div className="mb-4">
                  <label htmlFor="medium_of_instruction_12" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <BookOpen className="w-4 h-4 mr-2" />
                    Medium of Instruction (12th Grade)
                  </label>
                  <select
                    id="medium_of_instruction_12"
                    name="medium_of_instruction_12"
                    value={form.medium_of_instruction_12}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  >
                    <option value="">Select medium</option>
                    <option value="English">English</option>
                    <option value="Hindi">Hindi</option>
                    <option value="Regional Language">Regional Language</option>
                    <option value="Other">Other</option>
                  </select>
                  <p className="mt-1 text-sm text-gray-500">Language of instruction in 12th standard</p>
                </div>
              </div>

              {/* NEW SECTION: Academic Performance */}
              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Academic Performance (Optional)</h3>

                <div>
                  <label htmlFor="gpa_percentile" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Award className="w-4 h-4 mr-2" />
                    GPA / Percentile
                  </label>
                  <input
                    id="gpa_percentile"
                    name="gpa_percentile"
                    type="number"
                    min="0"
                    max="100"
                    step="0.01"
                    value={form.gpa_percentile}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="e.g., 85.5, 8.5 (CGPA), 90 (Percentage)"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    📊 Optional - Enter your CGPA, GPA, or percentage. This won't affect your career score negatively.
                  </p>
                </div>
              </div>

              {/* NEW SECTION: Portfolio Links */}
              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Portfolio & Professional Links</h3>

                {/* LinkedIn URL */}
                <div className="mb-4">
                  <label htmlFor="linkedin_url" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Linkedin className="w-4 h-4 mr-2" />
                    LinkedIn Profile
                  </label>
                  <input
                    id="linkedin_url"
                    name="linkedin_url"
                    type="url"
                    value={form.linkedin_url}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="https://linkedin.com/in/yourprofile"
                  />
                  <p className="mt-1 text-sm text-gray-500">💼 Add your LinkedIn profile to import professional experience</p>
                </div>

                {/* GitHub URL */}
                <div className="mb-4">
                  <label htmlFor="github_url" className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Github className="w-4 h-4 mr-2" />
                    GitHub Profile
                  </label>
                  <input
                    id="github_url"
                    name="github_url"
                    type="url"
                    value={form.github_url}
                    onChange={onChange}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                    placeholder="https://github.com/yourusername"
                  />
                  <p className="mt-1 text-sm text-gray-500">💻 Add your GitHub to showcase your coding projects and contributions</p>
                </div>
              </div>

              {/* Submit Button */}
              <div className="pt-6 border-t border-gray-200">
                <button
                  type="submit"
                  disabled={saving}
                  className="w-full sm:w-auto flex items-center justify-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {saving ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin mr-2" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5 mr-2" />
                      {profile ? 'Update Profile' : 'Create Profile'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Profile Completion Tips */}
          <div className="mt-8 bg-blue-50 rounded-xl p-6 border border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-4">💡 Profile Tips</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-800">
              <div>
                <strong>Be Specific:</strong> Detailed skills and interests help AI provide better recommendations
              </div>
              <div>
                <strong>Stay Updated:</strong> Regular profile updates improve recommendation accuracy
              </div>
              <div>
                <strong>Include Goals:</strong> Mention your career aspirations in interests and bio
              </div>
              <div>
                <strong>Quantify Experience:</strong> Include years of experience for better role matching
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
