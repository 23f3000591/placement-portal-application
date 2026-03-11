<script setup>
import { ref } from 'vue'

const job_title = ref('')
const job_description = ref('')
const min_cgpa = ref('')
const allowed_edu_level = ref('')
const allowed_branch = ref('')
const allowed_year = ref('')
const deadline = ref('')

async function createDrive(){

    console.log("Create drive clicked")

    const token = localStorage.getItem('token')

    const drive = {
        job_title: job_title.value,
        job_description: job_description.value,
        min_cgpa: min_cgpa.value,
        allowed_edu_level: allowed_edu_level.value,
        allowed_branch: allowed_branch.value,
        allowed_year: allowed_year.value,
        deadline: deadline.value
    }

    console.log("Sending:", drive)

    const response = await fetch('http://127.0.0.1:5000/company/create-drive',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Authentication-Token': token
        },
        body: JSON.stringify(drive)
    })

    console.log("Response status:", response.status)

    const data = await response.json()

    console.log("Response data:", data)

    alert(data.message)
}
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">Create Placement Drive</h2>

        <form @submit.prevent="createDrive">

            <div class="mb-3">
                <label>Job Title</label>
                <input type="text" class="form-control" v-model="job_title">
            </div>

            <div class="mb-3">
                <label>Description</label>
                <textarea class="form-control" v-model="job_description"></textarea>
            </div>

            <div class="mb-3">
                <label>Minimum CGPA</label>
                <input type="number" step="0.1" class="form-control" v-model="min_cgpa">
            </div>

            <div class="mb-3">
                <label>Education Level</label>
                <input type="text" class="form-control" v-model="allowed_edu_level">
            </div>

            <div class="mb-3">
                <label>Branch</label>
                <input type="text" class="form-control" v-model="allowed_branch">
            </div>

            <div class="mb-3">
                <label>Year</label>
                <input type="number" class="form-control" v-model="allowed_year">
            </div>

            <div class="mb-3">
                <label>Deadline</label>
                <input type="date" class="form-control" v-model="deadline">
            </div>

            <button class="btn btn-primary">
                Create Drive
            </button>

        </form>
    </div>
    <div class="mt-3">
        <router-link class="btn btn-primary" to="/company/dashboard">
            Go to Dashboard
        </router-link>
    </div>
</template>