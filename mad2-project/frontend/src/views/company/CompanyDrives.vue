<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const drives = ref([])

async function loadDrives(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/company/drives',{
        headers:{
            'Authentication-Token': token
        }
    })

    if(!response.ok){
        alert("Failed to load drives")
        return
    }

    const data = await response.json()

    drives.value = data
}

function viewApplicants(id){
    router.push(`/company/applicants?drive_id=${id}`)
}

onMounted(()=>{
    loadDrives()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">My Placement Drives</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>CGPA</th>
                    <th>Branch</th>
                    <th>Year</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Applicants</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.min_cgpa }}</td>
                    <td>{{ drive.branch }}</td>
                    <td>{{ drive.year }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>

                    <td>
                        <button class="btn btn-info btn-sm" @click="viewApplicants(drive.id)">
                            View Applicants
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div class="mt-3">

            <router-link class="btn btn-secondary me-2" to="/company/dashboard">
                ← Back to Dashboard
            </router-link>

            <router-link class="btn btn-primary" to="/company/create-drive">
                Create New Drive
            </router-link>

        </div>
    </div>
</template>