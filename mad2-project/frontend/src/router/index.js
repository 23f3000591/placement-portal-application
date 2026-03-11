import LandingPage from "@/views/LandingPage.vue"
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage,
    },

    // Auth views
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/auth/Login.vue')
    },
    {
      path: '/student/register',
      name: 'StudentRegister',
      component: () => import('../views/auth/StudentRegister.vue')
    },
    {
      path: '/company/register',
      name: 'CompanyRegister',
      component: () => import('../views/auth/CompanyRegister.vue')
    },
    
    //For Admin
    {
      path:'/admin/dashboard',
      name: 'AdminDashboard',
      component: () => import('../views/admin/AdminDashboard.vue')
    },
    {
      path:'/admin/companies',
      name: 'AdminCompanies',
      component: () => import('../views/admin/AdminCompanies.vue')
    },
    {
      path:'/admin/students',
      name: 'AdminStudents',
      component: () => import('../views/admin/AdminStudents.vue')
    },
    {
      path:'/admin/drives',
      name: 'AdminDrives',
      component: () => import('../views/admin/AdminDrives.vue')
    },

    // For Student
    {
      path: '/student/dashboard',
      name: 'StudentDashboard',
      component: () => import('../views/student/StudentDashboard.vue')
    },
    {
      path:'/student/drives',
      name: 'StudentDrives',
      component: () => import('../views/student/StudentDrives.vue')
    },
    {
      path:'/student/applications',
      name: 'StudentApplications',
      component: () => import('../views/student/StudentApplications.vue')
    },
    {
      path:'/student/profile',
      name: 'StudentProfile',
      component: () => import('../views/student/StudentProfile.vue')
    },

    // For Company
    {
      path: '/company/dashboard',
      name: 'CompanyDashboard',
      component: () => import('../views/company/CompanyDashboard.vue')
    },
    {
      path: '/company/drives',
      name: 'CompanyDrives',
      component: () => import('../views/company/CompanyDrives.vue')
    },
    {
      path: '/company/create-drive',
      name: 'CreateDrive',
      component: () => import('../views/company/CreateDrive.vue')
    },
    {
      path: '/company/applicants',
      name: 'CompanyApplicants',
      component: () => import('../views/company/CompanyApplicants.vue')
    }
  ],
})

export default router
