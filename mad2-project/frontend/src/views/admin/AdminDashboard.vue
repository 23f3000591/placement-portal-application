<script setup>
import { ref, onMounted } from 'vue'

const students = ref(0)
const companies = ref(0)
const drives = ref(0)
const applications = ref(0)

async function loadDashboard(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/admin/dashboard',{
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()

    students.value = data.students
    companies.value = data.companies
    drives.value = data.drives
    applications.value = data.applications
}

onMounted(()=>{
    loadDashboard()
})
</script>

<template>
    <div class="container mt-5">
    <h2 class="mb-4">Admin Dashboard</h2>

        <div class="row">

            <div class="col-md-3 mb-3">
                <div class="card p-3 text-center">
                    <h5>Students</h5>
                    <p>{{ students }}</p>
                </div>
            </div>

            <div class="col-md-3 mb-3">
                <div class="card p-3 text-center">
                    <h5>Companies</h5>
                    <p>{{ companies }}</p>
                </div>
            </div>

            <div class="col-md-3 mb-3">
                <div class="card p-3 text-center">
                    <h5>Drives</h5>
                    <p>{{ drives }}</p>
                </div>
            </div>

            <div class="col-md-3 mb-3">
                <div class="card p-3 text-center">
                    <h5>Applications</h5>
                    <p>{{ applications }}</p>
                </div>
            </div>

        </div>
        <!-- Navigation Buttons -->
        <div class="mt-4">
            <router-link class="btn btn-primary me-3" to="/admin/companies">
                Manage Companies
            </router-link>

            <router-link class="btn btn-primary me-3" to="/admin/students">
                View Students
            </router-link>

            <router-link class="btn btn-primary" to="/admin/drives">
                Manage Drives
            </router-link>
        </div>       
    </div>
</template>