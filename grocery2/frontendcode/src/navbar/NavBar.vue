<template>
    <nav class="navbar" v-if="showRegularNavbar" >
        <div class="container">
            <div class="navbar-menu">
                <div class="navbar-end">
                    <router-link to="/" class="navbar-item">Home</router-link>
                    <router-link v-if="isAuthenticated" to="/shop" class="navbar-item">Shop</router-link>
                    <router-link v-if="isAuthenticated" to="/cart" class="navbar-item">Cart</router-link>
                    <router-link v-if="isAuthenticated" to="/search" class="navbar-item">Search</router-link>
                    <router-link v-if="isAuthenticated" to="/profile" class="navbar-item">Profile</router-link>
                    <router-link v-if="!isAuthenticated" to="/login" class="navbar-item">Login</router-link>
                    <router-link v-if="!isAuthenticated" to="/signup" class="navbar-item">Sign Up</router-link>
                    <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                </div>
            </div>
        </div>
    </nav>
    <nav class="navbar" v-else-if="showStoreManagerNavbar" >
            <div class="container">
                <div class="navbar-menu">
                    <div class="navbar-end">
                        <router-link v-if="isAuthenticated" to="/store_dashboard" class="navbar-item">Dashboard</router-link>
                        <router-link v-if="isAuthenticated" to="/product_management" class="navbar-item">Manage Product</router-link>
                        <router-link v-if="!isAuthenticated" to="/store_login" class="navbar-item">Login</router-link>
                        <router-link v-if="!isAuthenticated" to="/store_signup" class="navbar-item">Sign Up</router-link>
                        <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                    </div>
                </div>
            </div>
    </nav>
    <nav class="navbar" v-else-if="showAdminNavbar" >
                <div class="container">
                    <div class="navbar-menu">
                        <div class="navbar-end">
                            <router-link v-if="isAuthenticated" to="/admin_dashboard" class="navbar-item">Admin Dashboard</router-link>
                            <router-link v-if="isAuthenticated" to="/category_management" class="navbar-item">Category Management</router-link>
                            <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                        </div>
                    </div>
                </div>
    </nav>
</template>

<script>
import { mapState } from 'vuex';
export default {
    name: "NavBar",
    computed: {
        ...mapState(['isAuthenticated','showRegularNavbar', 'showStoreManagerNavbar','showAdminNavbar']),
    },
    methods: {
        logout() {
            const accessToken = this.$store.state.token;
            this.$axios.post("/logout", null, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            })
                .then(() => {
                    this.$store.commit('setAuthenticated', false);
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('user');

                    if (this.showStoreManagerNavbar) {
                        this.$router.push("/store_login");
                    } else if (this.showAdminNavbar) {
                        this.$router.push("/admin_login");
                    }
                    else {
                        this.$router.push("/login");
                    }
                })
                .catch(error => {
                    console.error('Logout failed:', error);
                });
        },
    },
    
};
</script>

<style>
.navbar {
    background-color: transparent;
    opacity: 0.9;
    border: 0;
    margin: 0 0 20px 0;
    padding: 0;
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}

.navbar-menu {
    display: flex;
    justify-content: flex-end;
}

.navbar-item {
    color: black;
    font-family: Comic Sans MS, cursive;
    text-decoration: none;
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
}

.navbar-item:hover {
    transform: scale(2.0);
    background-color: #cdd6d6;
}
</style>
