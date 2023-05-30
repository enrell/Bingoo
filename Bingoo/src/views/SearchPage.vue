<script setup>
import SearchBar from '../components/SearchBar.vue'
</script>

<template>
  <main>
    <h1>Bingoo</h1>
    <SearchBar />
  </main>
</template>

<style scoped>
main {
  display: flex;
  width: 100vw;
  height: 100vh;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.search-container {
  display: flex;
  flex-direction: row;
  margin-bottom: 20vh;
}
h1 {
  font-size: 10vh;
  margin-bottom: 10vh;
  font-weight: bolder;
  color: #333333;
}
</style>
