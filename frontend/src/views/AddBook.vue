<template>
<div id="addbook">

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

        <main class="form-signin w-100 m-auto">
            <form @submit.prevent="submitForm">
                <img class="my-button mb-1" src="../assets/static/images/add_book.png" alt="" width="288" height="228">
                <h1 class="h3 mb-0 fw-normal"> Add Details of New Book under {{ this.section_name }} </h1>
                <br>
                <div class="form-group">
                    <label for="book_name">Book Name</label>
                    <input type="text" name="book_name" v-model="this.book_name" class="form-control" id="book_name" placeholder="Enter the name of book" required="required">
                </div>
                <div class="form-group">
                    <label for="book_author" required="required">Author Name (s)</label>
                    <input type="text" name="book_author" v-model="this.book_author" class="form-control" id="book_author" aria-describedby="names" placeholder="Enter Author Names">
                </div>
                <div class="form-group">
                    <label for="DownloadPrice">Set Download Price</label>
                    <input type="text" name="DownloadPrice" v-model="this.DownloadPrice" class="form-control" id="DownloadPrice" aria-describedby="names" placeholder="Specify Price toDownload eBook PDF">

                </div>
                <hr>
                <div class="form-group mt-3">
                    <label class="mr-6">Upload Book:</label>
                    <input type="file" @change="handleFileUpload" name="file">
                </div>

                <button type="submit" class="btn btn-primary w-100 py-2"> Submit </button>

            </form>
        </main>
    </body>
</div>
</template>


<script>
import axios from 'axios';
import { DateTime } from 'luxon';
import Swal from 'sweetalert2';

export default {
    name: 'addbook',
    props: {
        section_id: {
            type: String,
            required: true
        },
        section_name: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            book_name: '',
            book_author: '',
            DownloadPrice: 0,
            book_content: null,
            token: '',
            role: '',
            message: ''
        };
    },
    created() {
        this.token = localStorage.getItem('token');
        this.role = localStorage.getItem('user_role');
        if (!this.token) {
            this.$router.push('/LibrarianLogin');
        }
    },
    methods: {
        async submitForm() {
            // Submit logic to save the book details including section_id
            const formData = new FormData();
            formData.append('book_name', this.book_name);
            formData.append('book_author', this.book_author);
            formData.append('DownloadPrice', this.DownloadPrice);
            formData.append('book_content', this.book_content);
            formData.append('section_id', this.section_id);
            formData.append('section_name', this.section_name);
            
            try {
                const response = await axios.post('http://localhost:5000/api/ebooks', formData, {
                    headers: {
                        Authorization: `Bearer ${this.token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.status === 201) {
                    this.message = response.data;
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Book added successfully!',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.$router.push(`/booksportal/${this.section_name}/${this.section_id}`);
                    });
                }
            } catch (error) {
                if (error.response) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.response.data.message || 'An error occurred while adding the book.',
                        confirmButtonText: 'OK'
                    });
                } else if (error.request) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'No response received from the server.',
                        confirmButtonText: 'OK'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.message || 'An unexpected error occurred.',
                        confirmButtonText: 'OK'
                    });
                }
            }
        },
        handleFileUpload(event) {
            this.book_content = event.target.files[0];
        }
    }
};
</script>

<style scoped>
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

.h1 {
    font-size: 20px;
    margin-top: 24px;
    margin-bottom: 24px;
}

.img {
    height: 100px;
}

.my-button {
    display: block;
    margin: auto;
}
</style>
