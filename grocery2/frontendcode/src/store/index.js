// store/index.js

import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    isAuthenticated: false,
    token: null,
    showRegularNavbar: true,
    showStoreManagerNavbar: false,
    showAdminNavbar: false,
  },
  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
      localStorage.setItem('isAuthenticated', value);
    },
    setToken(state, token) {
      state.token = token; 
      localStorage.setItem('token', token);
    },
    setShowRegularNavbar(state, value) {
      state.showRegularNavbar = value;
    },
    setShowStoreManagerNavbar(state, value) {
      state.showStoreManagerNavbar = value;
    },
    setShowAdminNavbar(state, value) {
      state.showAdminNavbar = value;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/login', credentials);
        commit('setAuthenticated', true);
        commit('setToken', response.data.access_token);
      } catch (error) {
        console.error('Login failed:', error);
        throw new Error('Login failed. Please check your credentials and try again.');
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/logout');
        commit('setAuthenticated', false);
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('access_token');
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
  },
});

const isAuthenticated = localStorage.getItem('isAuthenticated');
if (isAuthenticated) {
  store.commit('setAuthenticated', JSON.parse(isAuthenticated));
}

export default store;
