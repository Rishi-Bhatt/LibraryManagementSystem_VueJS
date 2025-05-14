<template>
<div class="home">
    <!-- Navigation-->
    <!-- <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
        <div id="login" class="container px-4 px-lg-5">
            <div>
                <router-link to="/UserLogin" class="navbar-brand ms-auto">
                    <h1>USER LOGIN</h1>
                </router-link>
                <router-view> </router-view>

            </div>

            <div>
                <router-link to="/LibrarianLogin" class="navbar-brand ms-auto">
                    <h1>LIBRARIAN LOGIN</h1>
                </router-link>
                <router-view> </router-view>

            </div>

            <div class="nav-link ms-auto px-lg-2 py-4 py-lg-3">
                <router-link to="/register" class="navbar-brand ms-auto">
                    <h1>REGISTER AS A NEW USER</h1>
                </router-link>
                <router-view> </router-view>

            </div>
        </div>
    </nav> -->
    <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
        <div id="login" class="container d-flex justify-content-between">
            <div class="nav-item">
                <router-link to="/UserLogin" class="navbar-brand">
                    USER LOGIN
                </router-link>
                <router-view></router-view>
            </div>

            <div class="nav-item">
                <router-link to="/LibrarianLogin" class="navbar-brand">
                    LIBRARIAN LOGIN
                </router-link>
                <router-view></router-view>
            </div>

            <div class="nav-item">
                <router-link to="/register" class="navbar-brand">
                    REGISTER AS A NEW USER
                </router-link>
                <router-view></router-view>
            </div>
        </div>
    </nav>

    <!-- Page Header-->
    <header class="masthead">
        <div class="container position-relative px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5 justify-content-center">
                <div class="col-md-10 col-lg-8 col-xl-7">
                    <div class="page-heading">
                        <h1>PUSTAKALAY</h1>
                        <span class="subheading">॥ विद्या ददाति विनयं ॥</span>
                        <router-view> </router-view>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content-->
    <main class="mb-0">
        <div class="container px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5 justify-content-center">
                <p>
                    Welcome to Pustakalay! Step into a world where every page holds a new adventure,
                    every shelf whispers secrets, and every book is a portal to knowledge.
                    Whether you seek to lose yourself in fiction, unravel the mysteries of history,
                    or delve into the depths of science, our library is here to ignite your curiosity
                    and inspire your imagination. Come, lose yourself in the magic of words and embark on
                    a journey that knows no limits. Explore, discover, and let the stories within these walls
                    transport you to new realms of possibility.
                </p>
                <router-view> </router-view>
            </div>
        </div>
    </main>

    <!-- Footer-->
    <footer class="border-top">
        <div class="small text-center text-muted fst-italic">Copyright &copy; Pustakalay 2024</div>
    </footer>
</div>
</template>

<script>
// @ is an alias to /src

export default {
    name: 'HomeView',

}
</script>

<style scoped>
@import '../assets/static/Index.css';
/* @import url("https://getbootstrap.com/docs/5.3/examples/sign-in/sign-in.css"); */
@import url("https://cdn.jsdelivr.net/npm/@docsearch/css@3");
@import url("https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css");
@import url("https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css");

#mainNav {
    background-color: transparent;
    
}

.navbar-brand {
    font-weight: bold;
    font-style: italic;
    font-size: 1.75rem;
}

.nav-item {
    flex: 1;
    text-align: center;
    
}

* {
    padding: 0;
    margin: 0;
    font-family: monospace;
    font-size: large;
}
</style>
