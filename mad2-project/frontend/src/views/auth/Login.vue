<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth_store = useAuthStore()

const email = ref('')
const password = ref('')

async function login(){

    const user = {
        email: email.value,
        password: password.value
    }

    const response = await fetch('http://127.0.0.1:5000/login',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify(user)
    })

    if(!response.ok){
        const err = await response.json()
        alert(err.message)
        return
    }

    const data = await response.json()

    // save login state in Pinia
    auth_store.setUserCred(data.auth_token, data.user)

    const role = data.user.roles[0]

    if(role === 'student'){
        router.push('/student/dashboard')
    }
    else if(role === 'company'){
        router.push('/company/dashboard')
    }
    else{
        router.push('/admin/dashboard')
    }
}
</script>


<template>
<div class="container-fluid">

    <div class="row justify-content-center mt-5">

        <div class="col-4">

            <h2 class="mb-4 text-center">Login</h2>

            <form @submit.prevent="login">

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input
                        type="email"
                        class="form-control"
                        v-model="email"
                        required
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input
                        type="password"
                        class="form-control"
                        v-model="password"
                        required
                    >
                </div>

                <button type="submit" class="btn btn-primary w-100">
                    Login
                </button>

            </form>

        </div>

    </div>

</div>
</template>