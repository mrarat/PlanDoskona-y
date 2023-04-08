<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';

// api-usos
const course_name = ref('')
const course = reactive({ name : course_name.value })
const courses_info = reactive({ arr : [] })

function get_course_id() {
  course_name.value = course.name

  axios.get('https://usosapps.uw.edu.pl/services/courses/search', {
    params: {
      lang: 'pl',
      name: course_name.value
    }
  })
  .then(function (response) {
    courses_info.arr = response.data.items
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });  
}

// api-backend
const message_sent = ref('')
const message = reactive({ str : message_sent.value})
const received_message = reactive({ str : ''})

function get_message_back() {
  message_sent.value = message.str

  /* TODO
  axios.get('localhost:<port>/sth', {
    params: {
      msg: message_sent.value
    }
  })
  .then(function (response) {
    
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
  */  
}

</script>

<template>
  <div id="page" v-if="true">
    <div id="api-usos">
      <input v-model="course.name" placeholder="Type here">
      <button @click="get_course_id">get course id</button>
      <p>Search for word: <b>{{ course_name.value }}</b></p>
      <p>Number of results: {{ courses_info.arr.length }}</p>
      <ul>
        <li v-for="c in courses_info.arr">
          <p>course_id = {{ c.course_id }}</p>
          <p>match = {{ c.match }}</p>
        </li>
      </ul>
    </div>
    <div id="api-backend">
      <input v-model="message.str" placeholder="Type here">
      <button @click="get_message_back">get message back</button>
      <p>original message: <b>{{ message_sent.value }}</b></p>
      <p>received message: {{ received_message.str }}</p>
    </div>
  </div>
</template>

<style scoped>
#page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto;
  grid-template-areas:
    "api-usos api-backend";
  height: 100vh;
  gap: 10px;
  background: black;
  margin: 0;
}

#api-usos {
  grid-area: api-usos;
  background: white;
  padding: 1rem;
  margin: 10px;
  overflow: scroll;
}

#api-backend {
  grid-area: api-backend;
  background: white;
  padding: 1rem;
  margin: 10px;
  overflow: scroll;
}

input {
  width: 100%;
}
</style>