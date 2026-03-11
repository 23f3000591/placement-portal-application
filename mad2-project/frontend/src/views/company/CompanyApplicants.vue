<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const drive_id = ref(route.query.drive_id)
const applications = ref([])

async function loadApplicants(){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/company/applications/${drive_id.value}`,{
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()

    applications.value = data
}

async function updateStatus(id, action){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/company/${action}/${id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()

    alert(data.message)

    loadApplicants()
}

onMounted(()=>{
    loadApplicants()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">Applicants</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>

                <tr v-if="applications.length === 0">
                    <td colspan="5" class="text-center text-muted">
                        No applicants yet for this drive
                    </td>
                </tr>

                <tr v-for="app in applications" :key="app.application_id">
                    <td>{{ app.student_name }}</td>
                    <td>{{ app.branch }}</td>
                    <td>{{ app.cgpa }}</td>
                    <td>{{ app.status }}</td>

                    <td>
                        <button class="btn btn-warning btn-sm me-1" @click="updateStatus(app.application_id,'shortlist')">
                            Shortlist
                        </button>

                        <button class="btn btn-success btn-sm me-1" @click="updateStatus(app.application_id,'select')">
                            Select
                        </button>

                        <button class="btn btn-danger btn-sm" @click="updateStatus(app.application_id,'reject')">
                            Reject
                        </button>
                    </td>
                </tr>

            </tbody>
        </table>
        
        <div class="mt-3">

            <router-link class="btn btn-secondary me-2" to="/company/drives">
                ← Back to Drives
            </router-link>

            <router-link class="btn btn-primary" to="/company/dashboard">
                Go to Dashboard
            </router-link>

        </div>

    </div>
</template>