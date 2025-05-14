<template>
<div id="feedback">

    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
            <div class="container px-4 px-lg-5">
                <router-link to="/UserDashboard" class="navbar-brand">
                    <!-- <img :src="require('@/assets/static/images/about_us.png')" alt="Logo"> -->
                    <h6>Go back to User Dashboard</h6>
                </router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav ms-auto py-4 py-lg-0">
                        <li class="nav-item">
                            <router-link to="/UserDashboard" class="nav-link px-lg-3 py-3 py-lg-4">
                                <h6>User Dashboard</h6>
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link to="/about" class="nav-link px-lg-3 py-3 py-lg-4">
                                <h6>About</h6>
                            </router-link>
                        </li>

                        <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="mailto:21f1000330@ds.study.iitm.ac.in">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Page Header-->
        <header class="masthead">
            <div class="container position-relative px-4 px-lg-5">
                <div class="row gx-4 gx-lg-5 justify-content-center">
                    <div class="col-md-10 col-lg-8 col-xl-7">
                        <div class="page-heading">
                            <h1>Feedback</h1>
                            <span class="subheading">Please provide a Constructive Feedback</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        <!-- Main Content-->
        <main class="mb-4">
        <div class="container px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5 justify-content-center">
                <div class="col-md-10 col-lg-8 col-xl-7">
                    <p>Want to get in touch? Fill out the form below to send me a message and I will get back to you as soon as possible!</p>
                    <div class="my-5">
                        <form @submit.prevent="submitFeedback">
                            <div class="form-floating">
                                <input class="form-control" name="name" v-model="form.name" id="name" type="text" placeholder="Enter your name..." required />
                                <label for="name">Name</label>
                            </div>
                            <div class="form-floating">
                                <input class="form-control" name="email" v-model="form.email" id="email" type="email" placeholder="Enter your email..." required />
                                <label for="email">Email address</label>
                            </div>
                            <div class="form-floating">
                                <input class="form-control" name="phone" v-model="form.phone" id="phone" type="tel" placeholder="Enter your phone number..." required />
                                <label for="phone">Phone Number</label>
                            </div>
                            <div class="form-floating">
                                <input class="form-control" name="rating" v-model="form.rating" id="rating" type="number" placeholder="Enter Book Rating..." required />
                                <label for="rating">Rate the book on a scale of 1 to 10</label>
                            </div>
                            <div class="form-floating">
                                <textarea class="form-control" name="message" v-model="form.message" id="message" placeholder="Enter your message here..." style="height: 12rem" required></textarea>
                                <label for="message">Message</label>
                            </div>
                            <br />
                            <button class="btn btn-info" type="submit">Send</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <footer class="border-top">
        <div class="container px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5 justify-content-center">
                <div class="col-md-10 col-lg-8 col-xl-7">
                    <ul class="list-inline text-center"></ul>
                    <div class="small text-center text-muted fst-italic">Copyright &copy; Pustakalay 2024</div>
                </div>
            </div>
        </div>
    </footer>

    </body>

</div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
    name: 'feedback',
    data() {
        return {
            form: {
                name: '',
                email: '',
                phone: '',
                rating: '',
                message: '',
                user_id: 1, // Replace with the actual user_id from session or JWT
                book_id: 1  // Replace with the actual book_id from the context
            }
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        this.userId = localStorage.getItem('user_id');
        this.username = localStorage.getItem('user_name');
        if (!this.token) {
            console.log("Token not found");
            Swal.fire({
                icon: 'error',
                title: 'Login Required',
                text: 'Please login again.',
                confirmButtonText: 'OK'
            }).then(() => {
                this.$router.push('/UserLogin');
            });
        } else {
            this.submitFeedback();
        }
    },
    methods: {
        async submitFeedback() {
            try {
                const response = await axios.post('http://localhost:5000/api/feedback', this.form, {
                    // headers: {
                    //     Authorization: `Bearer ${this.token}`
                    // }, 
                    });
                if (response.status === 201) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Feedback Sent',
                        text: 'Your feedback was noted.',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.$router.push('/UserIssuedBooksView'); // Redirect to the desired page
                    });
                    this.form = {
                        name: '',
                        email: '',
                        phone: '',
                        rating: '',
                        message: '',
                        user_id: 1,
                        book_id: 1
                    };
                } else {
                    throw new Error('Unexpected response status');
                }
            } catch (error) {
                if (error.response && error.response.data) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.response.data.error,
                        confirmButtonText: 'OK'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error sending message!',
                        confirmButtonText: 'OK'
                    });
                }
            }
        }
    }
};
</script>



<style scoped>
/* @import '../assets/static/FeedbackStyles.css'; */
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
</style>
