// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    // Removed rewrite rules - now using API routes for proxying to backend
    // This provides better error handling and debugging capabilities
  }
  
  module.exports = nextConfig