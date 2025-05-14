<template>
<div class="userdashboard">

    <body>
        
        <nav class="py-2 bg-body-tertiary border-bottom">
            <div>
                <!-- class="container d-flex flex-wrap" -->
                <ul>
                    <li>
                        <router-link to="/about">
                            About
                        </router-link>
                    </li>
                    <li><a href="#">Contact</a></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li><a href="#">Pustakalay User Dashboard</a></li>

                    <li></li>

                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>

                    <li><a class="btn btn-logout px-3" @click="logout">Logout</a></li>
                </ul>

            </div>
        </nav>

        <header class="py-1 mb-0 me-lg-0 border-bottom">
            <div class="container d-flex flex-wrap">

                <router-link to="/UserRequests" class="d-flex align-items-center mb-0 mb-lg-0 me-lg-auto link-body-emphasis text-decoration-none">
                    <span class="fs-4">Requested Books</span>
                </router-link>

                <router-link to="/UserIssuedBooksView" class="d-flex align-items-center mb-0 mb-lg-0 me-lg-auto link-body-emphasis text-decoration-none">
                    <span class="fs-4">Issued books</span>
                </router-link>
                <!-- Search Bar -->
                <div class="search-bar ms-auto">
                    <input type="search" class="form-control" placeholder="Search Book/Section" aria-label="Search" v-model="searchQuery" @input="search">
                </div>
            </div>
        </header>

        <div class="b-example-divider"></div>
        <main>
            <!-- <table class="table table-warning table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Section</th>
                        <th>Book Name</th>
                        <th>Author</th>
                        <th colspan="2">Actions</th>
                    </tr>
                </thead>
                <tbody id="results">
                    <tr v-for="(section, index) in filteredSections" :key="section.section_id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ section.section_name }}</td>
                        <td colspan="5">
                            <table class="table table-bordered">
                                <tr v-if="section.ebooks.length > 0" v-for="book in section.ebooks" :key="book.book_id">
                                    <td>{{ book.book_name }}</td>
                                    <td>{{ book.book_author }}</td>
                                    <td colspan="2">
                                        <div class="btn-group">
                                            <a href="#" class="btn btn-outline-success btn-sm" type="submit" @click="requestBook(book.book_id)">Request</a>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-if="section.ebooks.length === 0">
                                    <td colspan="6">No Books available in this section</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table> -->
            <table class="table table-warning table-hover">
    <thead>
        <tr>
            <th>ID</th>
            <th>Section</th>
            <th>Book Name</th>
            <th>Author</th>
            <th>Price</th>
            <th colspan="2">Actions</th>
        </tr>
    </thead>
    <tbody id="results">
        <tr v-for="(section, index) in filteredSections" :key="section.section_id">
            <td>{{ index + 1 }}</td>
            <td>{{ section.section_name }}</td>
            <td colspan="4">
                <table class="table table-bordered">
                    <tr v-if="section.ebooks.length > 0" v-for="book in section.ebooks" :key="book.book_id">
                        <td>{{ book.book_name }}</td>
                        <td>{{ book.book_author }}</td>
                        <td>{{ book.DownloadPrice }}</td>
                        <td>
                            <div class="btn-group">
                                <a href="#" class="btn btn-outline-success btn-sm" type="submit" @click="requestBook(book.book_id)">Request</a>
                            </div>
                        </td>
                    </tr>
                    <tr v-if="section.ebooks.length === 0">
                        <td colspan="6">No Books available in this section</td>
                    </tr>
                </table>
            </td>
        </tr>
    </tbody>
</table>

        </main>
    </body>
</div>
</template>
<script>
import axios from 'axios';
import {
    DateTime
} from 'luxon';
import Swal from 'sweetalert2';

export default {
    name: 'userdashboard',
    data() {
        return {
            token: null,
            esection: [],
            searchQuery: ''
        };
    },
    computed: {
        filteredSections() {
            const query = this.searchQuery.toLowerCase();
            return this.esection.filter(section => {
                return section.section_name.toLowerCase().includes(query) ||
                    section.ebooks.some(book =>
                        book.book_name.toLowerCase().includes(query) ||
                        book.book_author.toLowerCase().includes(query)
                    );
            });
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        if (!this.token) {
            Swal.fire({
                icon: 'error',
                title: 'Login Required',
                text: 'Please login again.',
                confirmButtonText: 'OK'
            }).then(() => {
                this.$router.push('/UserLogin');
            });
        } else {
            this.fetchSectionsWithBooks();
        }
    },
    methods: {
        formatDate(dateStr) {
            if (!dateStr) return 'None';
            return DateTime.fromISO(dateStr).toFormat('dd/MM/yyyy HH:mm:ss');
        },
        async fetchSectionsWithBooks() {
            try {
                const sectionResponse = await axios.get('http://localhost:5000/api/esection', {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    }
                });
                if (sectionResponse.status === 200) {
                    const sections = sectionResponse.data.data;
                    for (let section of sections) {
                        const booksResponse = await axios.get(`http://localhost:5000/api/ebooks?section_id=${section.section_id}`, {
                            headers: {
                                Authorization: `Bearer ${this.token}`
                            }
                        });
                        section.ebooks = booksResponse.status === 200 ? booksResponse.data.EBdata.filter(book => book.sectionid === section.section_id) : [];
                    }
                    this.esection = sections;
                }
            } catch (error) {
                console.log(error);
            }
        },
        async requestBook(bookId) {
            try {
                const response = await axios.post('http://localhost:5000/api/request_book', {
                    user_id: localStorage.getItem('user_id'),
                    bookid: bookId
                }, {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    }
                });
                if (response.status === 201) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Book Requested',
                        text: 'Book requested successfully'
                    }).then(() => {
                        if (response.data.warning) {
                            Swal.fire({
                                icon: 'warning',
                                title: 'Warning',
                                text: response.data.warning
                            });
                        }
                        this.$router.push('/UserRequests');
                    });
                }
            } catch (error) {
                if (error.response) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.response.data.error
                    });
                } else if (error.request) {
                    console.log('Error request:', error.request);
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.message
                    });
                }
            }
        },
        logout() {
            localStorage.clear();
            this.$router.push('/');
        },
        search() {
            // You can trigger search functionality here if needed
        }
    }
}
</script>





<style scoped>
@import '../assets/static/UserDashboardNavbar.css';
@import url("https://getbootstrap.com/docs/5.3/examples/sign-in/sign-in.css");
@import url("https://cdn.jsdelivr.net/npm/@docsearch/css@3");
@import url("https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css");
@import url("https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css");

.outer-table,
.inner-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.outer-table th,
.outer-table td,
.inner-table th,
.inner-table td {
    border: 1px solid #ddd;
    padding: 8px;
}

.outer-table th,
.inner-table th {
    background-color: #f2f2f2;
    text-align: left;
}

/* .outer-table tr:hover,
.inner-table tr:hover {
  background-color: #f1f1f1;
} */

.outer-table th {
    padding-top: 12px;
    padding-bottom: 12px;
    background-color: #4caf50;
    color: white;
}

.inner-table th {
    padding-top: 8px;
    padding-bottom: 8px;
    background-color: #2196f3;
    color: white;
}

button {
    background-color: #c5293b;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
    text-align: center;
}

button:hover {
    background-color: #fa0511;
}

/* .table th,
.table td {
    text-align: center;
    vertical-align: middle;
}

.btn-group {
    display: flex;
    justify-content: center;
    gap: 5px;

} */

.top-navbar {
    /* background-color: #333; */
    background: #22438C;
    height: 40px;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
}

/* .navbar {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f8f9fa;
    padding: 0.5rem 1rem;
} */

.nav-left,
.nav-right {
    display: flex;
    align-items: center;
}

.nav-center {
    flex: 1;
    text-align: center;
}

.nav-item {
    margin-right: 1rem;
}

.nav-item:last-child {
    margin-right: 0;
}

.nav-item a {
    color: black;
    font-weight: bold;
    text-decoration: none;
}

.nav-item h6 {
    margin: 0;
}

.search-bar {
    background: #22438C;
    /* padding: 0.5rem 1rem; */
    border: 2px solid #f5f7fa;
    /* Change the color and width as needed */
    border-radius: 0.50rem;
    /* Optional: add border radius */

    color: #007bff;
    /* Text color */
    font-weight: bold;
    /* Optional: make text bold */

}

.search-bar:hover {
    color: #fff;
    /* Text color on hover */
    background: #112C66;
    border: 2px solid #f5f7fa;
    /* Change the color and width as needed */
    border-radius: 0.50rem;
}

.btn-logout {
    /* padding: 0.5rem; */
    background: #22438C;
    /* padding: 0.5rem 1rem; */
    border: 1px solid #f5f7fa;
    /* Change the color and width as needed */
    border-radius: 0.25rem;
    /* Optional: add border radius */

    color: #007bff;
    /* Text color */
    font-weight: bold;
    /* Optional: make text bold */

}

.btn-logout:hover {
    /* background-color: #007bff; Background color on hover */
    color: #fff;
    /* Text color on hover */
    background: #112C66;
    border: 1px solid #f5f7fa;
    /* Change the color and width as needed */
    border-radius: 0.25rem;
}

* {
    padding: 0;
    margin: 0;
    font-family: monospace;
}

ul {
    list-style: none;
    background: #22438C;
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 0;
    margin: 0;
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

/* @media (min-width: 768px) {
    .bd-placeholder-img-lg {
        font-size: 3.5rem;
    }
} */

.nav-scroller {
    position: relative;
    z-index: 2;
    height: 2.75rem;
    /* overflow-y: hidden; */
}

/* .nav-scroller .nav {
    display: flex;
    flex-wrap: nowrap;
    padding-bottom: 1rem;
    margin-top: -1px;
    overflow-x: auto;
    text-align: center;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
} */

.btn-bd-primary {
    --bd-violet-bg: #712cf9;
    --bd-violet-rgb: 112.520718, 44.062154, 249.437846;
    --bs-btn-font-weight: 600;
    --bs-btn-color: var(--bd-violet-bg);
    --bs-btn-bg: var(--bd-violet-bg);
    --bs-btn-border-color: var(--bd-violet-bg);
    --bs-btn-hover-color: var(--bd-violet-bg);
    --bs-btn-hover-bg: #6528e0;
    --bs-btn-hover-border-color: #6528e0;
    --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
    --bs-btn-active-color: var(--bs-btn-hover-color);
    --bs-btn-active-bg: #5a23c8;
    --bs-btn-active-border-color: #5a23c8;
}
</style>
