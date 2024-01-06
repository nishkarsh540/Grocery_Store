<template>
    <div class="main">
    <div class="container">
        <div class="manage_cart">
            <h1>Create Category</h1>
            <form @submit.prevent="createCategory">
                <input style="border: none;
                    border-radius: 20px;
                    padding: 8px 20px;
                    font-weight: bold;
                    border-style:solid" class="create_input" type="text" v-model="newCategoryName" placeholder="Enter category name"
                    required/>
                <button type="submit">Create</button>
            </form>

            <h1>Existing Categories</h1>
            <table>
                <ul v-if="categories.length > 0">
                    <li v-for="category in categories" :key="category.id">
                        <span class="category-name">{{ category.name }}</span>
                        <button @click="editCategory(category)">Edit</button>
                        <button style="background-color: #dc3545;" @click="showConfirmation(category.id)">Remove</button>
                    </li>
                </ul>
                <p v-else>No Categories Found!!</p>
            </table>
        </div>
        <div class="manager">
            <h1>Manager Response</h1>
            <button class="toggle" @click="toggleManagerResponse">Manager Response  ↓</button>
            <div v-if="showManagerResponse">
                <p v-if="tasks.length === 0">No Requests</p>
                <table v-else>
                    <thead>
                        <tr>
                            <th>Task</th>
                            <th>Category</th>
                            <th>Modification</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="task in tasks" :key="task.id">
                            <td>{{ task.options }}</td>
                            <td>{{ task.category }}</td>
                            <td>{{ task.modification }}</td>
                            <td>
                                <button @click="confirmApproval(task)">Approve</button>
                                <button  style="background-color: #dc3545;" @click="confirmRejection(task)" >Reject</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div v-if="showConfirmationModal" class="confirmation-modal">
            <h2>Confirmation</h2>
            <p>Are you sure you want to remove this category?</p>
            <div class="modal-buttons">
                <button style="background-color: lightblue;" @click="removeCategory(categoryId)">Confirm</button>
                <button class="remove-button" @click="cancelConfirmation">Cancel</button>
            </div>
        </div>
        <div v-if="showEditModal" class="edit-modal">
            <h2>Edit Category</h2>
            <form @submit.prevent="submitEditedCategory">
                <input style="border: none;
                    border-radius: 20px;
                    padding: 8px 20px;
                    font-weight: bold;
                    border-style:solid" type="text" v-model="editCategoryName" required />
                <div class="modal-buttons">
                    <button style="background-color: rgb(237, 180, 131);" type="submit">Save</button>
                    <button style="border: none;
                    border-radius: 20px;
                    padding: 8px 20px;
                    color: #fff;
                    cursor: pointer;
                    font-weight: bold;" class="remove-button" @click="cancelEditCategory">Cancel</button>
                </div>
            </form>
        </div>
        <div v-if="showConfirmationModal || showEditModal" class="v-modal"></div>
    </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            newCategoryName: '',
            categories: [],
            showManagerResponse: false,
            tasks: [],
            showConfirmationModal: false,
            showEditModal: false,
            categoryId: null,
            editCategoryName: '',
            editingCategoryId: null,
        };
    },
    methods: {
        toggleManagerResponse() {
            this.showManagerResponse = !this.showManagerResponse;
        },
        confirmApproval(task) {
            if (task.options === 'create') {
                this.newCategoryName = task.modification;
                setTimeout(location.reload.bind(location), 600);
                this.createCategory();
                this.confirmRejection(task);
            } else if (task.options === 'delete' ) {
                this.removeCategory(task.category);
                this.confirmRejection(task);
                setTimeout(location.reload.bind(location), 600);
            }
            else{
                this.editCategoryName = task.modification;
                this.editingCategoryId = task.category;
                this.submitEditedCategory();
                this.confirmRejection(task);
                setTimeout(location.reload.bind(location), 600);
            }
        },
        confirmRejection(task) {
            const newtask = {
                name: task.id,
            };
            const accessToken = localStorage.getItem('access_token');
            axios
                .delete('/api/admin/tasks', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                    data: newtask,
                })
                .then(() => {
                    setTimeout(location.reload.bind(location), 600);
                })
                .catch((error) => {
                    console.error('Error fetching tasks:', error);
                });
        },
        fetchTasks() {
            
            const accessToken = localStorage.getItem('access_token');
            axios
                .get('/api/admin/tasks', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.tasks = response.data.tasks;
                })
                .catch((error) => {
                    console.error('Error fetching tasks:', error);
                });
        },
        createCategory() {
            const newCategory = {
                name: this.newCategoryName,
            };

            const accessToken = localStorage.getItem('access_token');
            axios
                .post('/api/admin/categories', newCategory, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.categories.push(response.data.category);
                    this.newCategoryName = '';
                    this.$toast.success('Category Created Successfully', {
                        position: 'top-right',
                        duration: 5000, 
                    });
                })
                .catch((error) => {
                    console.error('Error creating category:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },
        showConfirmation(categoryId) {
            this.showConfirmationModal = true;
            this.categoryId = categoryId;
        },
        removeCategory(categoryId) {
            const accessToken = localStorage.getItem('access_token');
            axios
                .delete('/api/admin/categories', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                    data: {
                        id: categoryId,
                    },
                })
                .then(() => {
                    this.categories = this.categories.filter(
                        (category) => category.id !== categoryId
                    );
                    this.showConfirmationModal = false;
                    this.$toast.success('Category Removed Successfully', {
                        position: 'top-right',
                        duration: 5000, // Duration in milliseconds (5 seconds in this case)
                    });
                })
                .catch((error) => {
                    console.error('Error removing category:', error);
                    this.showConfirmationModal = false;
                    this.$toast.error(error, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
        fetchCategories() {

            const accessToken = localStorage.getItem('access_token');
            axios
                .get('/api/admin/categories', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.categories = response.data.categories;
                })
                .catch((error) => {
                    console.error('Error fetching categories:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
        editCategory(category) {
            this.editCategoryName = category.name;
            this.editingCategoryId = category.id;
            this.showEditModal = true;
        },
        submitEditedCategory() {
            const editedCategory = {
                id: this.editingCategoryId,
                name: this.editCategoryName,
            };

            const accessToken = localStorage.getItem('access_token');
            axios
                .put('/api/admin/categories', editedCategory, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.categories = this.categories.map((category) =>
                        category.id === this.editingCategoryId
                            ? { ...category, name: response.data.category.name } 
                            : category
                    );
                    this.editCategoryName = '';
                    this.editingCategoryId = null;
                    this.showEditModal = false;
                    this.$toast.success('Category Edited Successfully', {
                        position: 'top-right',
                        duration: 5000,
                    });
                })
                .catch((error) => {
                    console.error('Error editing category:', error);
                    this.showEditModal = false;
                    this.$toast.error(error, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
        cancelEditCategory() {
            this.editCategoryName = '';
            this.editingCategoryId = null;
            this.showEditModal = false;
        },
        cancelConfirmation() {
            this.showConfirmationModal = false;
        },
    },
    created() {
        this.fetchCategories();
        this.fetchTasks();
    },
};
</script>

<style scoped>
.main {
    background-color: #caebf2;
}

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
}

.manage_cart,
.manager {
    margin: 20px;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    width: 80%;
    max-width: 600px;
    background-color: #efefef;
}

.manage_cart h1,
.manager h1 {
    text-align: center;
}

.toggle {
    position: relative;
    left: 30%;
    transform: translateX(-50%);

    top: 50%;
    transform: translateY(-50%);
}

.manage_cart form,
.manager button {
    display: flex;
    justify-content: center;
}

.manage_cart button,
.manager button,
.confirmation-modal button,
.edit-modal button[type="submit"] {
    border: none;
    border-radius: 20px;
    padding: 8px 20px;
    color: #fff;
    cursor: pointer;
    font-weight: bold;
}

.edit-modal {
    width: 300px;
    background-color: #fff;
    padding: 20px;
    border-radius: 20px;
    z-index: 9999;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.edit-modal h2 {
    text-align: center;
    margin-bottom: 20px;
}

.edit-modal form {
    display: flex;
    flex-direction: column;
}

.edit-modal label {
    font-weight: bold;
    margin-bottom: 5px;
}

.edit-modal input {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 8px;
    margin-bottom: 15px;
}

.edit-modal .modal-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 15px;
}

.manage_cart button,
.manager button,
.confirmation-modal button,
.edit-modal button[type="submit"] {
    border: none;
    border-radius: 20px;
    padding: 8px 20px;
    color: #fff;
    cursor: pointer;
    font-weight: bold;
}

.manage_cart button {
    background-color: #28a745;
    margin-left: 10px;
}

.manager button {
    background-color: #28a745;
    margin: 5px;
}

.v-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9998;
    display: flex;
    justify-content: center;
    align-items: center;
}

.manage_cart button {
    background-color: #28a745;
    margin-left: 10px;
}

.manager button {
    background-color: #28a745;
    margin: 5px;
}

.confirmation-modal,
.edit-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    padding: 20px;
    border-radius: 20px;
    z-index: 9999;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.v-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9998;
    display: flex;
    justify-content: center;
    align-items: center;
}

.remove-button {
    background-color: #dc3545;
    margin-left: 10px;
}

.reject-button {
    background-color: #dc3545;
}

ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

ul li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
}

.category-name {
    flex: 1;
    margin-right: 10px;
}

.category-buttons {
    display: flex;
}</style>
