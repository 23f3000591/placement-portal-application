<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import PublicNavbar from './components/PublicNavbar.vue'
import PrivateNavbar from './components/PrivateNavbar.vue'

const route = useRoute()
const publicRoutes = ['/', '/login', '/student/register', '/company/register']

const isPublicRoute = computed(() => {
    return publicRoutes.includes(route.path)
})
</script>

<template>
    <PublicNavbar v-if="isPublicRoute" />
    <PrivateNavbar v-else/>

    <router-view />
</template>