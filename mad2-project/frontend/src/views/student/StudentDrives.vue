<script setup>
import { ref, onMounted } from 'vue'

const drives = ref([])

async function loadDrives(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/student/drives',{
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

async function applyDrive(id){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/student/apply/${id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    alert(data.message)
}

onMounted(()=>{
    loadDrives()
})
</script>

<template>
    <div class="container mt-5">
    <h2 class="mb-4">Available Placement Drives</h2>
        <div class="row">
            <div class="col-md-4 mb-3" v-for="drive in drives" :key="drive.id">
                <div class="card p-3">
                    <h5>{{ drive.job_title }}</h5>
                    <p><strong>Company:</strong> {{ drive.company }}</p>
                    <p><strong>CGPA:</strong> {{ drive.min_cgpa }}</p>
                    <p><strong>Branch:</strong> {{ drive.branch }}</p>
                    <p><strong>Year:</strong> {{ drive.year }}</p>
                    <p><strong>Deadline:</strong> {{ drive.deadline }}</p>
                    <button
                        v-if="!drive.applied"
                        class="btn btn-primary w-100"
                        @click="applyDrive(drive.id)"
                    >
                    Apply
                    </button>

                    <button
                        v-else
                        class="btn btn-success w-100"
                        disabled
                    >
                    Applied
                    </button>
                </div>
            </div>
        </div>
        <div class="mt-4">
            <router-link class="btn btn-secondary" to="/student/dashboard">
                ← Back to Dashboard
            </router-link>
        </div>
    </div>
</template>