<template>
    <div class="signup-page">
        <div class="login-form">
            <h2>Admin Login</h2>
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="username">Admin_Username:</label>
                    <input type="text" v-model="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Admin_Password:</label>
                    <input type="password" v-model="password" required>
                </div>
                <div class="form-group">
                    <label for="secret_key">Admin_Secret_Key:</label>
                    <input type="text" v-model="secret_key" required>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
        <div class="admin-link">
                    <router-link to="/store_login" class="admin-button">Return Back </router-link>
        </div>
    </div>
</template>


<script>

export default {
    data() {
        return {
            username: "",
            password: "",
            secret_key: "",
        };
    },
    methods: {
        handleLogin() {
            const formData = {
                username: this.username,
                password: this.password,
                secret_key: this.secret_key,
            };

            this.$axios.post("/admin/login", formData)
                .then((response) => {
                    const accessToken = response.data.access_token;
                    localStorage.setItem("access_token", accessToken);
                    const user = response.data.user; 
                    localStorage.setItem("user", JSON.stringify(user));

                    this.$store.commit('setAuthenticated', true);
                    this.$router.push("/admin_dashboard");
                    this.$toast.success('Login Succesful', {
                        position: 'top-right',
                        duration: 5000,
                    }); 
                })
                .catch((error) => {
                    console.error(error);
                    this.$toast.success(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                    
                });
        },
    },
};
</script>

<style scoped>
.login-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #efefef;
    width: 400px;
    margin: 0 auto;
    margin-top: 50px;
}

.admin-link {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin-top: 20px;
}

.admin-link p {
    margin-bottom: 10px;
    font-size: 14px;
    color: #555;
}

.admin-button {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 50px;
    /* Make the button pill-shaped */
    background-color: #fff;
    color: #14c0eb;
    border: 2px solid #14c0eb;
    text-decoration: none;
    font-size: 16px;
    transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}

.admin-button:hover {
    background-color: #14c0eb;
    color: #fff;
    border-color: transparent;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.admin-button:active {
    background-color: #0c7b8c;
    border-color: transparent;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.admin-button:focus {
    outline: none;
}

.signup-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #caebf2;
    background-size: cover;
    background-position: center;
    flex-direction: column;
}

h2 {
    font-size: 24px;
    margin-bottom: 20px;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.form-group {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    width: 100%;
}

label {
    font-weight: bold;
    margin-right: 10px;
    flex: 1;
    text-align: right;
}

input {
    flex: 2;
}

label {
    font-weight: bold;
    margin-right: 10px;
    margin-bottom: 10px;
}

input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
    max-width: 300px;
}

button {
    background-color: #14c0eb;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s ease;
    margin-top: 20px;
}

button:hover {
    background-color: #0b8fa2;
}

button:active {
    background-color: #0c7b8c;
}

button:focus {
    outline: none;
}</style>