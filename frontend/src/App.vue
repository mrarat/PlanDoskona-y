<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const USOS_API_URL = 'https://usosapps.uw.edu.pl/services'
const BACKEND_API_URL =
  import.meta.env.VITE_API_URL == undefined ? 'http://localhost:8000' : import.meta.env.VITE_API_URL

const message_sent = ref('')

// Drawer
const drawer = ref(null)

// Select semester
const select_semester = ref(null);
const items_semester = ref([
  { title: 'Semestr letni 2023/2024 (2023L)', value: '2023L' },
  { title: 'Semestr zimowy 2023 (2023Z)', value: '2023Z' },
  { title: 'Semestr letni 2022/2023 (2022L)', value: '2022L' },
  { title: 'Semestr zimowy 2022 (2022Z)', value: '2022Z' },
  { title: 'Semestr letni 2021/2022 (2021L)', value: '2021L' },
  { title: 'Semestr zimowy 2021 (2021Z)', value: '2021Z' },
]);

// Select course
const loading_course = ref(false)
const search_course = ref(null)
const select_course = ref(null);
const items_course = ref([]);

async function query_course_search(course_name) {
  loading_course.value = true

  await axios.get(USOS_API_URL + '/courses/search', {
      params: {
        lang: 'pl',
        name: course_name,
        fields: 'name|course_id',
        num: 20,
      }
    })
    .then(function (response) {
      //console.log(response.data.items[0])
      items_course.value = response.data.items.map((item) => { return {title: `${item.name.pl} (${item.course_id})`, value: item.course_id} } );
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
      loading_course.value = false
    })
}

// Load groups
async function query_course(course_id) {
  let course = null

  console.log(select_semester.value)

  await axios.get(USOS_API_URL + '/courses/course_edition', {
      params: {
        course_id: course_id,
        term_id: select_semester.value,
        fields: 'course_name|term_id|course_units_ids',
      }
    })
    .then(function (response) {
      console.log('got course data')
      console.log(response.data)
      course = response.data;
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
      return course
    })
}

async function query_unit_groups_numbers(unit_id) {
  let unit_groups_ids = null

  await axios.get(USOS_API_URL + '/courses/course_unit', {
      params: {
        course_unit_id: course_unit_id,
        term_id: select_semester.value.value,
        fields: 'class_groups',
      }
    })
    .then(function (response) {
      console.log(response.data)
      unit_groups_ids = response.data.class_groups.map(item => item.number);
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
    })

    return unit_groups_ids
}

async function query_group_dates(unit_id, group_number) {
  let group_dates = null

  await axios.get(USOS_API_URL + '/tt/classgroup_dates2', {
      params: {
        course_unit_id: course_unit_id,
        term_id: select_semester.value.value,
        fields: 'class_groups',
      }
    })
    .then(function (response) {
      console.log(response.data)
      group_dates = response.data;
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
    })

    return group_dates
}

function query_unit_dates(unit_id) {
  let unit = { id: unit_id }

  let group_numbers = query_unit_groups_numbers(unit_id)
  unit.groups = group_numbers.map(gn => { return { number: gn, dates: query_group_dates(unit_id, gn)}})

  return unit
}

async function query_course_dates(course_id) {
  let course = await query_course(course_id)
  console.log(`course is null: ${course === null}`)
  console.log('course:')
  console.log(course)
  course.units = course.course_units_ids.map(cu_id => query_unit_dates)
  return course
}

function query(x) {
  //console.log(x)
  console.log(query_course_dates(x))
}

</script>

<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" 
      class="bg-deep-purple"
      theme="dark"
      width="500"
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
        <v-autocomplete
          v-model="select_course"
          v-model:search="search_course"
          :loading="loading_course"
          :items="items_course"
          item-title="title"
          item-value="value"
          hide-no-data
          hide-details
          label="Wyszukaj przedmiot"
          @keyup.native.enter="query_course_search(search_course)"
        ></v-autocomplete>
      </v-list-item>

      <v-list-item>
        <v-btn variant="outlined" @click="query(select_course)">
          Button
        </v-btn>
      </v-list-item>
    </v-list>
      
    </v-navigation-drawer>

    <v-app-bar absolute color="pink">
      <v-app-bar-nav-icon @click="drawer = !drawer">+</v-app-bar-nav-icon>

      <v-toolbar-title>PlanDoskonały</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <!--  -->
      
    </v-main>
  </v-app>
</template>

<style scoped>
</style>
