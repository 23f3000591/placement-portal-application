<script setup>
import { ref, onMounted } from 'vue'

const students = ref([])

async function loadStudents(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/admin/students',{
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    students.value = data
}

async function blacklist(user_id){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/admin/blacklist/${user_id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    alert(data.message)

    loadStudents()
}

async function whitelist(user_id){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/admin/unblacklist/${user_id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    alert(data.message)

    loadStudents()
}

onMounted(()=>{
    loadStudents()
})
</script>


<template>
    <div class="container mt-5">
        <h2 class="mb-4">Students</h2>
        <table class="table table-bordered">
            <thead>
            <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Branch</th>
            <th>Year</th>
            <th>CGPA</th>
            <th>Status</th>
            <th>Actions</th>
            </tr>
            </thead>

            <tbody>
                <tr v-for="student in students" :key="student.id">
                    <td>{{ student.name }}</td>
                    <td>{{ student.email }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.year }}</td>
                    <td>{{ student.cgpa }}</td>

                    <td>
                        <span v-if="!student.is_blacklisted" class="badge bg-success">
                            Active
                        </span>

                        <span v-else class="badge bg-danger">
                            Blacklisted
                        </span>
                    </td>

                    <td>
                        <!-- If student NOT blacklisted -->
                        <template v-if="!student.is_blacklisted">
                            <button class="btn btn-warning btn-sm" @click="blacklist(student.user_id)">
                                Blacklist
                            </button>
                        </template>

                        <!-- If student blacklisted -->
                        <template v-else>
                            <button class="btn btn-info btn-sm" @click="whitelist(student.user_id)">
                                Whitelist
                            </button>
                        </template>
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