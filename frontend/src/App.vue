<script setup>
import { ref } from 'vue'

import CourseSearch from './components/CourseSearch.vue'

import { useCoursesStore } from './store/coursesStore'
const coursesStore = useCoursesStore()

// Drawer
const drawer = ref(null)

</script>

<template>
  <v-app id="inspire">
    <v-navigation-drawer
      app
      v-model="drawer"
      class="bg-deep-purple"
      theme="dark"
      width="500"
      height="100%"
      permanent
    >
      <div style="overflow-y: scroll; height: 100%">
        <CourseSearch></CourseSearch>

        <v-expansion-panels>
          <v-expansion-panel v-for="(course, index) in coursesStore.courses" :key="index">
            <v-expansion-panel-title color="teal">
              <span>{{ course.course_name.pl }}</span>
            </v-expansion-panel-title>

            <v-expansion-panel-text>
              <v-btn
                color="orange-darken-4"
                @click="coursesStore.deleteCourse(course.course_id, course.term_id)"
                >usuń</v-btn
              >
              <div v-for="unit in course.units" :key="unit.id">
                <v-list>
                  <v-list-item v-for="group in unit.class_groups" :key="group.number">
                    <v-row class="d-flex align-center justify-space-between">
                      <v-col cols="10" class="flex-grow-0"
                        ><v-sheet
                          ><span>{{ group.dates[0].name.pl }} gr. {{ group.number }}</span></v-sheet
                        ></v-col
                      >
                      <v-col cols="2" class="flex-grow-0"
                        ><v-sheet
                          ><v-checkbox
                            hide-details
                            density="compact"
                            class="float-right"
                            v-model="group.selected"
                          ></v-checkbox></v-sheet
                      ></v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </v-navigation-drawer>

    <v-app-bar absolute color="pink-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>PlanDoskonały</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <!--  -->
    </v-main>
  </v-app>
</template>

<style scoped></style>
