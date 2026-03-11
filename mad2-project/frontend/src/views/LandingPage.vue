<template>
    <div>
        <!-- Hero Section -->
        <div class="container d-flex flex-column justify-content-center align-items-center text-center vh-100">
            <h1 class="display-4 fw-bold">
                <span class="text-primary">Campus</span> Placement Portal
            </h1>

            <p class="lead text-muted mt-3">
                Connecting Students and Recruiters Seamlessly
            </p>

            <div class="mt-5 d-flex gap-3">
                <router-link to="/company/register" class="btn btn-primary btn-lg px-4">
                    Hire Talent
                </router-link>

                <router-link to="/student/register" class="btn btn-outline-primary btn-lg px-4">
                    Get Hired
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LandingPage"
}
</script>