<template>
    <v-btn
        @click="run()"
    >
    Stwórz plan doskonały!
    </v-btn>
    {{ errorMessage }}
    <keep-alive>
        <ejs-schedule ref='scheduleObj' height='500px' width='100%' :selectedDate='selectedDate' 
        :eventSettings='eventSettings' :workHours='workHours'
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
import { provide, ref } from "vue"
import {
  ScheduleComponent as EjsSchedule, ViewsDirective as EViews, ViewDirective as EView,
  ResourcesDirective as EResources, ResourceDirective as EResource,
  Day, Week, WorkWeek, Month, Agenda
} from "@syncfusion/ej2-vue-schedule"
import { registerLicense } from '@syncfusion/ej2-base'

// Registering Syncfusion license key
registerLicense('MjE5Njg1NUAzMjMxMmUzMjJlMzNXZ3prU2hzV2JUSUxKVTFWYzVYcWNYTDYwbVZsMkQ5RjNXa0wvUGY4N1NnPQ==;Mgo+DSMBaFt+QHJqVk1mQ1BbdF9AXnNIfll1QGlZek4BCV5EYF5SRHNdR1xjSntTc0ZrUXg=;Mgo+DSMBMAY9C3t2VFhiQlJPcEBDQmFJfFBmRGNTfFt6dFBWESFaRnZdQV1mS3tSdkZmWXpacHFS;Mgo+DSMBPh8sVXJ1S0R+X1pCaV5dX2NLfUN3RWlaelRwcUU3HVdTRHRcQlhhTH9TdUBjXHtccHM=;MjE5Njg1OUAzMjMxMmUzMjJlMzNQWmlKRDl0VllwYXNteTJrd2UyQ21Ha3hqMU8rQ2ZsRXZQWG02OE1UT0JjPQ==;NRAiBiAaIQQuGjN/V0d+Xk9HfVldXHxLflF1VWJZdV11flVDcC0sT3RfQF5jTHxWd0VgXH9bdHJVQQ==;ORg4AjUWIQA/Gnt2VFhiQlJPcEBDQmFJfFBmRGNTfFt6dFBWESFaRnZdQV1mS3tSdkZmWXpad3NS;MjE5Njg2MkAzMjMxMmUzMjJlMzNoanlPeTlpK1prQ0F4Yk4renU5bW9HMFlDaG9rTkFRRmFFNVRpaEMrenowPQ==;MjE5Njg2M0AzMjMxMmUzMjJlMzNiRTBtMmpDVDRNWnFSQXB4OHh6ZXRwZDZsZzNwaXZieHRsekxOL0RFSTNrPQ==;MjE5Njg2NEAzMjMxMmUzMjJlMzNWbjlqaUxYTFJYUTJJTTF1MEd0eVlMWldSNzN2NnI2MDhoYXBlTVVpTjM0PQ==;MjE5Njg2NUAzMjMxMmUzMjJlMzNuWG9BeWF1dnFCVkYxUVR4cHBQWmxnSGkwRFRJdW9iU2pXZ0JTM3JFQWpJPQ==;MjE5Njg2NkAzMjMxMmUzMjJlMzNXZ3prU2hzV2JUSUxKVTFWYzVYcWNYTDYwbVZsMkQ5RjNXa0wvUGY4N1NnPQ==');

provide('schedule', [Day, Week, WorkWeek, Month, Agenda]);

let selectedDate = new Date() // current date
let workHours = {
    highlight: true,
    start: '08:00',
    end: '19:00'
}
let eventSettings = {
  dataSource: [
  ]
}
const ownerDataSource = [
  { OwnerText: "Nancy", Id: 1, OwnerColor: "#ffaa00" },
  { OwnerText: "Steven", Id: 2, OwnerColor: "#f8a398" },
  { OwnerText: "Michael", Id: 3, OwnerColor: "#7499e1" }
]

const coursesStore = useCoursesStore()

/*
Proxy(Object) {
    course_name: {…}, 
term_id: '2022L', 
course_units_ids: Array(2), 
course_id: '1000-212bMD',
 units: Array(2)}
*/
let errorMessage = ref('')

async function run() {
    errorMessage.value = ''
    let scheduleObj = document.getElementById('Schedule').ej2_instances[0]
    for (let i = 0; i < 10000; ++i) {
        scheduleObj.deleteEvent(i)
    }
    if (coursesStore.courses.length == 0) {
        errorMessage.value = 'Nie wybrano żadnego przedmiotu!'
        return
    }
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
    let collisions = Array(n_groups).fill().map(() => Array(n_groups).fill(0));
    let id_1 = 0, id_2 = 0;
    for (let i_1 = 0; i_1 < coursesStore.courses.length; ++i_1) {
        for (const unit_1 of coursesStore.courses[i_1].units) if (unit_1.class_groups[0].dates[0].name.pl != 'Wykład') {
            for (const group_1 of unit_1.class_groups) {
                id_2 = 0;
                for (let i_2 = 0; i_2 < coursesStore.courses.length; ++i_2) {
                    for (const unit_2 of coursesStore.courses[i_2].units) if (unit_2.class_groups[0].dates[0].name.pl != 'Wykład') {
                        for (const group_2 of unit_2.class_groups) {
                            if (id_1 != id_2) {
                                for (const date_1 of group_1.dates) {
                                    for (const date_2 of group_2.dates) {
                                        let beg_mn = Math.min((new Date(date_1.start_time)).getTime(), (new Date(date_2.start_time)).getTime())
                                        let beg_mx = Math.max((new Date(date_1.start_time)).getTime(), (new Date(date_2.start_time)).getTime())
                                        let end_mn = Math.min((new Date(date_1.end_time)).getTime(), (new Date(date_2.end_time)).getTime())
                                        let end_mx = Math.max((new Date(date_1.end_time)).getTime(), (new Date(date_2.end_time)).getTime())
                                        if (beg_mn == beg_mx && end_mn == end_mx ||
                                            (beg_mn > end_mx || end_mn > beg_mx)) {
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
    // algorytm
    let best = 100000000, candidate = -1;
    for (let i = 0; i < n_possibilities; ++i) {
        let mask = []
        let tmp = i, prefix_sum = 0
        for (let j = 0; j < n_valid_groups.length; ++j) if (n_valid_groups[j] != 0) {
            mask.push(tmp % n_valid_groups[j] + prefix_sum)
            tmp = Math.floor(tmp / n_valid_groups[j])
            prefix_sum += n_valid_groups[j]
        }
        let n_collisions = 0
        for (let j = 0; j < mask.length; ++j) {
            for (let k = 0; k < mask.length; ++k) {
                if (j != k) {
                    n_collisions += collisions[j][k];
                }
            }
        }
        let ok = true, ctr = 0
        for (let j = 0; j < mask.length; ++j) {
            for (const unit of coursesStore.courses[j].units) if (unit.class_groups[0].dates[0].name.pl != 'Wykład') {
                for (const group of unit.class_groups) {
                    console.log(group)
                    if (mask[j] == ctr && group.selected == false) {
                        ok = false
                    }
                    ++ctr
                }
            }
        }
        if (!ok) {
            continue;
        }
        if (n_collisions == 0) {
            let potential = 0
            const min_max = new Map()
            prefix_sum = 0
            ctr = 0
            for (let j = 0; j < mask.length; ++j) {
                let group_id = mask[j] - prefix_sum
                for (const unit of coursesStore.courses[j].units) if (unit.class_groups[0].dates[0].name.pl != 'Wykład') {
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
                potential += value.max - value.min;
            }
            console.log(potential)
            if (potential < best) {
                best = potential
                candidate = i
            }
        }
    }
    if (candidate >= 0) {
        let mask = []
        for (let j = 0; j < n_valid_groups.length; ++j) {
            mask.push(candidate % n_valid_groups[j])
            candidate = Math.floor(candidate / n_valid_groups[j])
        }
        let ctr = 0, next_id = 0
        scheduleObj = document.getElementById('Schedule').ej2_instances[0]
        for (let j = 0; j < mask.length; ++j) {
            for (const unit of coursesStore.courses[j].units) {
                ctr = 0
                for (const group of unit.class_groups) {
                    if (mask[j] == ctr || unit.class_groups[0].dates[0].name.pl == 'Wykład') for (const date of group.dates) {
                        scheduleObj.addEvent({
                            Id: next_id++,
                            OwnerId: j,
                            EventType: 'Confirmed',
                            Subject: coursesStore.courses[j].course_name.pl + " " + date.name.pl + " " + group.number,
                            StartTime: new Date(date.start_time),
                            EndTime: new Date(date.end_time)
                        })
                    }
                    ++ctr;
                }
            }
        }
    } else {
        errorMessage.value = 'Brak planu idealnego:('
    }
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