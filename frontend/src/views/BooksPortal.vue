<template>
<div id="booksportal">

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

        <nav class="top-navbar">
            BOOKS PORTAL
        </nav>
        
    
        <nav class="navbar navbar-expand-md bg-dark sticky-top border-bottom" data-bs-theme="dark">
            <div class="container">
                <a class="navbar-brand d-md-none" href="#">
                    <svg class="bi" width="24" height="24">
                        <use xlink:href="#aperture" />
                    </svg>
                    Pustakalay
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" aria-controls="offcanvas" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">
                    <div class="offcanvas-header">
                        <h5 class="offcanvas-title" id="offcanvasLabel">Pustakalay</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                    <div class="offcanvas-body">
                        <ul class="navbar-nav flex-grow-1">
                            <li class="nav-item ms-auto">
                                <a class="nav-link" href="/LibrarianDashboard">Go to Librarian Dashboard</a>
                            </li>
                            <li class="nav-item ms-auto">
                                <router-link :to="{ name: 'addbook', params: { section_id: section_id }}" class="navbar-brand">
                                    <h6>ADD BOOK</h6>
                                </router-link>
                            </li>
                            <li class="nav-item ms-auto search-bar">
                                <input type="text" v-model="searchQuery" @input="searchBooks" placeholder="Search">
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <div class="my-2 p-2 bg-body rounded shadow-sm">
            <table class="table align-middle caption-top table-borderless table-info table-hover">
                <caption class="caption-top">List of eBooks in {{ section_name.toUpperCase() }} eSection:</caption>
                <thead>
                    <tr>
                        <th scope="col" style="width: 3%">ID</th>
                        <th scope="col" style="width: 9%">Book</th>
                        <th scope="col" style="width: 9%">Author</th>
                        <th scope="col" style="width: 5%">Content</th>
                        <th scope="col" style="width: 5%">Price</th>
                        <th scope="col" style="width: 9%">Created_At</th>
                        <th scope="col" style="width: 9%">Updated_At</th>
                        <th scope="col" colspan="2" style="width: 10%"> Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(eb, index) in filteredEbooks" :key="eb.book_id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ eb.book_name }}</td>
                        <td>{{ eb.book_author }}</td>
                        <td>
                            <a :href="`http://localhost:5000/api/ebooks/${eb.book_id}/pdf`" target="_blank" class="btn btn-outline-success btn-sm">
                                Read
                            </a>
                        </td>
                        <td>{{ eb.DownloadPrice }}</td>
                        <td>{{ formatDate(eb.date_created) }}</td>
                        <td>{{ formatDate(eb.updated_at) }}</td>
                        <td colspan="2">
                            <div class="btn-group">
                                <router-link :to="{ name: 'updatebook', params: { book_id: eb.book_id, section_id: section_id, section_name: section_name }}" class="btn btn-outline-success btn-sm">
                                    Update
                                </router-link>
                                <button class="btn btn-outline-danger btn-sm" type="button" @click.prevent="DeleteEBook(eb.book_id)">
                                    Remove
                                </button>
                            </div>
                        </td>
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
    name: 'booksportal',
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
            searchQuery: '',
            ebooks: [],
            token: null
        };
    },
    created() {
        this.token = localStorage.getItem('token');
        if (!this.token) {
            this.$router.push('/LibrarianLogin');
        } else {
            this.GetEBooks();
        }
    },
    computed: {
        filteredEbooks() { 
            const query = this.searchQuery.trim().toLowerCase();
            if (!query) {
                return this.ebooks.filter(eb => Number(eb.sectionid) === Number(this.section_id));
            }
            return this.ebooks.filter(eb =>
                (eb.book_name && eb.book_name.toLowerCase().includes(query)) ||
                (eb.book_author && eb.book_author.toLowerCase().includes(query)) ||
                (eb.DownloadPrice && eb.DownloadPrice.toString().includes(query))
            ).filter(eb => Number(eb.sectionid) === Number(this.section_id));
        }
    },
    methods: {
        formatDate(dateStr) {
            if (!dateStr) {
                return 'None';
            }
            return DateTime.fromISO(dateStr).toFormat('dd/MM/yyyy HH:mm:ss');
        },
        searchBooks() {
            // Triggered on input, no debounce
        },
        async GetEBooks() {
            try {
                const response = await axios.get('http://localhost:5000/api/ebooks', {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    },
                });

                if (response.status === 200) {
                    this.ebooks = response.data.EBdata;
                }
            } catch (error) {
                console.log(error);
                Swal.fire({
                    icon: 'error',
                    title: 'Fetch Error',
                    text: 'Failed to fetch eBooks. Please try again later.',
                    confirmButtonText: 'OK'
                });
            }
        },
        async DeleteEBook(book_id) {
            try {
                const response = await axios.delete(`http://localhost:5000/api/ebooks/${book_id}`, {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    },
                });

                if (response.status === 200) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'eBook deleted successfully.',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.GetEBooks();
                    });
                }
            } catch (error) {
                if (error.response) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.response.data.message || 'Failed to delete eBook.',
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
        }
    }
};
</script>







<style scoped>
@import url("https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css");

caption {
    caption-side: top;
    font-weight: bold;
    font-size: 1.25rem;
    color: #6b08ad;
    /* text-transform: uppercase; */
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
    /* Ensures columns have equal widths */
}

th,
td {
    text-align: center;
    padding: 10px;
    border: 1px solid #ddd;
    white-space: nowrap;
    /* Prevents content from wrapping */
    overflow: hidden;
    /* Ensures content does not overflow */
    text-overflow: ellipsis;
    /* Adds ellipsis for overflowed content */
}

th:first-child,
td:first-child {
    width: 5%;
}

th:nth-child(2),
td:nth-child(2),
th:nth-child(3),
td:nth-child(3),
th:nth-child(4),
td:nth-child(4),
th:nth-child(5),
td:nth-child(5),
th:nth-child(6),
td:nth-child(6),
th:nth-child(7),
td:nth-child(7) {
    width: 10%;
}

th:nth-child(8),
td:nth-child(8),
th:nth-child(9),
td:nth-child(9) {
    width: 15%;
}

.btn {
    padding: 5px 10px;
    margin: 0 2px;
    /* Reduces spacing between buttons */
}

.btn-group {
    display: flex;
    justify-content: center;
    gap: 10px;
    /* Adds small spacing between buttons */
}

.table-hover tbody tr:hover {
    background-color: #f5f5f5;
}

* {
    padding: 0;
    margin: 0;
    font-family: monospace;
    font-size: large;
}
</style>
