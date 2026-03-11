<script setup>
import { ref } from 'vue'

const github = ref('')
const linkedin = ref('')
const contact = ref('')
const cgpa = ref('')

async function updateProfile(){

    const token = localStorage.getItem('token')

    const data = {
        github: github.value,
        linkedin: linkedin.value,
        contact: contact.value,
        cgpa: cgpa.value
    }

    const response = await fetch('http://127.0.0.1:5000/student/profile',{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
            'Authentication-Token': token
        },
        body: JSON.stringify(data)
    })

    const res = await response.json()

    alert(res.message)
}
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">Update Profile</h2>

        <form @submit.prevent="updateProfile">
            <div class="mb-3">
                <label class="form-label">GitHub</label>
                <input type="text" class="form-control" v-model="github">
            </div>

            <div class="mb-3">
                <label class="form-label">LinkedIn</label>
                <input type="text" class="form-control" v-model="linkedin">
            </div>

            <div class="mb-3">
                <label class="form-label">Contact</label>
                <input type="text" class="form-control" v-model="contact">
            </div>

            <div class="mb-3">
                <label class="form-label">CGPA</label>
                <input type="number" step="0.01" class="form-control" v-model="cgpa">
            </div>

            <button class="btn btn-primary">
                Update
            </button>
        </form>
        <div class="mt-4">
            <router-link class="btn btn-secondary" to="/student/dashboard">
                ← Back to Dashboard
            </router-link>
        </div>
    </div>
</template>