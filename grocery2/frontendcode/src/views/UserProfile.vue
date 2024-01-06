<template>
    <div class="main">
        <div class="profile">
            <h1 class="user_info">User Information</h1>
            <h1 class="name">Name: <b>{{ this.name }}</b></h1>
            <h1 class="username">Username: <b>{{ this.username }}</b></h1>
            <template v-if="count === 0">
                <h1 class="bold">
                    Your shopping journey starts here - explore a world of possibilities
                    and fill up your order.
                </h1>
            </template>
            <template v-else>
                <h1 class="header"><b>Your Orders</b></h1>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="order in orders" :key="order.id">
                            <td style="vertical-align: middle;"><b>{{ order.product.name }}</b></td>
                            <td style="vertical-align: middle;">{{ order.product_price }}</td>
                            <td style="vertical-align: middle;">{{ order.quantity }}</td>
                            <td style="vertical-align: middle;">${{ (order.quantity * order.product_price).toFixed(2) }}
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td><b>Total</b></td>
                            <td></td>
                            <td></td>
                            <td>${{ total_price.toFixed(2) }}</td>
                        </tr>
                    </tfoot>
                </table>
            </template>
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
        };
    },
    methods: {
        async getPurchasedOrders() {
            try {
                const response = await axios.get(`/api/${this.user_id}/order?status=Purchased`);

                this.orders = response.data.orders;
                this.total_price = response.data.total_price;
                this.count = this.orders.length;
            } catch (error) {
                console.error('Error fetching purchased orders:', error);
            }
        },
    },
    mounted() {
        this.getPurchasedOrders();
    },
};
</script>

<style scoped> 
.profile {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    height: 500px;
}

table {
    border-collapse: collapse;
    width: 100%;
    background-color: peachpuff;
}

th,
td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.button_color {
    background-color: rgb(7, 20, 208);
}

.header {
    font-size: larger;
    color: hsl(0, 0%, 7%);
    background-color:peachpuff;
}

.user_info {
    font-size: xx-large;
}

.bold {
    font-size: x-large;
}

.username,
.name {
    font-size: x-large;
}
</style>
