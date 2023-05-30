<script setup>
import SearchBar from '../components/SearchBar.vue'
import { ref } from 'vue'

</script>

<template>
  <main>
    <div class="search-container">
      <h1>Bingoo</h1>
    </div>
    <SearchBar />
    <div id="results">
      <ul>
        <li></li>
      </ul>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  width: 100vw;
  height: 100vh;
  flex-direction: column;
  align-items: center;
}
.search-container {
  display: flex;
  flex-direction: row;
}
h1 {
  font-size: 3vh;
  font-weight: bolder;
  color: #333333;
  margin-bottom: 2vh;
}
#results {
  display: flex;
  width: 80vw;
  height: 150vh;
}
</style>
