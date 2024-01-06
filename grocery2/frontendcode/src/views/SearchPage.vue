<template>
    <div class="search-container">
        <h1><b>Product Search</b></h1>
        <form class="search-form" @submit.prevent="searchProducts">
            <input class="search-input" v-model="searchQuery" type="text" name="search_query" placeholder="Search Here">
            <button class="search-button" type="submit">Search</button>
        </form>

        <h1><b>Search Results</b></h1>
        <div v-if="products.length > 0">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Price/unit</th>
                        <th>Manufacture Date</th>
                        <th>Available</th>
                        <th>Quantity</th>
                        <th>Add to cart</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in products" :key="product.id">
                        <td style="vertical-align: middle;">{{ product.name }}</td>
                        <td style="vertical-align: middle;">{{ product.category}}</td>
                        <td style="vertical-align: middle;">${{ product.price }}/{{ product.unit }}</td>
                        <td style="vertical-align: middle;">{{ product.manufacture_date }}</td>
                        <td style="vertical-align: middle;">{{ product.quantity }}</td>
                        <td v-if="product.unit === 'piece'">
                            <template v-if="product.quantity > 0.0">
                                <input v-model="product.quantityToAdd" type="number" id="quantity" name="quantity" min="1"
                                    :max="product.quantity">
                            </template>
                            <template v-else>
                                <b>OUT OF STOCK</b>
                            </template>
                        </td>
                        <td v-else>
                            <template v-if="product.quantity > 0.0">
                                <input v-model="product.quantityToAdd" step="0.01" type="number" id="quantity"
                                    name="quantity" min="0" :max="product.quantity">
                            </template>
                            <template v-else>
                                OUT OF STOCK
                            </template>
                        </td>
                        <td><button class="addtocart" @click="addToCart(product)">Add to Cart</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No results found.</p>
    </div>
</template>

<script>

import axios from 'axios';
export default {
    data() {
        return {
            searchQuery: '',
            products: [],
            user_id: JSON.parse(localStorage.getItem('user')).user_id,
        };
    },
    methods: {
        searchProducts() {
            axios.post(`/api/customer/${this.user_id}/search`, { search_query: this.searchQuery })
                .then(response => {
                    this.products = response.data;
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                });
        },
        addToCart(product) {
            const cartItem = {
                product_id: product.id,
                quantity: product.quantityToAdd
            };

            const accessToken = localStorage.getItem('access_token');
            axios.post('/add_to_cart', [cartItem], {
                headers: {
                    Authorization: `Bearer ${accessToken}`, 
                },
            })
                .then(response => {
                    console.log(response.data.message);
                    this.$toast.success('Product added successfully to cart!', {
                        position: 'top-right',
                        duration: 3000,
                    });
                    setTimeout(location.reload.bind(location), 600);

                })
                .catch(error => {
                    console.error('Error adding product to cart:', error);
                });
        }
    },
};

</script>

<style scoped>
table {
            border-collapse: collapse;
            width: 80%;
        }

th,
td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.addtocart {
    padding: 10px 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    text-align: center;
    cursor: pointer;
    border-radius: 40px;
    width: 100%;
}
.header {
    font-size: larger;
    color: hsl(0, 0%, 7%);
}
.search-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: rgb(245, 245, 220); 
}
.search-form {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    border-radius: 50px;
    background-color: #f2f2f2;
}
.search-input {
    border: none;
    outline: none;
    padding: 8px;
    border-radius: 50px 0 0 50px;
}
.search-button {
    border: none;
    outline: none;
    padding: 8px 10px;
    border-radius: 0 50px 50px 0;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}
.search-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.search-form {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    border-radius: 50px;
    background-color: #f2f2f2;
}

.search-input {
    border: none;
    outline: none;
    padding: 8px;
    border-radius: 50px 0 0 50px;
}

.search-button {
    border: none;
    outline: none;
    padding: 8px 16px;
    border-radius: 0 50px 50px 0;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}
</style>