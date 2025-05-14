// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'

import { BootstrapVueNext } from 'bootstrap-vue-next'

// Import Bootstrap and BootstrapVueNext CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

// Create the Vue app
const app = createApp(App)

// Use BootstrapVueNext and IconsPlugin
app.use(BootstrapVueNext)


// Use router
app.use(router)

// Mount the app
app.mount('#app')
