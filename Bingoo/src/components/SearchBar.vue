<script>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  setup() {
    const searchTerm = ref('')
    const router = useRouter()
    const store = useStore()

    const sendRequest = () => {
      const keyword = searchTerm.value

      axios
        .get(`http://localhost:3000/api/search?keyword=${keyword}`)
        .then((response) => {
          console.log(response.data)

          const links = response.data.links
          store.commit('setLinks', links)
          router.push('/ResultPage')
        })
        .catch((error) => {
          console.error(error)
        })
    }
    return {
      searchTerm,
      sendRequest
    }
  }
}
</script>

<template>
  <div class="search-container">
    <input type="search" v-model="searchTerm" @keyup.enter="sendRequest"/>
    <button @click="sendRequest" >Enviar</button>
  </div>
</template>

<style scoped>
input {
  width: 50vh;
  height: 5vh;
  font-size: 2vh;
  padding: 0.5em;
  border: 0.2em solid #000000;
  border-radius: 1.5vh;
  resize: none;
}
button {
  width: 5vh;
  height: 5vh;
  margin-right: 1vh;
  border: 0.2em solid #333333;
  border-radius: 1.5vh;
  background-color: #333333;
  color: white;
  font-size: 1vh;
  font-weight: bold;
}
button:active {
  background-color: #f2f2f2;
  color: #333333;
}
</style>
