/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 💡 현재 App.tsx 등에서 사용하는 스타일링 호환을 위해 설정
    },
  },
  plugins: [],
}
