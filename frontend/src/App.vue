<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const USOS_API_URL = 'https://usosapps.uw.edu.pl/services'
const BACKEND_API_URL =
  import.meta.env.VITE_API_URL == undefined ? 'http://localhost:8000' : import.meta.env.VITE_API_URL

  const drawer = ref(null)

const select_semester = ref(null);
const items_semester = ref([
  { title: 'Semestr letni 2023/2024 (2023L)', value: '2023L' },
  { title: 'Semestr zimowy 2023 (2023Z)', value: '2023Z' },
  { title: 'Semestr letni 2022/2023 (2022L)', value: '2022L' },
  { title: 'Semestr zimowy 2022 (2022Z)', value: '2022Z' },
  { title: 'Semestr letni 2021/2022 (2021L)', value: '2021L' },
  { title: 'Semestr zimowy 2021 (2021Z)', value: '2021Z' },
]);

const select_course = ref(null);
const items_course = ref([{ state: 'some state', abbr: 'some abbr' },]);

const search1 = async (query) => {
  if (!query) return;
  
  // Simulate a 400ms delay
  await new Promise((resolve) => setTimeout(resolve, 400));

  // Assign the simulated data to items1
  items_course.value = [
    { state: 'some state', abbr: 'some abbr' },
  ];
};

const loading_test = ref(false)
const search_test = ref(null)
const select_test = ref(null);
const items_test = ref([]);

function query_course(course_name) {
  axios.get(USOS_API_URL + '/courses/search', {
      params: {
        lang: 'pl',
        name: course_name,
        fields: 'name|course_id',
        num: 20,
      }
    })
    .then(function (response) {
      console.log(response.data.items[0])
      items_test.value = response.data.items.map((item) => { return {title: `${item.name.pl} (${item.course_id})`, value: item.course_id} } );
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
      // always executed
    })

  items_test.value = [
    { title: 'md', value: 5},
  ]
}

const loading = ref(false)
const items = ref([])
const search = ref(null)
const select = ref(null)
const states = [
  'Alabama',
  'Alaska',
  'American Samoa',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'District of Columbia',
  'Federated States of Micronesia',
  'Florida',
  'Georgia',
  'Guam',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Marshall Islands',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Northern Mariana Islands',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Palau',
  'Pennsylvania',
  'Puerto Rico',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virgin Island',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]

/*
watch(search, val => {
  if (val && val !== select.value) {
    querySelections(val)
  }
})
*/

function querySelections(v) {
  loading.value = true
  // Simulated ajax query
  setTimeout(() => {
    items.value = states.filter(e => {
      return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
    })
    loading.value = false
  }, 500)
}

</script>

<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" 
      class="bg-deep-purple"
      theme="dark"
      width="400"
      permanent
    >
      <!--  -->
      <v-list>
      <v-list-item>
        <v-select
          v-model="select_semester"
          :items="items_semester"
          item-title="title"
          item-value="value"
          label="Wybierz semestr"
        ></v-select>
      </v-list-item>

      <v-list-item>
        <v-select
          v-model="select_course"
          :hint="select_course ? `${select_course.state}, ${select_course.abbr}` : 'nazwa przedmiotu, kod przedmiotu'"
          :items="items_course"
          item-title="state"
          item-value="abbr"
          label="Wyszukaj przedmiot"
          placeholder="Wyszukaj przedmiot"
          persistent-hint
          return-object
          single-line
        ></v-select>
      </v-list-item>

      <v-list-item>
        <v-autocomplete
          v-model="select_test"
          v-model:search="search_test"
          :loading="loading_test"
          :items="items_test"
          item-title="title"
          item-value="value"
          hide-no-data
          hide-details
          label="Wyszukaj przedmiot"
          @keyup.native.enter="query_course(search_test)"
        ></v-autocomplete>
      </v-list-item>

      <v-list-item>
        <v-autocomplete
          v-model="select"
          v-model:search="search"
          :loading="loading"
          :items="items"
          hide-no-data
          hide-details
          label="What state are you from?"
          @keyup.native.enter="querySelections(search)"
        ></v-autocomplete>
      </v-list-item>

    </v-list>
      
    </v-navigation-drawer>

    <v-app-bar absolute color="pink">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>PlanDoskonały</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <!--  -->
      
    </v-main>
  </v-app>
</template>

<style scoped>
.v-app-bar {
  background-color: purple;
}
</style>
