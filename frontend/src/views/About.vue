<template>
<div id="about">

    <body>

        <!-- Navbar Start -->
        <nav class="navbar navbar-expand-lg" style="background-color: rgb(250, 170, 31);">
            <router-link to="/UserDashboard" class="navbar-brand">
                <!-- <img :src="require('@/assets/static/images/about_us.png')" alt="Logo"> -->
                <h6>Go back to User Dashboard</h6>
            </router-link>

            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="link" href="mailto:21f1000330@ds.study.iitm.ac.in">Contact</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/UserDashboard" class="link">
                            <h6>Go back to User Dashboard</h6>
                        </router-link>
                    </li>
                </ul>
            </div>
        </nav>
        <!-- Navbar Ends -->

        <h1>About Us</h1>
        <p>
            <br>
            <div>
                <strong>
                    <h5>Mission : </h5>
                </strong> We are committed to revolutionizing library management through innovative technology solutions that streamline operations and enhance user experience.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>History : </h5>
                </strong> Established with a passion for modernizing library administration, we embarked on a journey to simplify processes and empower librarians.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>Team : </h5>
                </strong> Our diverse team comprises dedicated professionals with expertise in software development, user experience design, and library science.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>Values : </h5>
                </strong> We prioritize integrity, collaboration, and continuous improvement to deliver cutting-edge solutions tailored to the evolving needs of libraries.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>Approach : </h5>
                </strong> By combining industry knowledge with advanced technology, we offer intuitive and scalable systems that optimize library workflows.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>Impact : </h5>
                </strong> Our solutions have empowered libraries worldwide, facilitating efficient resource management and fostering a love for learning.<br>
            </div>
            <br>
            <br>
            <div>
                <strong>
                    <h5>Vision : </h5>
                </strong> We aspire to be the forefront of library technology, shaping the future of information access and knowledge dissemination globally.<br>
            </div>
            <br>
            <br>

        </p>
        <!-- FOOTER -->
        <footer class="text-white-50">
            <p>&copy; 2024 Pustakalay &nbsp;
                <router-link to="/register" class="text-white">
                    <h6>Register</h6>
                </router-link>,

                Developed by Rishi Bhatt .</p>
        </footer>

    </body>

</div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'about',

};
</script>

<style scoped>
/* @import '../assets/static/about_us.css'; */
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
