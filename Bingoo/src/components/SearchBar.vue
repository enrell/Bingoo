<script setup></script>

<template>
  <div class="search-container">
    <textarea
      name="Search"
      maxlength="1024"
      spellcheck="false"
      type="search"
      aria-label="Pesquisar"
    >
    </textarea>
    <button on-click="/ResultPage" @click="">Enviar</button>
  </div>
</template>

<style scoped>
textarea {
  width: 50vh;
  height: 2.5vh;
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
