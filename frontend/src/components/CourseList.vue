<script setup>
import { useCoursesStore } from '@/store/coursesStore'
const coursesStore = useCoursesStore()
</script>

<template>
  <v-expansion-panels>
    <v-expansion-panel v-for="(course, index) in coursesStore.courses" :key="index">
      <v-expansion-panel-title color="teal">
        <span>{{ course.course_name.pl }} ({{ course.course_id }})</span>
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
                <v-col cols="6" class="flex-grow-0">
                  <v-sheet>
                    <span>{{ group.dates[0]?.name?.pl || 'Nieznany typ zajęć' }} gr. {{ group.number }}</span>
                  </v-sheet>
                </v-col>

                <v-col cols="4" class="flex-grow-0">
                  <v-sheet>
                    <span>{{ group.submit_count || 0 }}</span>
                  </v-sheet>
                </v-col>

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
</template>
