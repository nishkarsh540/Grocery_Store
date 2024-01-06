<template>
    <div class="signup-page">
        <div class="signup-form">
            <h2>Store SignUp</h2>
            <form @submit.prevent="signup">
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" v-model="name" required>
                </div>
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" v-model="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" v-model="password" required>
                </div>
                <div class="form-group">
                    <label for="confirmPassword">Confirm Password:</label>
                    <input type="password" v-model="confirmPassword" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" v-model="email" required>
                    <div v-if="emailError" class="error-message">{{ emailError }}</div>
                </div>
                <div class="form-group">
                    <label for="secret_key">Secret Key:</label>
                    <input type="text" v-model="secret_key" required>
                </div>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            name: "",
            username: "",
            password: "",
            confirmPassword: "",
            secret_key:"",
            email: "",
            emailError: "",
        };
    },
    methods: {
        checkEmailFormat(email) {
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            return emailRegex.test(email);
        },
        signup() {
            
            if (this.password !== this.confirmPassword) {
                console.error("Passwords do not match.");
                return;
            }
            if (!this.checkEmailFormat(this.email)) {
                this.emailError = "Invalid email format";
                return;
            }


            const formData = {
                name: this.name,
                username: this.username,
                password: this.password,
                email: this.email,
                confirmPassword: this.confirmPassword,
                secret_key: this.secret_key,
            };
            this.$axios
                .post("/store_manager/signup", formData)
                .then(() => {
                    this.$router.push("/store_login");
                    this.$toast.success('SignUp Succesful !!', {
                        position: 'top-right',
                        duration: 5000,
                    });
                })
                .catch((error) => {
                    console.error(error.response.data.message);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
    },
};
</script>


<style scoped>
.signup-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #f8eee7;
    background-size: cover;
    background-position: center;
}

.signup-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #f4decb;
    width: 400px;
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
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 15px;
    width: 100%;
}

label {
    font-weight: bold;
    margin-right: 10px;
    flex: 1;
}

input {
    flex: 2;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
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
}

button:hover {
    background-color: #0b8fa2;
}

button:active {
    background-color: #0c7b8c;
}

button:focus {
    outline: none;
}

.error-message {
    color: red;
    margin-top: 5px;
}
</style>