<template>
  <div id="app">
    <nav-bar />
    <router-view />
  </div>
</template>

<script>
import NavBar from "@/navbar/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
body {
  font-family: sans-serif;
  margin: 0;
  padding: 0;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  height: auto;
  min-height: 100%;
  min-width: 1024px;
  width: 100%;
}
</style>
