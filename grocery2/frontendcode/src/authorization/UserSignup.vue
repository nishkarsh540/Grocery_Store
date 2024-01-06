<template>
    <div class="signup-container">
        <div class="signup-form">
            <h2>Sign Up</h2>
            <form @submit.prevent="signup">
                <label for="name">Name</label>
                <input type="text" v-model="name" required>
                <label for="username">Username</label>
                <input type="text" v-model="username" required>
                <label for="email">Email</label>
                <input type="email" v-model="email" required>
                <div v-if="emailError" class="error-message">{{ emailError }}</div>
                <label for="password">Password</label>
                <input type="password" v-model="password" required>
                <label for="confirmPassword">Confirm Password</label>
                <input type="password" v-model="confirmPassword" required>
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
                email: this.email,
                password: this.password,
                confirmPassword: this.confirmPassword, 
            };
            this.$axios
                .post("/signup", formData)
                .then(() => {
                    this.$router.push("/login");
                    this.$toast.success('User Created', {
                        position: 'top-right',
                        duration: 5000,
                    });
                })
                .catch((error) => {
                    console.error(error.response.data.message);
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
.signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.signup-form {
    text-align: center;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 320px;
}

h2 {
    margin-bottom: 16px;
    font-size: 24px;
}

label {
    font-size: 14px;
    font-weight: bold;
    display: block;
    margin-bottom: 6px;
}

input[type="text"],
input[type="password"],input[type="email"] {
    width: 80%;
    padding: 10px;
    margin-bottom: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

button {
    background-color: #007bff;
    color: #ffffff;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>