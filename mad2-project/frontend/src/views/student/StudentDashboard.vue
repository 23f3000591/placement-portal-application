<script setup>
import { ref, onMounted } from 'vue'

const name = ref('')
const branch = ref('')
const year = ref('')
const cgpa = ref('')
const applications = ref(0)
const selected = ref(0)

async function loadDashboard(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/student/dashboard', {
        headers:{
            'Authentication-Token': token
        }
    })

    if(!response.ok){
        alert("Failed to load dashboard")
        return
    }

    const data = await response.json()

    name.value = data.name
    branch.value = data.branch
    year.value = data.year
    cgpa.value = data.cgpa
    applications.value = data.applications
    selected.value = data.selected
}

onMounted(()=>{
    loadDashboard()
})
</script>


<template>
    <div class="container mt-5">
        <h2 class="mb-4">Student Dashboard</h2>
        <div class="row">
            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Name</h5>
                    <p>{{ name }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Branch</h5>
                    <p>{{ branch }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Year</h5>
                    <p>{{ year }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>CGPA</h5>
                    <p>{{ cgpa }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Total Applications</h5>
                    <p>{{ applications }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Selected</h5>
                    <p>{{ selected }}</p>
                </div>
            </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="mt-4">
            <router-link class="btn btn-primary me-3" to="/student/drives">
                View Placement Drives
            </router-link>

            <router-link class="btn btn-primary me-3" to="/student/applications">
                My Applications
            </router-link>

            <router-link class="btn btn-primary" to="/student/profile">
                Update Profile
            </router-link>
        </div>
    </div>
</template>