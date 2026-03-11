<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const name = ref('')
const edu_level = ref('')
const branch = ref('')
const year = ref('')
const contact = ref('')
const cgpa = ref('')
const github = ref('')
const linkedin = ref('')

async function register(){

    const student = {
        email: email.value,
        password: password.value,
        name: name.value,
        edu_level: edu_level.value,
        branch: branch.value,
        year: year.value,
        contact: contact.value,
        cgpa: cgpa.value,
        github: github.value,
        linkedin: linkedin.value
    }

    const response = await fetch('http://127.0.0.1:5000/student/register',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(student)
    })

    if(!response.ok){
        const errordata = await response.json()
        alert(errordata.message)
        return
    }

    const data = await response.json()

    alert(data.message)

    router.push('/login')
}
</script>


<template>
    <div class="container-fluid">
        <div class="row justify-content-center mt-5">
            <div class="col-6">
            <h2 class="mb-4 text-center">Student Registration</h2>
                <form @submit.prevent="register">

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" v-model="email" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input type="text" class="form-control" v-model="name" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Education Level</label>
                        <select class="form-control" v-model="edu_level">
                            <option value="Bachelors">Bachelors</option>
                            <option value="Masters">Masters</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Branch</label>
                        <input type="text" class="form-control" v-model="branch">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Year</label>
                        <input type="number" class="form-control" v-model="year">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Contact</label>
                        <input type="text" class="form-control" v-model="contact">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">CGPA</label>
                        <input type="number" step="0.01" class="form-control" v-model="cgpa">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">GitHub</label>
                        <input type="text" class="form-control" v-model="github">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">LinkedIn</label>
                        <input type="text" class="form-control" v-model="linkedin">
                    </div>

                    <button class="btn btn-primary w-100">
                        Register
                    </button>

                </form>
            </div>
        </div>
    </div>
</template>