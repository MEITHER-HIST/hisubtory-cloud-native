import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

// https://vitejs.dev/config/
export default defineConfig({
  // 💡 엔트리 포인트 탐색 위치를 명시적으로 현재 디렉토리로 설정
  root: process.cwd(),
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'esnext',
    outDir: 'build',
    emptyOutDir: true,
    sourcemap: false,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/admin': { target: 'http://127.0.0.1:8000' },
      '/static': { target: 'http://127.0.0.1:8000' },
      '/media': { target: 'http://127.0.0.1:8000' },
    },
  },
});
