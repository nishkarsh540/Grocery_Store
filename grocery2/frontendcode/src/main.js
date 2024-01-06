import { createApp } from 'vue';
import App from './App.vue';
import router from './routes';
import store from './store'; 
import axios from 'axios';
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-default.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App);

axios.defaults.baseURL = 'http://127.0.0.1:8000'; 
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
});
app.use(router);
app.use(store);
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

app.config.globalProperties.$axios = axiosInstance;
app.use(VueToast);
app.mount('#app');
