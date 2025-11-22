import React from 'react'
import { Brain, Heart } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold">Career Intelligence</h3>
                <p className="text-gray-400 text-sm">AI-Powered Career Guidance</p>
              </div>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              Empowering students with AI-driven career insights, personalized recommendations, 
              and comprehensive analysis to build successful professional futures.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/dashboard" className="hover:text-white transition-colors">Dashboard</a></li>
              <li><a href="/profile" className="hover:text-white transition-colors">Profile</a></li>
              <li><a href="/career-analysis" className="hover:text-white transition-colors">Career Analysis</a></li>
              <li><a href="/reports" className="hover:text-white transition-colors">Reports</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/knowledge-base" className="hover:text-white transition-colors">Knowledge Base</a></li>
              <li><a href="/documents" className="hover:text-white transition-colors">Documents</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Career Intelligence System. All rights reserved.
          </p>
          <div className="flex items-center space-x-1 text-gray-400 text-sm mt-4 md:mt-0">
            <span>Made with</span>
            <Heart className="w-4 h-4 text-red-500" />
            <span>for students worldwide</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

