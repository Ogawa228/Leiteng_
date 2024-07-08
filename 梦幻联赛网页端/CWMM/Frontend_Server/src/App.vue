<template>
  <div>
    <div id="background"></div>
    <div id="app">
      <router-view/>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#background {
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: url("./assets/background.png");
  position: fixed;
  background-position: center bottom;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  top: 0;
}

</style>
<script setup>

</script>