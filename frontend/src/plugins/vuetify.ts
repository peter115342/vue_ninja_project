/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1976D2',   // Blue for primary actions
          secondary: '#4CAF50', // Green for positive financial indicators
          accent: '#FF5722',    // Orange for attention-grabbing elements
          error: '#FF5252',     // Red for errors or negative balances
          info: '#2196F3',      // Light blue for informational elements
          success: '#4CAF50',   // Green for successful actions
          warning: '#FFC107',   // Amber for warnings
          background: '#F5F5F5' // Light grey background
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#2196F3',   // Lighter blue for primary actions
          secondary: '#66BB6A', // Softer green for positive financial indicators
          accent: '#FF7043',    // Softer orange for attention-grabbing elements
          error: '#FF5252',     // Red for errors or negative balances
          info: '#64B5F6',      // Lighter blue for informational elements
          success: '#66BB6A',   // Softer green for successful actions
          warning: '#FFD54F',   // Softer amber for warnings
          background: '#121212' // Dark background
        }
      }
    }
  }
})
