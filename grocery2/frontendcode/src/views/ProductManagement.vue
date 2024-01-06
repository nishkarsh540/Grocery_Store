<template>
    <div class="container">
        <div class="add_product">
            <h1>Add Product</h1>
            <form @submit.prevent="addProduct" class="add-product-form">
                <table>
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Expiry Date</th>
                            <th>Manufacture Date</th>
                            <th>Category</th>
                            <th>Price</th>
                            <th>Unit</th>
                            <th>Quantity</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input  v-model="productName" type="text" placeholder="Product Name" required></td>
                            <td><input v-model="expiryDate" type="date" required></td>
                            <td><input v-model="manufactureDate" type="date" required></td>
                            <td>
                                <select v-model="selectedCategoryId" required>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </td>
                            <td><input v-model="price" type="number" min="0" step="0.01" placeholder="Price" required></td>
                            <td>
                                <select v-model="unit" required>
                                    <option value="piece">Piece</option>
                                    <option value="kg">Kg</option>
                                    <option value="litre">Litre</option>
                                    <option value="dozens">Dozens</option>
                                    <option value="gallons">Gallons</option>
                                </select>
                            </td>
                            <td><input v-model="quantity" type="number" placeholder="Quantity" required></td>
                            <td><button class="btn btn-danger" type="submit">Add Product</button></td>
                        </tr>
                    </tbody>
                </table>
            </form>
        </div>

        <div class="manage_product">
            <h1>Existing Products</h1>
            <table v-if="products.length > 0">
                <thead>
                    <tr>
                        <th>Product Name</th>
                        <th>Expiry Date</th>
                        <th>Manufacture Date</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Unit</th>
                        <th>Quantity</th>
                        <th>Edit</th>
                        <th>Remove</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in products" :key="product.id">
                        <td>{{ product.name }}</td>
                        <td>{{ product.expiry_date }}</td>
                        <td>{{ product.manufacture_date }}</td>
                        <td>{{ getCategoryNameById(product.category_id) }}</td>
                        <td>{{ product.price }}</td>
                        <td>{{ product.unit }}</td>
                        <td>{{ product.quantity }}</td>
                        <td><button class="btn btn-danger" @click="editProduct(product)">Edit</button></td>
                        <td><button  class="btn btn-danger" style="background-color: #dc3545;" @click="removeProduct(product)">Remove</button></td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No products found.</p>
        </div>
        <div class="modal-overlay" v-if="showEditModal">
        <div  class="modal">
        <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Edit Product</h5>
            <button type="button" class="close" @click="closeEditModal">
            <span>&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form @submit.prevent="saveEditedProduct">
            <div class="form-group">
                <label for="productName">Product Name</label>
                <input
                v-model="editedProduct.name"
                type="text"
                id="productName"
                class="form-control"
                required
                />
            </div>
            <div class="form-group">
                <label for="expiryDate">Expiry Date</label>
                <input
                v-model="editedProduct.expiryDate"
                type="date"
                id="expiryDate"
                class="form-control"
                required/>
            </div>
            
            <div class="form-group">
                <label for="manufactureDate">Manufacture Date</label>
                <input
                v-model="editedProduct.manufactureDate"
                type="date"
                id="manufactureDate"
                class="form-control"
                required
                />
            </div>
            <div class="form-group">
                <label for="selectedCategoryId">Category</label>
                <select
                v-model="editedProduct.selectedCategoryId"
                id="selectedCategoryId"
                class="form-control"
                required>
                <option value="" disabled>Select a category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                </option>
                </select>
            </div>
            <div class="form-group">
                <label for="price">Price</label>
                <input
                v-model="editedProduct.price"
                type="number"
                min="0"
                step="0.01"
                id="price"
                class="form-control"
                required/>
            </div>
            
            <div class="form-group">
                <label for="unit">Unit</label>
                <select v-model="editedProduct.unit" id="unit" class="form-control" required>
                <option value="piece">Piece</option>
                <option value="kg">Kg</option>
                <option value="litre">Litre</option>
                <option value="dozens">Dozens</option>
                <option value="gallons">Gallons</option>
                </select>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity</label>
                <input
                v-model="editedProduct.quantity"
                type="number"
                id="quantity"
                class="form-control"
                required
                />
            </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditModal">
            Close
            </button>
            <button type="button" class="btn btn-primary" @click="saveEditedProduct">
            Save Changes
            </button>
        </div>
        </div>
        </div>
        </div>
    </div>
    
    <div class="modal-overlay" v-if="showConfirmationModal">
            <div class="modal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Confirm Removal</h5>
                            <button type="button" class="close" @click="cancelRemoveProduct">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>Are you sure you want to remove this product?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" style="margin-right: 110px;" class="btn btn-secondary" @click="cancelRemoveProduct">
                                Cancel
                            </button>
                            <button type="button" style="background-color: #dc3545; margin-left: 40px;"  class="btn btn-danger" @click="confirmRemoveProduct">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            user_id: JSON.parse(localStorage.getItem('user')).user_id, 
            showConfirmationModal: false,
            productToRemove: null,
            categories: [],
            products: [],
            productName: "",
            expiryDate: "",
            manufactureDate: "",
            selectedCategoryId: null,
            price: 0,
            unit: "piece",
            quantity: 0,
            showEditModal: false,
            editedProduct: {
                id: null,
                name: "",
                expiryDate: "",
                manufactureDate: "",
                selectedCategoryId: null,
                price: 0,
                unit: "piece",
                quantity: 0,
            },
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
                    this.products = response.data.products;
                    this.categories = response.data.categories;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                });
        },
        getCategoryNameById(categoryId) {
            const category = this.categories.find((category) => category.id === categoryId);
            return category ? category.name : "Unknown Category";
        },
        confirmRemoveProduct() {
            this.showConfirmationModal = false;

            if (this.productToRemove) {
                const productId = this.productToRemove.id;
                const accessToken = localStorage.getItem('access_token');
                axios.delete(`/api/store-manager/${this.user_id}/product_management`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                    data: { id: productId }, 
                })
                    .then(() => {
                        this.fetchDataFromBackend();
                        this.$toast.success('Product Removed Successfully', {
                            position: 'top-right',
                            duration: 5000, 
                        });
                    })
                    .catch((error) => {
                        console.error("Error removing product:", error);
                        this.$toast.error(error.response.data.message, {
                            position: 'top-right',
                            duration: 5000, 
                        });
                    });
            }

            this.productToRemove = null;
        },

        removeProduct(product) {
            this.productToRemove = product;
            this.showConfirmationModal = true;
        },
        cancelRemoveProduct() {
            this.productToRemove = null;
            this.showConfirmationModal = false;
        },

        closeConfirmationModal() {
            this.productToRemove = null;
            this.showConfirmationModal = false;
        },
        editProduct(product) {
            this.editedProduct.id = product.id;
            this.editedProduct.name = product.name;
            this.editedProduct.expiryDate = product.expiry_date;
            this.editedProduct.manufactureDate = product.manufacture_date;
            this.editedProduct.selectedCategoryId = product.category_id;
            this.editedProduct.price = product.price;
            this.editedProduct.unit = product.unit;
            this.editedProduct.quantity = product.quantity;

            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editedProduct = {
                id: null,
                name: "",
                expiryDate: "",
                manufactureDate: "",
                selectedCategoryId: null,
                price: 0,
                unit: "piece",
                quantity: 0,
            };
        },
         saveEditedProduct() {
            const expiryDateObject = new Date(this.editedProduct.expiryDate);
            const manufactureDateObject = new Date(this.editedProduct.manufactureDate);
            const updatedProduct = {
                id: this.editedProduct.id,
                name: this.editedProduct.name,
                expiry_date: expiryDateObject.toISOString().slice(0, 10),
                manufacture_date: manufactureDateObject.toISOString().slice(0, 10),
                category_id: this.editedProduct.selectedCategoryId,
                price: this.editedProduct.price,
                unit: this.editedProduct.unit,
                quantity: this.editedProduct.quantity,
            };

            const accessToken = localStorage.getItem('access_token');
            axios
                .put(`/api/store-manager/${this.user_id}/product_management`, updatedProduct, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then(() => {
                    this.closeEditModal();
                    this.fetchDataFromBackend();
                    this.$toast.success('Product Updated Successfully', {
                        position: 'top-right',
                        duration: 5000,
                    });
                })
                .catch((error) => {
                    console.error("Error updating product:", error);
                    this.$toast.error(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000,
                    });
                });
        },
        addProduct() {
            const expiryDateObject = new Date(this.expiryDate);
            const manufactureDateObject = new Date(this.manufactureDate);
            const newProduct = {
                name: this.productName,
                expiry_date: expiryDateObject.toISOString().slice(0, 10),
                manufacture_date: manufactureDateObject.toISOString().slice(0, 10),
                category_id: this.selectedCategoryId,
                price: this.price,
                unit: this.unit,
                quantity: this.quantity,
            };

            const accessToken = localStorage.getItem('access_token');
            axios.post(`/api/store-manager/${this.user_id}/product_management`, newProduct, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            })
                .then(() => {
                    this.productName = "";
                    this.expiryDate = "";
                    this.manufactureDate = "";
                    this.selectedCategoryId = null;
                    this.price = 0;
                    this.unit = "piece";
                    this.quantity = 0;
                    this.$toast.success('Product Added Succesfully', {
                        position: 'top-right',
                        duration: 5000, 
                    });
                    setTimeout(location.reload.bind(location), 600);
                })
                .catch((error) => {
                    console.error("Error adding product:", error);
                    this.$toast.success(error.response.data.message, {
                        position: 'top-right',
                        duration: 5000, 
                    });
                });
        }


    },

};
</script>


<style scoped>
body {
    background-color: peachpuff;

}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.modal-header h3 {
  margin: 0;
}
.close-btn {
  cursor: pointer;
  font-size: 20px;
  border: none;
  background: none;
  padding: 0;
  color: #888;
}
.modal-dialog {
  padding: 20px;
}
.modal-header h5 {
  margin: 0;
}
.modal-content {
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.close-btn:hover {
  color: #555;
}

.modal-content {
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.btn {
  cursor: pointer;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: bold;
  color: #fff;
  transition: background-color 0.3s ease;
}

.cancel-btn {
  background-color: #ccc;
}

.save-btn {
  background-color: #007bff;
  margin-left: 10px;
}

.btn:hover {
  background-color: #0056b3;
}
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: peachpuff;
}

.manage_product {
    width: 100%; 
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}
.add_product {
    width: 100%; 
    max-width: 950px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 20px;
    background-color: lightblue;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #66a3d2;
}
.add-product-form .btn {
    padding: 8px 20px;
}
</style>