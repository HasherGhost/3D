import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // During dev, forward API calls to the FastAPI server on port 8000
  server: {
    proxy: {
      '/predict': 'http://localhost:8000',
      '/health':  'http://localhost:8000',
      '/samples': 'http://localhost:8000',
    },
  },
  // Build output goes into the backend's static folder so FastAPI can serve it
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
  },
})
