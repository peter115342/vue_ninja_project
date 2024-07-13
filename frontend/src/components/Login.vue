<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card :color="theme.global.current.value.colors.background" class="elevation-12">
          <v-toolbar :color="theme.global.current.value.colors.primary" dark flat>
            <v-toolbar-title>{{ isRegistering ? 'Register' : 'Login' }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="username"
                :color="theme.global.current.value.colors.primary"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                :color="theme.global.current.value.colors.primary"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
              <v-text-field
                v-if="isRegistering"
                v-model="confirmPassword"
                :color="theme.global.current.value.colors.primary"
                label="Confirm Password"
                name="confirmPassword"
                prepend-icon="mdi-lock-check"
                type="password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              :color="theme.global.current.value.colors.primary"
              @click="handleSubmit"
            >
              {{ isRegistering ? 'Register' : 'Login' }}
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-btn
              :color="theme.global.current.value.colors.secondary"
              text
              @click="isRegistering = !isRegistering"
            >
              {{ isRegistering ? 'Back to Login' : 'Register' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar" :color="snackbarColor">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useTheme } from 'vuetify'
import axios from 'axios'

const theme = useTheme()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const isRegistering = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('')

const handleSubmit = async () => {
  if (isRegistering.value) {
    if (password.value !== confirmPassword.value) {
      showSnackbar('Passwords do not match', 'error')
      return
    }

    try {
      const response = await axios.post('http://localhost:8000/api/register', {
        username: username.value,
        password: password.value,
        confirm_password: confirmPassword.value
      })
      showSnackbar(response.data.message, 'success')
      isRegistering.value = false
    } catch (error) {
      showSnackbar(error.response?.data?.detail || 'An error occurred', 'error')
    }
  } else {
    // Handle login logic here
    console.log('Login clicked')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}
</script>
