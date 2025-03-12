import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

import { fileURLToPath, URL } from 'node:url'
import path from 'node:path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, path.join(process.cwd(), '../'), '')
  const apiUrl = mode === 'production' ? '/api' : env.API_URL

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    define: { 'import.meta.env.API_URL': JSON.stringify(apiUrl) }
  }
})
