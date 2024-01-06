<template>
    <div class="cart-page">
        <h1 v-if="price === 0" class="bold">No Items!! Go Shop Now!!</h1>
        <h1 v-else class="header"><b>Cart</b></h1>
        <div class="product-cards-container" v-if="price !== 0">
            <div class="product-card" v-for="(order, index) in orders" :key="order.id"
                :class="index % 2 === 0 ? 'even-row' : 'odd-row'">
                <div class="product-info">
                    <div class="product-name">{{ order.product.name }}</div>
                    <div class="product-price">${{ order.product_price }}</div>
                </div>
                <div class="product-actions">
                    <input v-if="order.product.unit === 'piece'" type="number" v-model="order.quantity"
                        @input="updateSubtotal(order)" min="1" :max="order.product.quantity" class="quantity-input" />
                    <input v-else type="number" step="0.01" v-model="order.quantity" @input="updateSubtotal(order)" min="1"
                        :max="order.product.quantity" class="quantity-input"/>
                    <div class="subtotal">${{ order.subtotal.toFixed(2) }}</div>
                    <button class="update-button" @click="confirmEditOrder(order.id)">Update</button>
                    <button class="remove-button" @click="confirmRemoveOrder(order.id)">Remove</button>
                </div>
            </div>
            <div class="total-row">
                <div class="total-text"><b>Total:</b></div>
                <div class="total-price">${{ total_price.toFixed(2) }}</div>
                <button class="button_color buy-all-button" @click="confirmBuyAllOrders">Buy All</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            orders: [],
            total_price: 0,
            price:0,
            user_id: JSON.parse(localStorage.getItem('user')).user_id,
        };
    },
    created() {
        this.fetchCartData();
    },
    methods: {
        fetchCartData() {
            axios
                .get(`/api/${this.user_id}/order?status=NC`)
                .then((response) => {
                    this.orders = response.data.orders;
                    this.total_price = response.data.total_price;
                    this.price = response.data.total_price;
                })
                .catch((error) => {
                    console.error('Error fetching cart data:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },
        updateSubtotal(order) {
            order.subtotal = order.quantity * order.product_price;
            this.calculateTotalPrice();
        },
        confirmEditOrder(orderId) {
            if (confirm('Are you sure you want to Edit this item Quantity from your cart?')) {
                this.updateOrder(orderId);
            }
        },
        updateOrder(orderId) {
            const order = this.orders.find((order) => order.id === orderId);
            if (order) {
                axios
                    .post(`/api/customer/${this.user_id}/cart`, {
                        update: orderId,
                        quantity: order.quantity,
                    })
                    .then(() => {
                        console.log('Order updated successfully');
                        this.$toast.success('Item Updated', {
                            position: 'top-right',
                            duration: 5000,
                        });
                        setTimeout(location.reload.bind(location), 600);
                        
                    })
                    .catch((error) => {
                        console.error('Error updating order:', error);
                        this.$toast.error(error.response.data.message, {
                            position: 'top-right',
                            duration: 5000,
                        });
                    });
            }
        },
        confirmRemoveOrder(orderId) {
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                this.removeOrder(orderId);
            }
        },
        removeOrder(orderId) {
            this.orders = this.orders.filter((order) => order.id !== orderId);
            axios
                .post(`/api/customer/${this.user_id}/cart`, {
                    remove: orderId,
                })
                .then(() => {
                    console.log('Order removed successfully');
                    this.$toast.success('Item Removed', {
                        position: 'top-right',
                        duration: 5000,
                    });
                    setTimeout(location.reload.bind(location), 600);
                    this.calculateTotalPrice();
                })
                .catch((error) => {
                    console.error('Error removing order:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },
        confirmBuyAllOrders() {
            if (confirm('Are you sure you want to purchase all items in your cart?')) {
                this.buyAllOrders();
            }
        },
        buyAllOrders() {
            axios
                .post(`/api/customer/${this.user_id}/cart`, {
                    buyall: true,
                })
                .then(() => {
                    console.log('All orders purchased successfully');
                    this.orders = []; 
                    this.total_price = 0;
                    this.price=0;
                    this.$toast.success('All orders purchased successfully', {
                        position: 'top-right',
                        duration: 5000,
                    });
                    
                })
                .catch((error) => {
                    console.error('Error buying all orders:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },
        calculateTotalPrice() {
            this.total_price = this.orders.reduce((sum, order) => sum + order.subtotal, 0);
        },
    },
};
</script>

<style scoped>
.product-cards-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
    margin: 20px auto;
}

.product-card {
    margin: 10px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-card.even-row {
    background-color: lightblue;
}

.product-card.odd-row {
    background-color: peachpuff;
}

.product-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.product-name {
    font-size: 18px;
    font-weight: bold;
}

.product-price {
    font-size: 16px;
    color: #555;
}

.product-actions {
    display: flex;
    align-items: center;
    margin-left: 10px;
    margin-right: 10px;
}

.quantity-input {
    flex: 1;
    padding: 2px 5px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 50px;
    margin-right: 10px;
}

.subtotal {
    font-size: 16px;
    font-weight: bold;
    color: #555;
    margin: 10px;
}

.update-button,
.remove-button {
    padding: 8px 16px;
    background-color: rgb(84, 168, 246);
    color: white;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 14px;
    text-transform: uppercase;
    margin: 10px;
}

.remove-button {
    background-color: rgb(255, 87, 87);
}

.total-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #ddd;
}

.total-text {
    font-size: 16px;
    font-weight: bold;
}

.total-price {
    font-size: 16px;
    font-weight: bold;
    color: #555;
    padding-left: 10px;
    
}

.buy-all-button {
    background-color: rgb(7, 20, 208);
    padding: 6px 10px;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 12px;
    text-transform: uppercase;
    float: right;
    margin-left: 10px;
}

.bold {
    font-size: xx-large;
}

.cart-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    top: 50%;
    background-color: rgb(245, 245, 220);
}</style>
