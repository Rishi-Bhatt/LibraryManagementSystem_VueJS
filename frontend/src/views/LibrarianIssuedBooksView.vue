<template>
<div class="librarianissuedbooksview">

    <body>

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

        <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
            <symbol id="chevron-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
            </symbol>
        </svg>

        <nav class="navbar navbar-expand-md navbar-dark bg-dark">

            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample04" aria-controls="navbarsExample04" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <a class="navbar-brand ms-auto" href="#">View all issued books</a>

            <router-link to="/LibrarianDashboard" class="navbar-brand ms-auto">
                <h6>Go back to Librarian Dashboard</h6>
            </router-link>

            <!-- Update the search input with v-model and @input event -->
            <div class="search-bar ms-auto">
                <input type="text" v-model="searchQuery" @input="searchIssuedBooks" placeholder="Search">
            </div>

        </nav>
        <div class="my-2 p-2 bg-body rounded shadow-sm">

            <table class="table align-middle caption-top table-primary table-hover table-borderless">
                <caption class="caption-top">Users have issued these books :</caption>
                <thead>
                    <tr>
                        <th scope="col" style="width: 5%;">Issued To</th>
                        <th scope="col" style="width: 5%;">Book</th>
                        <th scope="col" style="width: 5%;">Author</th>
                        <th scope="col" style="width: 5%;">Section</th>
                        <th scope="col" style="width: 6%;">Issued At</th>
                        <th scope="col" style="width: 6%;">Return Before</th>
                        <th scope="col" style="width: 5%;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(issued, index) in issuedBooks" :key="index">
                        <td>{{ issued.username }}</td>
                        <td>{{ issued.book_name }}</td>
                        <td>{{ issued.book_author }}</td>
                        <td>{{ issued.section_name }}</td>
                        <td>{{ issued.issued_at }}</td>
                        <td>{{ issued.return_before }}</td>
                        <td>
                            <div class="btn-group">
                                <a @click="revokeIssuedBook(issued.issue_id)" class="btn btn-outline-danger btn-sm">Revoke</a>
                            </div>
                        </td>
                    </tr>
                    <tr v-if="issuedBooks.length === 0">
                        <td colspan="6">No issued books found</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </body>
</div>
</template>
<script>
import axios from 'axios';
import { DateTime } from 'luxon';
import Swal from 'sweetalert2';

export default {
    name: 'LibrarianIssuedBooksView',
    data() {
        return {
            token: null,
            issuedBooks: [],
            searchQuery: '' // Add this line
        };
    },

    created() {
        this.token = localStorage.getItem('token');
        if (!this.token) {
            console.log("Token not found");
            Swal.fire({
                icon: 'warning',
                title: 'Login Required',
                text: 'Please log in again to continue.',
                confirmButtonText: 'OK'
            }).then(() => {
                this.$router.push('/UserLogin');
            });
        } else {
            this.fetchIssuedBooks();
        }
    },
    methods: {
        async fetchIssuedBooks() {
            try {
                const response = await axios.get('http://localhost:5000/api/approve_request', {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    },
                    params: {
                        search: this.searchQuery // Add search parameter
                    }
                });

                if (response.status === 200) {
                    this.issuedBooks = response.data.data.map(issued => ({
                        ...issued,
                        issued_at: issued.issued_at ? DateTime.fromISO(issued.issued_at).toFormat('dd/MM/yyyy HH:mm:ss') : 'Not Set',
                        return_before: issued.return_before ? DateTime.fromISO(issued.return_before).toFormat('dd/MM/yyyy HH:mm:ss') : 'Not Set'
                    }));
                } else {
                    console.log('Unexpected response status:', response.status);
                }
            } catch (error) {
                console.log(error);
                Swal.fire({
                    icon: 'error',
                    title: 'Fetch Error',
                    text: 'Failed to fetch issued books. Please try again later.',
                    confirmButtonText: 'OK'
                });
            }
        },

        // Call fetchIssuedBooks whenever searchQuery changes
        searchIssuedBooks() {
            this.fetchIssuedBooks();
        },

        async revokeIssuedBook(issueId) {
            try {
                const response = await axios.delete('http://localhost:5000/api/approve_request', {
                    data: {
                        issue_id: issueId
                    },
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    }
                });

                if (response.status === 200) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Revocation Successful',
                        text: 'Issued book revoked successfully.',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.fetchIssuedBooks(); // Refresh the list of issued books
                    });
                } else {
                    console.log('Unexpected response status:', response.status);
                }
            } catch (error) {
                console.log(error);
                Swal.fire({
                    icon: 'error',
                    title: 'Revocation Error',
                    text: 'Failed to revoke issued book. Please try again later.',
                    confirmButtonText: 'OK'
                });
            }
        }
    }
};
</script>

<style scoped>
@import '../assets/static/dashboard-style.css';
@import url("https://getbootstrap.com/docs/5.3/examples/sign-in/sign-in.css");
@import url("https://cdn.jsdelivr.net/npm/@docsearch/css@3");
@import url("https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css");
@import url("https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css");

caption {
    caption-side: top;
    font-weight: bold;
    font-size: 1.25rem;
    color: #6b08ad;
    /* Change this color to your preferred color */
}

.top-navbar {
    background-color: #333;
    height: 40px;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
}

.navbar-nav {
    flex: 1;
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.nav-link,
.navbar-brand h6 {
    color: white;
    font-size: 1.3rem;
}

.navbar-brand {
    color: white;
    font-size: 1.3rem;
}

.search-bar {
    display: flex;
    align-items: center;
}

.search-bar input {
    font-size: 1rem;
    padding: 0.5rem;
    border: none;
    border-radius: 0.25rem;
    background-color: white;
    color: black;
}

table {
    width: 100%;
    table-layout: fixed;
}

th,
td {
    text-align: center;
    padding: 10px;
    border: 1px solid #ddd;
    white-space: nowrap;
    /* Prevent content from wrapping */
}

th,
td {
    text-align: center;
    vertical-align: middle;
}

.btn {
    padding: 5px 10px;
    margin: 0 2px;
    /* Reduce spacing between buttons */
}

.table-hover tbody tr:hover {
    background-color: #f5f5f5;
}

.btn-group {
    display: flex;
    justify-content: center;
    gap: 5px;
    /* Add small spacing between buttons */
}

* {
    padding: 0;
    margin: 0;
    font-family: monospace;
    font-size: large;
}

.my-button {
    display: block;
    margin: auto;
}

c2 {
    text-align: center;
    margin: auto;
    display: flex;
    justify-content: space-between;
    display: grid;
}

class12 {
    text-align: center;
    margin: auto;
    display: flex;
}
</style>
