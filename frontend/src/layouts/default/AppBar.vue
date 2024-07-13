<template>
  <v-app-bar flat :color="theme.global.current.value.colors.primary">
    <v-app-bar-title>
      <v-icon icon="mdi-chart-line" class="mr-2" />
      Financial Tracker
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn icon @click="toggleTheme">
      <v-icon>{{ theme.global.name.value === 'light' ? 'mdi-weather-night' : 'mdi-weather-sunny' }}</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}
</script>
