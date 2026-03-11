<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const company_name = ref('')
const hr_contact = ref('')

async function register(){

    const company = {
        email: email.value,
        password: password.value,
        company_name: company_name.value,
        hr_contact: hr_contact.value
    }

    const response = await fetch('http://127.0.0.1:5000/company/register', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(company)
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
            <div class="col-5">
                <h2 class="mb-4 text-center">Company Registration</h2>

                    <form @submit.prevent="register">

                        <div class="mb-3">
                            <label class="form-label">Company Email</label>
                            <input type="email" class="form-control" v-model="email" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" v-model="password" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Company Name</label>
                            <input type="text" class="form-control" v-model="company_name" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">HR Contact</label>
                            <input type="text" class="form-control" v-model="hr_contact" required>
                        </div>

                        <button class="btn btn-primary w-100">
                            Register Company
                        </button>

                    </form>

            </div>
        </div>
    </div>
</template>