<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';

const USOS_API_URL = 'https://usosapps.uw.edu.pl/services'
const BACKEND_API_URL = import.meta.env.VITE_API_URL == undefined ? 'http://localhost:8000' : import.meta.env.VITE_API_URL

// api-backend
const message_sent = ref('')
const message = reactive({ str : message_sent.value})
const received_message = reactive({ str : ''})

function get_message_back() {
  message_sent.value = message.str

  axios.get(BACKEND_API_URL + '/mymessage', { // 'http://localhost:8000/mymessage' does not work, but '/mymessage' works
    params: {
      msg: message_sent.value
    }
  })
  .then(function (response) {
    received_message.str = response.data.message
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
}

const country = ref({})

function get_country() {
  axios.get(BACKEND_API_URL + '/countries/1/', {
  })
  .then(function (response) {
    country.value = response.data
    console.log(response)
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
}

// api-usos
const course_name = ref('')
const course = reactive({ name : course_name.value })
const courses_info = reactive({ arr : [] })
const groups = ref([])
const size = ref(0)
const selected = ref('')

function get_course_id() {
  groups.value = []
  course_name.value = course.name

  axios.get(USOS_API_URL + '/courses/search', {
    params: {
      lang: 'pl',
      name: course_name.value
    }
  })
  .then(function (response) {
    courses_info.arr = response.data.items
    size.value = courses_info.arr.length
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });  
}

function get_groups() {
  courses_info.arr = []
  course_name.value = course.name

  axios.get(USOS_API_URL + '/tt/course_edition', {
    params: {
      course_id: course_name.value,
      term_id: selected.value
    }
  })
  .then(function (response) {
    let collected = []
    for (let item of response.data)
      collected.push(item)
    console.log(collected);
    groups.value = collected
    size.value = collected.length
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });  
}

</script>

<template>
  <div id="page" v-if="true">
    <div id="api-usos">

      <input v-model="course.name" placeholder="Type here">
      <button @click="get_course_id">get course id</button>
      <button @click="get_groups">get groups</button>

      <span> Selected: {{ selected }}</span>
      <select v-model="selected">
        <option disabled value="">Please select one</option>
        <option>2023L</option>
        <option>2023Z</option>
        <option>2022L</option>
        <option>2022Z</option>
      </select>

      <p>Search for word: <b>{{ course.name }}</b></p>
      <p>Number of results: {{ size }}</p>

      <ul>
        <li v-for="c in courses_info.arr">
          <p>course_id = {{ c.course_id }}</p>
          <p>match = {{ c.match }}</p>
        </li>
      </ul>

      <ul>
        <li v-for="c in groups">
          <p>{{ c.name.pl }}</p>
          <p>{{ c.start_time }}</p>
          <p>{{ c.end_time }}</p>
        </li>
      </ul>

    </div>
    <div id="api-backend">
      <input v-model="message.str" placeholder="Type here">
      <button @click="get_message_back">get message back</button>
      <p>original message: <b>{{ message_sent }}</b></p>
      <p>received message: {{ received_message.str }}</p>
      <button @click="get_country">get country</button>
      <pre>{{ country }}</pre>
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