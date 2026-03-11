<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth_store = useAuthStore()

function logout(){
    auth_store.logout()
    router.push('/')
}
</script>

<template>
    <nav class="navbar navbar-light bg-light px-4 shadow-sm">
        <router-link to="/" class="navbar-brand fw-bold text-decoration-none text-dark">
            Placement Portal
        </router-link>

        <button class="btn btn-outline-danger" @click="logout">
            Logout
        </button>
    </nav>
</template>