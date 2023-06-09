<script>
import SearchBar from '../components/SearchBar.vue'
import { useStore } from 'vuex'
import { watch } from 'vue'
import axios from 'axios'

export default {
  components: {
    SearchBar
  },
  setup() {
    const store = useStore()
    let keyword = store.state.keyword

    const sendRequest = async () => {
      try {
        const response = await axios.get(`http://localhost:3000/api/search?keyword=${keyword}`)
        const links = response.data.links
        store.commit('setLinks', links)
      } catch (error) {
        console.error(error)
      }
    }

    watch(
      () => store.state.keyword,
      () => {
        sendRequest()
      }
    )

    return {
      sendRequest
    }
  }
}
</script>

<template>
  <main>
    <div class="search-container">
      <h1>Bingoo</h1>
    </div>
    <SearchBar @search="sendRequest"/>
    <div id="results">
      <ul v-if="$store.state.links.length > 0">
        <li v-for="(link, index) in $store.state.links" :key="index">
          <a :href="link" target="_blank">{{ link }}</a>
        </li>
      </ul>
       <p v-else class="no-results-message">Nenhum resultado encontrado para a pesquisa.</p>
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
