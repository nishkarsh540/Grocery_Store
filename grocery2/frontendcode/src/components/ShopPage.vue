<template>
    <div class="shop-page">
        <h1 class="header"><b>Product Catalog</b></h1>
        <div class="categories-container">
            <div v-for="cat in categories" :key="cat.id" class="category">
                <h2 class="header"><b>{{ cat.name }}</b></h2>
                <div class="product-grid">
                    <div v-for="product in cat.products" :key="product.id" class="product-card">
                        <div class="product-name">{{ product.name }}</div>
                        <div class="product-details">
                            <div>Expiry Date: {{ product.expiry_date }}</div>
                            <div>Manufacture Date: {{ product.manufacture_date }}</div>
                            <div>Available Quantity: {{ product.quantity }}</div>
                            <div>Price/unit: ${{ product.price }}/{{ product.unit }}</div>
                        </div>
                        <div class="product-actions">
                            <input type="number" v-model="product.quantityToAdd" :min="0" :max="product.quantity"
                                :step="product.unit === 'piece' ? 1 : 0.01" :disabled="product.quantity === 0"
                                class="quantity-input" />
                            <label class="checkbox-container">
                                <input type="checkbox" class="product-checkbox" v-model="product.selected"
                                    :disabled="product.quantity === 0" />
                                <span class="checkmark"></span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <button class="add-to-cart-button" @click="addToCart" :disabled="!hasSelectedProducts">Add To Cart</button>
    </div>
</template>


<script>
import axios from 'axios';
import store from '../store/index'; 

export default {
    data() {
        return {
            categories: [],
        };
    },
    created() {
        this.fetchCategories();
    },
    computed: {
        hasSelectedProducts() {
            return this.categories.some((category) =>
                category.products.some((product) => product.selected && product.quantityToAdd > 0)
            );
        },
    },
    methods: {
        fetchCategories() {
            axios
                .get('/categories')
                .then((response) => {
                    this.categories = response.data.map((category) => ({
                        ...category,
                        products: category.products.map((product) => ({
                            ...product,
                            selected: false,
                            quantityToAdd: 0,
                        })),
                    }));
                })
                .catch((error) => {
                    console.error('Error fetching categories:', error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },

        addToCart() {
            // Filter selected products
            const selectedProducts = this.categories
                .flatMap((category) =>
                    category.products.filter(
                        (product) => product.selected && product.quantityToAdd > 0 && product.quantityToAdd <= product.quantity
                    )
                )
                .map((product) => ({
                    product_id: product.id,
                    quantity: product.quantityToAdd,
                }));

            if (selectedProducts.length === 0) {
                alert('The entered quantity is  greater than available quantity.');
                return;
            }

            // Debug: Log selected products to the console
            console.log('Selected Products:', selectedProducts);

            // Send selected products to the backend
            const accessToken = localStorage.getItem('access_token');
            axios
                .post('/add_to_cart', selectedProducts, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`, 
                    },
                })
                .then(() => {
                    // Handle the success response from the backend
                    this.$toast.success('Product Added To Cart', {
                        position: 'top-right',
                        duration: 5000,
                    });

                    // You can also clear the selected products after adding them to the cart
                    this.categories.forEach((category) =>
                        category.products.forEach((product) => {
                            if (product.selected) {
                                product.selected = false;
                                product.quantityToAdd = 0;
                            }
                        })
                    );
                    setTimeout(location.reload.bind(location), 600);
                })
                .catch((error) => {
                    // Handle the error response from the backend
                    console.error('Error adding products to cart:', error);
                    alert('Failed to add products to cart. Please try again.');
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        },
    },
    beforeRouteEnter(to, from, next) {
        // Check if the user is logged in
        const isAuthenticated = store.state.isAuthenticated;

        if (!isAuthenticated) {
            
            alert('Please login to access the Product Catalog.');
            next('/login'); 
        } else {
            next();
        }
    },
};
</script>

<style scoped>
.add-to-cart-button {
    position: absolute;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    text-transform: uppercase;
}

.add-to-cart-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.shop-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    top: 50%;
    background-color: rgb(245, 245, 220);
}

table {
    border-collapse: collapse;
    width: 100%;
}

th,
td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.header {
    font-size: larger;
    color: hsl(0, 0%, 7%);
}


.categories-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}

.category {
    width: 100%;
    max-width: 600px;
    font-family: 'Comic Sans MS', cursive;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.product-card {
    background-color: white;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.product-name {
    font-size: 18px;
    font-weight: bold;
}

.product-details {
    margin-top: 10px;
    font-size: 14px;
    color: #555;
}

.product-actions {
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.quantity-input {
    flex: 1;
    padding: 2px 5px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 50px;
}
.custom-checkbox {
    position: relative;
    cursor: pointer;
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #ccc;
    border-radius: 4px;
    margin-right: 10px;
}

.custom-checkbox.checked {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

.custom-checkbox.checked::before {
    content: "\f058";
    font-family: "Bootstrap Icons";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
}
.custom-checkbox input[type="checkbox"] {
    opacity: 0;
    position: absolute;
}

.custom-checkbox input[type="checkbox"]:checked+.custom-checkbox {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

.custom-checkbox.plus::before {
    content: "+";
    font-family: Arial, sans-serif;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #555;
}
.custom-checkbox.plus input[type="checkbox"]:checked+.custom-checkbox {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

.custom-checkbox.plus.checked::before {
    content: "\f058";
    font-family: "Bootstrap Icons";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
}</style>
