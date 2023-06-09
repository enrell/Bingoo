import { createStore } from 'vuex'

const store = createStore({
  state() {
    return {
      links: [],
      keyword: ''
    }
  },
  mutations: {
    setLinks(state, links) {
      state.links = links
    }
  }
})

export default store
