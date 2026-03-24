import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

// https://vitejs.dev/config/
export default defineConfig({
  // 💡 리소스 경로를 상대 경로로 설정하여 MIME 타입 에러 방지
  base: './',
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    // 💡 Vite 기본값인 dist 폴더를 사용하여 호환성 극대화
    outDir: 'dist',
    emptyOutDir: true,
    assetsDir: 'assets',
  }
});
