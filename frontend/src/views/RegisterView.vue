<template>
<div class="register">


    <body class="d-flex align-items-center py-4 bg-body-tertiary">
        <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
            <symbol id="check2" viewBox="0 0 16 16">
                <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" />
            </symbol>
            <symbol id="circle-half" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 0 8 1v14zm0 1A8 8 0 1 1 8 0a8 8 0 0 1 0 16z" />
            </symbol>
            <symbol id="moon-stars-fill" viewBox="0 0 16 16">
                <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z" />
                <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z" />
            </symbol>
            <symbol id="sun-fill" viewBox="0 0 16 16">
                <path d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z" />
            </symbol>
        </svg>
        <!-- <-- <button class="btn btn-primary w-100 py-2" type="radio"></button> User </button> -->
        <main class="form-signin w-100 m-auto">
            <form>

                <img class="mb-1" src="../assets/static/images/register.png" alt="" width="288" height="228">
                <h1 class="h3 mb-0 fw-normal">Please Enter New User Details</h1>

                <div class="form-floating">
                    <input type="text" class="form-control" v-model="username" id="username" name="username" placeholder="username">
                    <label for="username">Username</label>
                </div>
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="email" id="email" name='email' placeholder="email">
                    <label for="email">Email address</label>
                </div>
                <div class="form-floating">
                    <input type="password" class="form-control" v-model="password" id="password" name="password" placeholder="password">
                    <label for="password">Password</label>
                </div>

                <!-- <button class="btn btn-primary w-100 py-2" type="submit">Register Now</button> -->
                <button class="btn btn-primary w-100 py-2" type="button" @click="register">Register Now</button>
                <div>
                    <router-link to="/">
                        <h6>Go to Home page</h6>
                    </router-link>
                    <router-view></router-view>
                    Already a User ?
                    <router-link to="/UserLogin">
                        
                        <h6>Go to User Login</h6>
                    </router-link>
                    <router-view></router-view>
                </div>
            </form>
        </main>

    </body>
</div>
</template>
<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
    name: 'register',
    data() {
        return {
            username: '',
            email: '',
            password: ''
        };
    },
    methods: {
        async register() {
            console.log('Registering user:', {
                username: this.username,
                email: this.email,
                password: this.password
            });

            try {
                const response = await axios.post('http://localhost:5000/api/register', {
                    username: this.username,
                    email: this.email,
                    password: this.password
                });

                if (response.status === 201) {
                    console.log('New user registered successfully');
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: `New user ${response.data.username} registered successfully!`,
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.$router.push('/');
                    });
                } else {
                    console.log('Registration failed');
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Registration failed. Please try again.',
                        confirmButtonText: 'OK'
                    });
                }
            } catch (error) {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    console.log('Error data:', error.response.data);
                    console.log('Error status:', error.response.status);
                    console.log('Error headers:', error.response.headers);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.response.data.message || 'An error occurred while registering.',
                        confirmButtonText: 'OK'
                    });
                } else if (error.request) {
                    // The request was made but no response was received
                    console.log('Error request:', error.request);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'No response received from the server.',
                        confirmButtonText: 'OK'
                    });
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error message:', error.message);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'An unexpected error occurred. Please try again.',
                        confirmButtonText: 'OK'
                    });
                }
            }
        }
    }
};
</script>

<style scoped>
@import url("https://getbootstrap.com/docs/5.3/examples/sign-in/sign-in.css");
@import url("https://cdn.jsdelivr.net/npm/@docsearch/css@3");
@import url("https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css");
@import url("https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css");
* {
    padding: 0;
    margin: 0;
    font-family: monospace;
    font-size: large;
}

.bd-placeholder-img {
    font-size: 1.125rem;
    text-anchor: middle;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
}

@media (min-width: 768px) {
    .bd-placeholder-img-lg {
        font-size: 3.5rem;
    }
}

.b-example-divider {
    width: 100%;
    height: 3rem;
    background-color: rgba(0, 0, 0, .1);
    border: solid rgba(0, 0, 0, .15);
    border-width: 1px 0;
    box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
}

.b-example-vr {
    flex-shrink: 0;
    width: 1.5rem;
    height: 100vh;
}

.bi {
    vertical-align: -.125em;
    fill: currentColor;
}

.nav-scroller {
    position: relative;
    z-index: 2;
    height: 2.75rem;
    overflow-y: hidden;
}

.nav-scroller .nav {
    display: flex;
    flex-wrap: nowrap;
    padding-bottom: 1rem;
    margin-top: -1px;
    overflow-x: auto;
    text-align: center;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
}

.btn-bd-primary {
    --bd-violet-bg: #712cf9;
    --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

    --bs-btn-font-weight: 600;
    --bs-btn-color: var(--bs-white);
    --bs-btn-bg: var(--bd-violet-bg);
    --bs-btn-border-color: var(--bd-violet-bg);
    --bs-btn-hover-color: var(--bs-white);
    --bs-btn-hover-bg: #6528e0;
    --bs-btn-hover-border-color: #6528e0;
    --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
    --bs-btn-active-color: var(--bs-btn-hover-color);
    --bs-btn-active-bg: #5a23c8;
    --bs-btn-active-border-color: #5a23c8;
}

.bd-mode-toggle {
    z-index: 1500;
}

.bd-mode-toggle .dropdown-menu .active .bi {
    display: block !important;
}

ul {
    list-style: none;
    background: #22438C;
}

ul li {
    display: inline-block;
    position: relative;
    color: #FFF;
}

ul li a {
    display: block;
    padding: 20px 25px;
    color: #FFF;
    text-decoration: none;
    text-align: center;
    font-size: 20px;

}

ul li ul.dropdown li {
    display: block;

}

ul li ul.dropdown {
    width: 100%;
    background: #22438C;
    position: absolute;
    z-index: 999;
    display: none;

}

ul li a:hover {
    background: #112C66;

}

ul li:hover ul.dropdown {
    display: block;
}
</style>
