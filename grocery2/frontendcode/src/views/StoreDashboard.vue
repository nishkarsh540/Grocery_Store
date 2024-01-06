<template>
    <div class="profile">
        <div class="user-info">
            <h1 class="name">Name: <b>{{ this.name }}</b></h1>
            <h1 class="username">Username: <b>{{ this.username }}</b></h1>
        </div>
        <div class="button-container">
            <button class="button_color button-generate" @click="showPopup">Generate Request</button>
            <button class="button_color button-generate" @click="exportCSV">
                Download Report
            </button>
        </div>
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <h2>Select Option:</h2>
                <label>
                    <input type="radio" v-model="selectedOption" value="create" /> Create
                </label>
                <label>
                    <input type="radio" v-model="selectedOption" value="edit" /> Edit
                </label>
                <label>
                    <input type="radio" v-model="selectedOption" value="delete" /> Delete
                </label>
                <div v-if="selectedOption === 'create'">
                    <input type="text" v-model="newApp" placeholder="Enter new app name" />
                </div>
                <div v-else-if="selectedOption === 'edit'">
                    <select v-model="selectedCategory">
                        <option v-for="category in existingCategories" :key="category.id" :value="category.id">
                            {{ category.name }}
                        </option>
                    </select>
                    <input type="text" v-model="newApp" placeholder="Enter new app name" />
                </div>
                <div v-else-if="selectedOption === 'delete'">
                    <select v-model="selectedCategory">
                        <option v-for="category in existingCategories" :key="category.id" :value="category.id">
                            {{ category.name }}
                        </option>
                    </select>
                </div>
                <button class="button_color button-submit" @click="submitRequest">Submit</button>
                <button class="button_color button-cancel" @click="closePopup">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            name: JSON.parse(localStorage.getItem('user')).name,
            username: JSON.parse(localStorage.getItem('user')).username,
            user_id: JSON.parse(localStorage.getItem('user')).user_id,
            orders: [],
            total_price: 0,
            count: 0,
            showModal: false,
            selectedOption: '',
            existingCategories: [],
            selectedCategory: null,
            newApp: '',
        };
    },
    created() {
        this.fetchDataFromBackend();
    },
    methods: {
        fetchDataFromBackend() {
            const accessToken = localStorage.getItem('access_token');
            axios
                .get(`/api/store-manager/${this.user_id}/product_management`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.existingCategories = response.data.categories;
                    console.log(this.existingCategories)
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
        exportCSV() {
            const accessToken = localStorage.getItem('access_token');
            const headers = {
                Authorization: `Bearer ${accessToken}`,
            };
            axios.post(`/export/${this.user_id}/report`, null, {
                headers: headers,
                responseType: 'blob',
            })
                .then(response => {
                    const downloadLink = document.createElement('a');
                    downloadLink.href = URL.createObjectURL(response.data);
                    downloadLink.download = 'product_report.csv';

                    document.body.appendChild(downloadLink);
                    downloadLink.click();

                    setTimeout(() => {
                        URL.revokeObjectURL(downloadLink.href);
                        document.body.removeChild(downloadLink);
                    }, 100);
                })
                .catch(error => {
                    console.error('Error exporting CSV:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },

        showPopup() {
            this.showModal = true;
        },
        closePopup() {
            this.showModal = false;
        },
        submitRequest() {
            const requestData = {
                option: this.selectedOption,
                category: this.selectedCategory,
                newApp: this.newApp,
                user_id: this.user_id,
            };

            if (!requestData.option) {
                this.$toast.error('Please select an option', {
                    position: 'top-right',
                    duration: 5000,
                });
                return;
            }
            if ((requestData.option === 'create' || requestData.option === 'edit') && !requestData.newApp) {
                this.$toast.error('Please enter the box', {
                    position: 'top-right',
                    duration: 5000,
                });
                return;
            }
            if ((requestData.option === 'edit' || requestData.option === 'delete') && !requestData.category) {
                this.$toast.error('Please select a category', {
                    position: 'top-right',
                    duration: 5000,
                });
                return;
            }
            const accessToken = localStorage.getItem('access_token');
            axios
                .post(`/api/store_manager/${this.user_id}/request`, requestData, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    console.log('Request submitted successfully:', response.data);
                    this.$toast.success('Request submitted successfully', {
                        position: 'top-right',
                        duration: 5000, 
                    });
                    this.selectedOption =  '';
                    this.selectedCategory = null;
                    this.newApp = null;
                    this.closePopup(); 
                })
                .catch((error) => {
                    console.error('Error submitting request:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                    this.closePopup();
                });
        },
    },
};
</script>

<style scoped>
body {
    margin: 0;
    padding: 0;
}

.profile {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background-color: rgb(245, 245, 220);
}

.button-container {
    margin-bottom: 20px;
}


.button-container button:hover .cloud-icon::before {
    opacity: 1;
    transform: translateX(-50%) translateY(-5px);
}

.button-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-end;
}

.button_color {
    padding: 6px 10px;
    background-color: transparent;
    color: #14c0eb;
    border: none;
    cursor: pointer;
}

.button-generate {
    padding: 6px 10px;
    color: #14c4eb;
    border: 1px solid #14d2eb;
    background-color: transparent;
    cursor: pointer;
}

.button-download {
    padding: 6px 10px;
    color: #eb141b;
    border: none;
    cursor: pointer;
}

.user-info {
    margin-bottom: 20px;
}

.modal {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    padding: 20px;
    background-color: #f0f8ff;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    max-width: 400px;
}

.modal-content h2 {
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.modal-content label {
    display: block;
    margin-bottom: 5px;
}

.modal-content input[type='radio'],
.modal-content select,
.modal-content input[type='text'] {
    margin-right: 5px;
}

.modal-content button {
    margin-top: 10px;
    padding: 8px 16px;
    color: white;
    border: none;
    cursor: pointer;
}

.button-submit {
    background-color: #14c0eb;
}

.button-cancel {
    background-color: #ccc;
}</style>
