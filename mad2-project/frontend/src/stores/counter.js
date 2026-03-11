import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {

    const token = ref(localStorage.getItem('token') || null)
    const user = ref(null)

    function setUserCred(auth_token, user_data){
        token.value = auth_token
        user.value = user_data

        localStorage.setItem('token', auth_token)
    }

    function logout(){
        token.value = null
        user.value = null

        localStorage.removeItem('token')
    }

    return {
        token,
        user,
        setUserCred,
        logout
    }

})