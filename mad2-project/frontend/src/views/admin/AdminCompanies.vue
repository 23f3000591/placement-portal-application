<script setup>
import { ref, onMounted } from 'vue'

const companies = ref([])

async function loadCompanies(){

    const token = localStorage.getItem('token')

    const response = await fetch('http://127.0.0.1:5000/admin/companies',{
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    companies.value = data
}

async function updateStatus(id, action){

    const token = localStorage.getItem('token')

    const response = await fetch(`http://127.0.0.1:5000/admin/company/${action}/${id}`,{
        method:'POST',
        headers:{
            'Authentication-Token': token
        }
    })

    const data = await response.json()
    alert(data.message)

    loadCompanies()
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

    loadCompanies()
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

    loadCompanies()
}

onMounted(()=>{
    loadCompanies()
})
</script>

<template>
    <div class="container mt-5">
    <h2 class="mb-4">Manage Companies</h2>

        <table class="table table-bordered">
            <thead>
            <tr>
            <th>Company</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
            </tr>
            </thead>

            <tbody>
                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.approval_status }}</td>

                    <td>
                        <!-- Pending -->
                        <template v-if="company.approval_status === 'Pending'">
                            <button class="btn btn-success btn-sm me-2"
                                @click="updateStatus(company.id,'approve')">
                                Approve
                            </button>

                            <button class="btn btn-danger btn-sm"
                                @click="updateStatus(company.id,'reject')">
                                Reject
                            </button>
                        </template>

                        <!-- Approved but NOT blacklisted -->
                        <template v-else-if="company.approval_status === 'Approved' && !company.is_blacklisted">
                            <button class="btn btn-warning btn-sm"
                                @click="blacklist(company.user_id)">
                                Blacklist
                            </button>
                        </template>

                        <!-- Blacklisted -->
                        <template v-else-if="company.is_blacklisted">
                            <button class="btn btn-info btn-sm"
                                @click="whitelist(company.user_id)">
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