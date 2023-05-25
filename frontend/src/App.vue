<script setup>
import { ref } from 'vue'

import CourseSearch from '@/components/CourseSearch.vue'
import CourseList from '@/components/CourseList.vue'
import Algorithm from '@/components/Algorithm.vue'

// Drawer
const drawer = ref(null)
</script>

<template>
  <div style="width: 100%; height: 62px"></div>
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
        
        <div style="width: 100%; height: 53px"></div>
        <CourseSearch></CourseSearch>
        <CourseList></CourseList>
      </div>
    </v-navigation-drawer>
    >

    <v-app-bar absolute color="pink-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>PlanDoskonały</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <Algorithm></Algorithm>
    </v-main>
  </v-app>
</template>
