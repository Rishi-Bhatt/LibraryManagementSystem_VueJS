import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LibrarianLogin from '../views/LibrarianLogin.vue'
import UserLogin from '../views/UserLogin.vue'
import RegisterView from '../views/RegisterView.vue'
import UserDashboard from '../views/UserDashboard.vue'
import LibrarianDashboard from '../views/LibrarianDashboard.vue'
import AddSection from '../views/AddSection.vue'
import UpdateSection from '../views/UpdateSection.vue'
import BooksPortal from '../views/BooksPortal.vue'
import AddBook from '../views/AddBook.vue'
import UpdateBook from '../views/UpdateBook.vue'
import ApproveRequest from '../views/ApproveRequest.vue'
import LibrarianIssuedBooksView from '../views/LibrarianIssuedBooksView.vue'
import UserRequests from '../views/UserRequests.vue'
import UserIssuedBooksView from '../views/UserIssuedBooksView.vue'
import PaymentGateway from '../views/PaymentGateway.vue'

import About from '../views/About.vue'
import Feedback from '../views/Feedback.vue'



const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/LibrarianLogin',
    name: 'librarianlogin',
    component: LibrarianLogin
  },
  {
    path: '/UserLogin',
    name: 'userlogin',
    component: UserLogin
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/UserDashboard',
    name: 'userdashboard',
    component: UserDashboard
  },
  {
    path: '/LibrarianDashboard',
    name: 'librariandashboard',
    component: LibrarianDashboard
  },
  {
    path: '/AddSection',
    name: 'addsection',
    component: AddSection
  },
  {
    path: '/updatesection/:section_id',
    name: 'updatesection',
    component: UpdateSection,
    props: true
  },
  {
    path: '/booksportal/:section_name/:section_id',
    name: 'booksportal',
    component: BooksPortal,
    props: true
  },
  {
    path: '/addbook/:section_name/:section_id',
    name: 'addbook',
    component: AddBook,
    props: true
  },
  {
    path: '/updatebook/:section_name/:section_id/:book_id',
    name: 'updatebook',
    component: UpdateBook,
    props: true
  },
  {
    path: '/ApproveRequest',
    name: 'approverequest',
    component: ApproveRequest
  },
  {
    path: '/LibrarianIssuedBooksView',
    name: 'librarianissuedbooksview',
    component: LibrarianIssuedBooksView
  },
  {
    path: '/UserRequests',
    name: 'userrequests',
    component: UserRequests
  },
  {
    path: '/UserIssuedBooksView',
    name: 'userissuedbooksview',
    component: UserIssuedBooksView
  },
  {
    path: '/PaymentGateway',
    name: 'PaymentGateway',
    component: PaymentGateway
  },
  
  {
    path: '/about',
    name: 'about',
    component: About
  },
  {
    path: '/feedback',
    name: 'feedback',
    component: Feedback
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
