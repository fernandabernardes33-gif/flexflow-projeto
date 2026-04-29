export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
      borderRadius: {
        DEFAULT: '10px',
      },
      colors: {
        primary:         '#2563eb',
        'primary-dark':  '#1d4ed8',
        'primary-light': '#dbeafe',
        success:         '#059669',
        'success-light': '#d1fae5',
        danger:          '#dc2626',
        'danger-light':  '#fee2e2',
        warning:         '#ea580c',
        'warning-light': '#ffedd5',
        slate: {
          50:  '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          400: '#94a3b8',
          600: '#64748b',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
    },
  },
  plugins: [],
}
