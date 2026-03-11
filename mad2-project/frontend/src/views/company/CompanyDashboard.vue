<script setup>
import { ref, onMounted } from 'vue'

const company_name = ref('')
const hr_contact = ref('')
const approval_status = ref('')
const drives = ref(0)
const applications = ref(0)

async function loadDashboard(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/company/dashboard',{
        headers:{
            'Authentication-Token': token
        }
    })

    if(!response.ok){
        alert("Failed to load dashboard")
        return
    }

    const data = await response.json()

    company_name.value = data.company_name
    hr_contact.value = data.hr_contact
    approval_status.value = data.approval_status
    drives.value = data.drives
    applications.value = data.applications
}

onMounted(()=>{
    loadDashboard()
})
</script>

<template>
    <div class="container mt-5">
    <h2 class="mb-4">Company Dashboard</h2>
        <div class="row">
            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Company</h5>
                    <p>{{ company_name }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>HR Contact</h5>
                    <p>{{ hr_contact }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Approval Status</h5>
                    <p>{{ approval_status }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Total Drives</h5>
                    <p>{{ drives }}</p>
                </div>
            </div>

            <div class="col-md-6 mb-3">
                <div class="card p-3">
                    <h5>Total Applications</h5>
                    <p>{{ applications }}</p>
                </div>
            </div>

        </div>

            <div class="mt-4">

            <router-link class="btn btn-primary me-3" to="/company/create-drive">
                Create Drive
            </router-link>

            <router-link class="btn btn-primary" to="/company/drives">
                View Drives
            </router-link>

            </div>
    </div>
</template>