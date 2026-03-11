<script setup>
import { ref, onMounted } from 'vue'

const applications = ref([])

async function loadApplications(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/student/applications',{
        headers:{
            'Authentication-Token': token
        }
    })

    if(!response.ok){
        alert("Failed to load applications")
        return
    }

    const data = await response.json()

    applications.value = data
}

onMounted(()=>{
    loadApplications()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">My Applications</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Status</th>
                    <th>Date</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="app in applications" :key="app.application_id">
                    <td>{{ app.company }}</td>
                    <td>{{ app.job_title }}</td>
                    <td>{{ app.status }}</td>
                    <td>{{ app.applied_on }}</td>
                </tr>
            </tbody>
        </table>

        <div class="mt-4">
            <router-link class="btn btn-secondary" to="/student/dashboard">
                ← Back to Dashboard
            </router-link>
        </div>
    </div>
</template>