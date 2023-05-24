<script setup>
import { ref } from 'vue'
import axios from 'axios'

const USOS_API_URL = 'https://usosapps.uw.edu.pl/services'

const message_sent = ref('')

// Drawer
const drawer = ref(null)

// Select semester
const select_semester = ref(null)
const items_semester = ref([
  { title: 'Semestr letni 2023/2024 (2023L)', value: '2023L' },
  { title: 'Semestr zimowy 2023 (2023Z)', value: '2023Z' },
  { title: 'Semestr letni 2022/2023 (2022L)', value: '2022L' },
  { title: 'Semestr zimowy 2022 (2022Z)', value: '2022Z' },
  { title: 'Semestr letni 2021/2022 (2021L)', value: '2021L' },
  { title: 'Semestr zimowy 2021 (2021Z)', value: '2021Z' }
])

// Select course
const loading_course = ref(false)
const search_course = ref(null)
const select_course = ref(null)
const items_course = ref([])

async function query_course_search(course_name) {
  loading_course.value = true

  await axios
    .get(USOS_API_URL + '/courses/search', {
      params: {
        lang: 'pl',
        name: course_name,
        fields: 'name|course_id',
        num: 20
      }
    })
    .then(function (response) {
      //console.log(response.data.items[0])
      items_course.value = response.data.items.map((item) => {
        return { title: `${item.name.pl} (${item.course_id})`, value: item.course_id }
      })
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {
      loading_course.value = false
    })
}

// Load groups
async function query_course_edition(course_id, term_id) {
  let course = null

  await axios
    .get(USOS_API_URL + '/courses/course_edition', {
      params: {
        course_id: course_id,
        term_id: term_id,
        fields: 'course_name|term_id|course_units_ids|course_id'
      }
    })
    .then(function (response) {
      course = response.data
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {})

  return course
}

async function query_course_unit(course_unit_id) {
  let unit = null

  await axios
    .get(USOS_API_URL + '/courses/course_unit', {
      params: {
        course_unit_id: course_unit_id,
        fields: 'id|class_groups'
      }
    })
    .then(function (response) {
      unit = response.data
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {})

  return unit
}

async function query_classgroup_dates(unit_id, group_number) {
  let dates = null

  //await new Promise((resolve) => setTimeout(resolve, 1000))

  await axios
    .get(USOS_API_URL + '/tt/classgroup_dates2', {
      params: {
        unit_id: unit_id,
        group_number: group_number
      }
    })
    .then(function (response) {
      dates = response.data
    })
    .catch(function (error) {
      console.log(error)
    })
    .finally(function () {})

  return dates
}

async function get_unit(course_unit_id) {
  let unit = await query_course_unit(course_unit_id)

  /*
  // requests are sent one after another
  for (var group of unit.class_groups) {
    group.selected = true
    group.dates = await query_classgroup_dates(group.course_unit_id, group.number)
  }
  */

  // requests are sent asynchronously
  const promises = unit.class_groups.map(async (group) => {
    group.selected = true
    group.dates = await query_classgroup_dates(group.course_unit_id, group.number)
    return group
  })

  unit.class_groups = await Promise.all(promises)

  return unit
}

async function get_course(course_id, term_id) {
  let course = await query_course_edition(course_id, term_id)
  course.units = await Promise.all(
    course.course_units_ids.map((course_unit_id) => get_unit(course_unit_id))
  )

  return course
}

function print_course(course_id, term_id) {
  get_course(course_id, term_id).then(function (response) {
    console.log(response)
  })
}

/*
{
  courses: [
    {
      // from services/courses/course_edition
      "course_name": {
          "pl": "Matematyka dyskretna",
          "en": "Discrete mathematics"
      },
      "term_id": "2022L",
      "course_units_ids": [
          "486449",
          "486450"
      ],
      "course_id": "1000-212bMD"

      // added
      units: [
        {
          // from services/courses/course_unit
          "class_groups": [
            {
                "course_unit_id": "486450",
                "number": 1

                // from services/tt/classgroup_dates2
                dates: [
                  {
                    "start_time": "2023-02-27 12:15:00",
                    "end_time": "2023-02-27 14:00:00",
                    "name": {
                        "pl": "Ćwiczenia",
                        "en": "Class"
                    }
                  },
                  {
                    "start_time": "2023-03-03 10:15:00",
                    "end_time": "2023-03-03 12:00:00",
                    "name": {
                        "pl": "Ćwiczenia",
                        "en": "Class"
                    }
                  },
                ]

                // added option if it is included in a plan
                "selected": true
            },
            {
                "course_unit_id": "486450",
                "number": 2
            },
            {
                "course_unit_id": "486450",
                "number": 3
            },
            {
                "course_unit_id": "486450",
                "number": 4
            },
            {
                "course_unit_id": "486450",
                "number": 5
            },
            {
                "course_unit_id": "486450",
                "number": 6
            },
            {
                "course_unit_id": "486450",
                "number": 7
            },
            {
                "course_unit_id": "486450",
                "number": 8
            },
            {
                "course_unit_id": "486450",
                "number": 9
            }
          ]

          "id": 486450 // "course_unit_id": 486450 // added for redundancy
        }
      ]
    }
  ]
}
*/

const rerenderKey = ref(0)

function rerender() {
  rerenderKey.value++
}

import { useCoursesStore } from './store/coursesStore'
const coursesStore = useCoursesStore()

async function addCourse(course_id, term_id) {
  let course = await get_course(course_id, term_id)
  coursesStore.addCourse(course)
  //rerender()
}

// testing
const courses = ref([])

let cid = 0
function addc() {
  courses.value.push({
    id: cid,
    name: `Course ${cid}`
  })

  cid++
}

</script>

<template>
  <v-app id="inspire">
    <v-navigation-drawer app v-model="drawer" class="bg-deep-purple" theme="dark" width="500" height="100%" permanent :key="rerenderKey">
      <!--  -->
      <div style="overflow-y: scroll; height: 100%" :key="rerenderKey">
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
            @keyup.enter="query_course_search(search_course)"
          ></v-autocomplete>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="addCourse(select_course, select_semester)"> dodaj przedmiot </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="console.log(coursesStore.courses)">
            store
          </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="rerender">
            rerender
          </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="addc">
            addc
          </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="addCourse('1000-212bMD', '2022L')">
            add MD
          </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn variant="outlined" @click="addCourse('1000-214bIOP', '2022L')">
            add IOP
          </v-btn>
        </v-list-item>
      </v-list>

      

      <!--
      <v-expansion-panels>
        <v-expansion-panel
          v-for="course in coursesStore.courses"
          :key="{ course_id: course.course_id, term_id: course.term_id}"
          style="overflow-y: visible;"
        >
          <v-expansion-panel-title color="teal">
            <span>{{ course.course_name.pl }}</span>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-btn color="orange-darken-4">Delete</v-btn>
            <div
              v-for="unit in course.units"
              :key="unit.id"
            >
              <v-list>
                <v-list-item
                  v-for="group in unit.class_groups"
                  :key="{ course_unit_id: group.course_unit_id, number: group.number }"
                >
                  <v-row class="d-flex align-center justify-space-between">
                    <v-col cols="10" class="flex-grow-0"><v-sheet><span>{{ group.dates[0].name.pl }} | {{ group.number }}</span></v-sheet></v-col>
                    <v-col cols="2" class="flex-grow-0"><v-sheet><v-checkbox hide-details density="compact" class="float-right"></v-checkbox></v-sheet></v-col>
                  </v-row>
                </v-list-item>
              </v-list>
            </div>
            
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
      -->

      <!--
      <v-expansion-panels>
        <v-expansion-panel
          v-for="i in 15"
          :key="i"
        >
          <v-expansion-panel-title color="teal">
            <span>course_name</span>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-btn color="orange-darken-4">Delete</v-btn>
            <div
              v-for="i in 3"
              :key="i"
            >
              <v-list>
                <v-list-item
                  v-for="i in 6"
                  :key="i"
                >
                  <v-row class="d-flex align-center justify-space-between">
                    <v-col cols="10" class="flex-grow-0"><v-sheet><span>group</span></v-sheet></v-col>
                    <v-col cols="2" class="flex-grow-0"><v-sheet><v-checkbox hide-details density="compact" class="float-right"></v-checkbox></v-sheet></v-col>
                  </v-row>
                </v-list-item>
              </v-list>
            </div>
            
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
      -->

      <!--
      <v-expansion-panels>
        <v-expansion-panel
          v-for="course in courses"
          :key="course.id"
        >
          <v-expansion-panel-title color="teal">
            <span>{{ course.name }}</span>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-btn color="orange-darken-4">Delete</v-btn>
            <div
              v-for="i in 3"
              :key="i"
            >
              <v-list>
                <v-list-item
                  v-for="i in 6"
                  :key="i"
                >
                  <v-row class="d-flex align-center justify-space-between">
                    <v-col cols="10" class="flex-grow-0"><v-sheet><span>group</span></v-sheet></v-col>
                    <v-col cols="2" class="flex-grow-0"><v-sheet><v-checkbox hide-details density="compact" class="float-right"></v-checkbox></v-sheet></v-col>
                  </v-row>
                </v-list-item>
              </v-list>
            </div>
            
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
      -->

      <v-expansion-panels>
        <v-expansion-panel
          v-for="(course, index) in coursesStore.courses"
          :key="index"
        >
          <v-expansion-panel-title color="teal">
            <span>{{ course.course_name.pl }}</span>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-btn color="orange-darken-4">Delete</v-btn>
            <div
              v-for="unit in course.units"
              :key="unit.id"
            >
              <v-list>
                <v-list-item
                  v-for="group in unit.class_groups"
                  :key="group.number"
                >
                  <v-row class="d-flex align-center justify-space-between">
                    <v-col cols="10" class="flex-grow-0"><v-sheet><span>{{ group.dates[0].name.pl }} | {{ group.number }}</span></v-sheet></v-col>
                    <v-col cols="2" class="flex-grow-0"><v-sheet><v-checkbox hide-details density="compact" class="float-right"></v-checkbox></v-sheet></v-col>
                  </v-row>
                </v-list-item>
              </v-list>
            </div>
            
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
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

<style scoped></style>
