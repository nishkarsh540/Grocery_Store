import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import UserLogin from '../authorization/UserLogin.vue';
import UserSignup from '../authorization/UserSignup.vue';
import StoreLogin from '../authorization/StoreLogin.vue';
import StoreSignup from '../authorization/StoreSignup.vue';
import AdminLogin from '../authorization/AdminLogin.vue';
import ShopPage from '../components/ShopPage.vue';
import CustomerCart from '../views/CustomerCart.vue';
import SearchPage from '../views/SearchPage.vue';
import UserProfile from '../views/UserProfile.vue';
import ProductManagement from '../views/ProductManagement.vue';
import StoreDashboard from '../views/StoreDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import CategoryManagement from '../views/CategoryManagement.vue';
import store from '../store';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
  },
  {
    path: '/store_login',
    name: 'StoreLogin',
    component: StoreLogin,
    meta: {
      showStoreManagerNavbar: true,
    },
  },
  {
    path: '/admin_login',
    name: 'AdminLogin',
    component: AdminLogin,
    meta: {
      showAdminNavbar: true,
    },
  },
  {
    path: '/category_management',
    name: 'CategoryManagement',
    component: CategoryManagement,
    meta: {
      showAdminNavbar: true,
    },
  },
  {
    path: '/store_signup',
    name: 'StoreSignup',
    component: StoreSignup,
    meta: {
      showStoreManagerNavbar: true,
    },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: UserSignup,
  },
  {
    path: '/shop',
    name: 'Shop',
    component: ShopPage,
  },
  {
    path: '/cart',
    name: 'CustomerCart',
    component: CustomerCart,
  },
  {
    path: '/search',
    name: 'SearchPage',
    component: SearchPage,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile,
  },
  {
    path: '/product_management',
    name: 'ProductManagement',
    component: ProductManagement,
    meta: {
      showStoreManagerNavbar: true,
    },
  },
  
  {
    path: '/store_dashboard',
    name: 'StoreDashboard',
    component: StoreDashboard,
    meta: {
      showStoreManagerNavbar: true,
    },
  },
  {
    path: '/admin_dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      showAdminNavbar: true,
    },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  if (to.meta.showStoreManagerNavbar) {
    store.commit('setShowRegularNavbar', false);
    store.commit('setShowStoreManagerNavbar', true);
    store.commit('setShowAdminNavbar', false);
  } else if (to.meta.showAdminNavbar) {
      store.commit('setShowRegularNavbar', false);
      store.commit('setShowStoreManagerNavbar', false);
      store.commit('setShowAdminNavbar', true);
      
  } else  {
    store.commit('setShowRegularNavbar', true);
    store.commit('setShowStoreManagerNavbar', false);
    store.commit('setAdminNavbar', false);
  }
  next();
});
export default router;
