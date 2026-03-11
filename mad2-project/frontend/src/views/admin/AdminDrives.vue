<script setup>
import { ref, onMounted } from 'vue'

const drives = ref([])

async function loadDrives(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/admin/drives',{
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()

    drives.value = data
}

async function updateStatus(id, action){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/admin/drive/${action}/${id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()

    alert(data.message)

    loadDrives()
}

onMounted(()=>{
    loadDrives()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">Placement Drives</h2>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.company }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.allowed_branch }}</td>
                    <td>{{ drive.min_cgpa }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>

                    <td>
                        <button class="btn btn-success btn-sm me-2" @click="updateStatus(drive.id,'approve')">
                            Approve
                        </button>

                        <button class="btn btn-danger btn-sm" @click="updateStatus(drive.id,'reject')">
                            Reject
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="mt-4">
            <router-link class="btn btn-secondary" to="/admin/dashboard">
                ← Back to Dashboard
            </router-link>
        </div>
    </div>
</template>