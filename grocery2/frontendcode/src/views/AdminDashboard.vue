<template>
    <div class="profile">
        <div class="user-info">
            <h1 class="name">Name: <b>{{ this.name }}</b></h1>
            <h1 class="username">Username: <b>{{ this.username }}</b></h1>
        </div>
        <div class="manager-managing">
            <h2>MANAGER MANAGING</h2>
            <table v-if="pendingManagers.length > 0">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="manager in pendingManagers" :key="manager.id">
                        <td>{{ manager.name }}</td>
                        <td>{{ manager.username }}</td>
                        <td>{{ manager.email }}</td>
                        <td>
                        <button class="manager_button" @click="confirmApproval(manager)">Approve</button>
                        <button style="background-color: lightcoral;" class="manager_button" @click="confirmRejection(manager)">Reject</button>

                        </td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No new managers</p>
        </div>
        <div v-if="showConfirmationModal" class="modal">
        <div class="modal-content">
            <h2>{{ confirmationTitle }}</h2>
            <p>{{ confirmationMessage }}</p>
            <div>
            <button class="button-submit" @click="handleConfirmation(true)">Confirm</button>
            <button  class="button-cancel" @click="handleConfirmation(false)">Cancel</button>
            </div>
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
            pendingManagers: [],
            showConfirmationModal: false,
            confirmationTitle: '',
            pendingManagerToHandle: null,
        };
    },
    created() {
        this.fetchPendingManagers();
        console.log(this.user_id);
    },
    methods: {
        fetchPendingManagers() {
            const accessToken = localStorage.getItem('access_token');
            axios
                .get('/api/admin/pending_managers', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.pendingManagers = response.data; 
                })
                .catch((error) => {
                    console.error('Error fetching pending managers:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });

                });
        },
        handleManagerAction(managerId, status) {
            const accessToken = localStorage.getItem('access_token');
            const data = {
                manager_id: managerId,
                status: status,
            };

            axios
                .post('/api/admin/pending_managers', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    console.log(response.data);
                    this.fetchPendingManagers(); 
                })
                .catch((error) => {
                    console.error('Error processing manager action:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
        confirmApproval(manager) {
            this.pendingManagerToHandle = manager;
            this.confirmationTitle = 'Approve Manager';
            this.confirmationMessage = `Approve ${manager.name}'s manager request?`;
            this.showConfirmationModal = true;
        },

        confirmRejection(manager) {
            this.pendingManagerToHandle = manager;
            this.confirmationTitle = 'Reject Manager';
            this.confirmationMessage = `Delete ${manager.name}'s account?`;
            this.showConfirmationModal = true;
        },

        handleConfirmation(isConfirmed) {
            if (isConfirmed) {
                if (this.confirmationTitle === 'Approve Manager') {
                    this.handleManagerAction(this.pendingManagerToHandle.id, 'approve');
                } else if (this.confirmationTitle === 'Reject Manager') {
                    this.handleManagerAction(this.pendingManagerToHandle.id, 'reject');
                }
            }

            this.showConfirmationModal = false;
            this.confirmationTitle = '';
            this.confirmationMessage = '';
            this.pendingManagerToHandle = null;
        },
    },
};
</script>

<style scoped>
body {
    margin: 0;
    padding: 0;
}
.manager_button{
    border: none;
    border-radius: 20px;
    padding: 8px 20px;
    color: whitesmoke;
    cursor: pointer;
    font-weight: bold;
    background-color: rgb(234, 162, 85);
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
    background-color: #caebf2;
}

.button-container {
    margin-bottom: 20px;
}

.button-container button:hover .cloud-icon::before {
    opacity: 1;
    transform: translateX(-50%) translateY(-5px);
}

/* Additional styles to position the buttons */
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
}
</style>
