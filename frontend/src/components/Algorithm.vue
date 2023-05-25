<template>
    <v-btn
        @click="run()"
    >
    Stwórz plan doskonały!
    </v-btn>
    <keep-alive>
    <ejs-schedule height='550px' width='100%' :selectedDate='selectedDate' 
    :eventSettings='eventSettings'
    id='Schedule'>
    <e-views>
      <e-view option='Day'></e-view>
      <e-view option='Week'></e-view>
      <e-view option='WorkWeek'></e-view>
      <e-view option='Month'></e-view>
      <e-view option='Agenda'></e-view>
    </e-views>
    <e-resources>
      <e-resource field="OwnerId" title="Owner" name="Owners" :dataSource="ownerDataSource" textField="OwnerText"
        idField="Id" colorField="OwnerColor">
      </e-resource>
    </e-resources>
  </ejs-schedule>
</keep-alive>
</template>

<script setup>
import { useCoursesStore } from '@/store/coursesStore'

import { provide, ref } from "vue";
import {
  ScheduleComponent as EjsSchedule, ViewsDirective as EViews, ViewDirective as EView,
  ResourcesDirective as EResources, ResourceDirective as EResource,
  Day, Week, WorkWeek, Month, Agenda
} from "@syncfusion/ej2-vue-schedule";

provide('schedule', [Day, Week, WorkWeek, Month, Agenda]);


const selectedDate = new Date(2023, 7, 8);
let eventSettings = {
  dataSource: [
  ]
};
const ownerDataSource = [
  { OwnerText: "Nancy", Id: 1, OwnerColor: "#ffaa00" },
  { OwnerText: "Steven", Id: 2, OwnerColor: "#f8a398" },
  { OwnerText: "Michael", Id: 3, OwnerColor: "#7499e1" }
];



const coursesStore = useCoursesStore()
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

            // added option if it is included of a plan
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

      "course_unit_id": 486450 // added for redundancy
    }
  ]
}
]
}
*/
/*
Proxy(Object) {
    course_name: {…}, 
term_id: '2022L', 
course_units_ids: Array(2), 
course_id: '1000-212bMD',
 units: Array(2)}
*/
async function run() {
    console.log(coursesStore.courses[0].units[0].class_groups[0].dates[0].name)
    // Proxy(Object) {pl: 'Wykład', en: 'Lecture'}
    // preprocessing
    let n_groups = 0, n_possibilities = 1
    let n_valid_groups = []
    for (const course of coursesStore.courses) {
        let sum = 0
        for (const unit of course.units) {
            if (unit.class_groups[0].dates[0].name.pl != 'Wykład') {
                sum += unit.class_groups.length
            }
        }
        n_valid_groups.push(sum)
        n_groups += sum;
        n_possibilities *= sum;
    }
    let collisions = [n_groups][n_groups];
    let id_1 = 0, id_2 = 0;
    for (let i_1 = 0; i_1 < coursesStore.courses.length; ++i_1) {
        console.log(coursesStore.courses[i_1].units[0])
        for (const unit_1 of coursesStore.courses[i_1].units) {
            console.log(unit_1)
            if (unit_1.class_groups[0].dates[0].name != 'Wykład') {
            for (const group_1 of unit_1.class_groups) {
                id_2 = 0;
                for (let i_2 = 0; i_2 < coursesStore.courses.length; ++i_2) {
                    for (const unit_2 of coursesStore.courses[i_2].units) if (unit_2.class_groups[0].dates[0].name != 'Wykład') {
                        for (const group_2 of unit_2.class_groups) {
                            if (id_1 != id_2) {
                                for (const date_1 of group_1.dates) {
                                    for (const date_2 of group_2.dates) {
                                        let beg_mn = Math.min(date_1.start_time, date_2.start_time)
                                        let beg_mx = Math.max(date_1.start_time, date_2.start_time)
                                        let end_mn = Math.min(date_1.end_time, date_2.end_time)
                                        let end_mx = Math.max(date_1.end_time, date_2.end_time)
                                        if (beg_mn == beg_mx && end_mn == end_mx ||
                                            beg_mn < end_mx && end_mn < beg_mx) {
                                            collisions[id_1][id_2]++;
                                        }
                                    }
                                }
                            }
                            id_2++
                        }
                    }
                }
                id_1++;
            }
            }
        }
    }
    // algorytm
    let best = 100000000, candidate = -1;
    for (let i = 0; i < n_possibilities; ++i) {
        let mask = []
        let tmp = i, prefix_sum = 0
        console.log('przed')
        console.log(tmp)
        for (let j = 0; j < n_valid_groups.length; ++j) if (n_valid_groups[j] != 0) {
            mask.push(tmp % n_valid_groups[j] + prefix_sum)
            tmp = Math.floor(tmp / n_valid_groups[j])
            prefix_sum += n_valid_groups[j]
        }
        let n_collisions = 0
        for (let j = 0; j < mask.length; ++j) {
            for (let k = 0; k < mask.length; ++k) {
                if (j != k) {
                    //n_collisions += collisions[j][k];
                }
            }
        }
        console.log('mask')
        console.log(mask[0])
        console.log(mask[1])
        if (n_collisions == 0) {
            let potential = 0
            const min_max = new Map()
            prefix_sum = 0
            let ctr = 0
            console.log('mask length')
            console.log(mask.length)
            for (let j = 0; j < mask.length; ++j) {
                let group_id = mask[j] - prefix_sum
                console.log('group id')
                console.log(group_id)
                for (const unit of coursesStore.courses[j].units) if (unit.class_groups[0].dates[0].name != 'Wykład') {
                    for (const group of unit.class_groups) {
                        if (group_id == ctr) for (const date of group.dates) {
                            let key = date.start_time.substr(0, date.start_time.indexOf(" "))
                            if (!min_max.has(key)) {
                                min_max.set(key, {
                                    min: 10000000,
                                    max: 0
                                })
                            }
                            let current = min_max.get(key)
                            min_max.set(key, {
                                min: Math.min(current.min, (new Date(date.start_time)).getHours() * 60 + (new Date(date.start_time)).getMinutes()),
                                max: Math.max(current.max, (new Date(date.end_time)).getHours() * 60 + (new Date(date.end_time)).getMinutes())
                            })
                        }
                        ++ctr;
                    }
                }
                prefix_sum += n_valid_groups[j];
            }
            for (const [key, value] of min_max) {
                console.log(value)
                potential += value.max - value.min;
            }
            console.log(potential)
            if (potential < best) {
                best = potential
                candidate = i
            }
        }
    }
    console.log('candidate')
    console.log(candidate)
    let events = []
    if (candidate >= 0) {
    let mask = []
    for (let j = 0; j < n_valid_groups.length; ++j) {
        mask.push(candidate % n_valid_groups[j])
        candidate = Math.floor(candidate / n_valid_groups[j])
    }
    console.log('mask after')
    console.log(mask[0])
    console.log(mask[1])
    let ctr = 0, next_id = 0
    let scheduleObj = document.getElementById('Schedule').ej2_instances[0]
    for (let j = 0; j < mask.length; ++j) {
        console.log(j)
        console.log(coursesStore.courses[j].units[1].class_groups[0].dates[0].name.pl)
        for (const unit of coursesStore.courses[j].units) if (unit.class_groups[0].dates[0].name.pl != 'Wykład') {
            ctr = 0
            for (const group of unit.class_groups) {
                if (mask[j] == ctr) for (const date of group.dates) {
                    scheduleObj.addEvent({
                        Id: next_id++,
                        OwnerId: j,
                        EventType: 'Confirmed',
                        Subject: coursesStore.courses[j].course_name.pl + " " + date.name.pl,
                        StartTime: new Date(date.start_time),
                        EndTime: new Date(date.end_time)
                    })
                    console.log(j)
                }
                ++ctr;
            }
        }
    }
    }
    console.log(this.eventSettings.dataSource)
}
</script>

<style>
  @import '../../node_modules/@syncfusion/ej2-base/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-buttons/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-calendars/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-dropdowns/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-inputs/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-navigations/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-popups/styles/material.css';
  @import '../../node_modules/@syncfusion/ej2-vue-schedule/styles/material.css';
</style>