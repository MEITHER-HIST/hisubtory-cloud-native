import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// 💡 ESM 환경에서 __dirname을 대체하는 표준 방법
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  root: process.cwd(),
  plugins: [react()],
  resolve: {
    alias: {
      // 💡 경로 별칭을 안전하게 설정
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'esnext',
    outDir: 'build',
    emptyOutDir: true,
    sourcemap: false,
    // 💡 빌드 실패 시 상세 로그를 위한 설정
    minify: 'esbuild',
    reportCompressedSize: false,
  },
});
