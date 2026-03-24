import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // 💡 경로 별칭을 표준적인 방식으로 설정
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'build',
    emptyOutDir: true,
  }
});
