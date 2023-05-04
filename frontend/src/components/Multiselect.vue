<template>
<div>
  <label class="typo__label" for="ajax">Async multiselect</label>
  <multiselect 
  v-model="selectedCountries" 
  id="ajax" 
  label="name" 
  placeholder="Type to search" 
  open-direction="bottom" 
  :options="countries"
  :multiple="true" 
  :searchable="true" 
  :loading="isLoading" 
  :internal-search="false" 
  :clear-on-select="false" 
  :close-on-select="true" 
  :options-limit="300" :limit="3" 
  :limit-text="limitText" 
  :max-height="600" 
  :show-no-results="false" 
  :hide-selected="true"
  track-by="name" 
  @search-change="asyncFind">
    <template slot="tag" slot-scope="{ option, remove }">
        <span class="custom__tag"><span>{{ option.name }}
        </span>
        <span class="custom__remove" @click="removeOption(option)">❌
        </span>
    </span></template>
    <template slot="clear" slot-scope="props">
      <div class="multiselect__clear" v-if="selectedCountries.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
    </template><span slot="noResult">Oops! No elements found. Consider changing the search query.</span>
  </multiselect>
  <pre class="language-json"><code>{{ selectedCountries  }}</code></pre>
</div>
<button class="btn btn-primary" v-on:click="builder">Stwórz plan doskonały!</button>
  {{ candidate }}
    <DayPilotCalendar id="dp" :config="config" ref="calendar" />
  </template>
  <script>
 import Multiselect from 'vue-multiselect'
 
import {DayPilot, DayPilotCalendar} from '@daypilot/daypilot-lite-vue'
import axios from 'axios'
import { ref } from 'vue'

export default {
  components: {
    Multiselect,
    DayPilotCalendar
  },
  data () {
    return {
      selectedCountries: ref([]),
      countries: [],
      isLoading: false,
      courses_id: [],
      courses_dates: [],
      candidate: -1,
      config: {
        viewType: "Week",
        startDate: "2022-08-01",
      },
    }
  },
  computed: {
    calendar() {
      return this.$refs.calendar.control;
    }
  },
  methods: {
    removeOption(option) {
        console.log("elo")
        let index = selectedCountries.indexOf(option);
        selectedCountries.splice(index, 1);
    },
    limitText (count) {
      return `and ${count} other countries`
    },
    asyncFind (query) {
      this.isLoading = true
      axios
    .get('https://usosapps.uw.edu.pl/services' + '/courses/search', {
      params: {
        lang: 'pl',
        name: query
      }
    })
    .then(response => {
        console.log(response.data.items[0].match)
        let options = []
        for (let i = 0; i < response.data.items.length; i++) {
            options.push({name: response.data.items[i].match});
        }
        this.countries = options;
        this.isLoading = false
      })
    .catch(error => {
      console.log(error)
    })
    },
    async builder() {
        this.courses_id = []
        for (let i = 0; i < this.selectedCountries.length; i++) {
            let n = this.selectedCountries[i].name.split(" ")
            this.courses_id.push(n[n.length - 1].substring(1, n[n.length - 1].length - 1))
        }
        this.courses_dates = []
        let n_possibilities = 1
        for (let i = 0; i < this.courses_id.length; i++) {
            let tmp = []
            await axios
            .get('https://usosapps.uw.edu.pl/services' + '/tt/course_edition', {
                params: {
                    course_id: this.courses_id[i],
                    term_id: '2022L'
                    //1000-212bMD
                }
            })
            .then(response => {
                for (let k = 0; k < response.data.length; ++k) {
                    let flag = false;
                    for (let j = 0; j < k; ++j) {
                        if (response.data[k].name.pl == response.data[j].name.pl) {
                            flag = true;
                        } 
                    }
                    if (flag == false) {
                    let dates = []
                    for (let j = 0; j < response.data.length; ++j) {
                        if (response.data[k].name.pl == response.data[j].name.pl) {
                            let n = response.data[j].start_time.split(" ")
                            let m = response.data[j].end_time.split(" ")
                            const d = new Date(response.data[j].start_time)
                            dates.push({
                                day: d.getDay() - 1,
                                start: n[n.length - 1],
                                end: m[m.length - 1]
                            })
                        }
                    }
                    tmp.push({
                        name: response.data[k].name.pl,
                        dates: dates
                    })
                    console.log(tmp)
                    console.log(tmp.length)
                    }
                }
                this.courses_dates.push(tmp)
                n_possibilities *= tmp.length
            })
            .catch(error => {
                console.log(error)
            })
        }
        // algorytm
        let best = 100000000
        for (let i = 0; i < n_possibilities; ++i) {
            let mask = []
            let tmp = i
            for (let j = 0; j < this.courses_dates.length; ++j) {
                mask.push(tmp % this.courses_dates[j].length)
                tmp = Math.floor(tmp/this.courses_dates[j].length)
            }
            let occupied = []
            for (let j = 0; j < this.courses_dates.length; ++j) {
                console.log(this.courses_dates[j][mask[j]])
                for (let k = 0; k < this.courses_dates[j][mask[j]].dates.length; ++k) {
                    occupied.push(this.courses_dates[j][mask[j]].dates[k])
                }
            }
            let ok = true
            for (let j = 0; j < occupied.length; ++j) {
                for (let k = j + 1; k < occupied.length; ++k) {
                    if (occupied[j].day == occupied[k].day) {
                        let min_date_j = new Date("2022-08-01 " + occupied[j].start)
                        let start_minute_j = min_date_j.getHours() * 60 + min_date_j.getMinutes()
                        let max_date_j = new Date("2022-08-01 " + occupied[j].end)
                        let end_minute_j = max_date_j.getHours() * 60 + max_date_j.getMinutes()
                        let min_date_k = new Date("2022-08-01 " + occupied[k].start)
                        let start_minute_k = min_date_k.getHours() * 60 + min_date_k.getMinutes()
                        let max_date_k = new Date("2022-08-01 " + occupied[k].end)
                        let end_minute_k = max_date_k.getHours() * 60 + max_date_k.getMinutes()
                        let beg_mn = Math.min(start_minute_j, start_minute_k)
                        let beg_mx = Math.max(start_minute_j, start_minute_k)
                        let end_mn = Math.min(end_minute_j, end_minute_k)
                        let end_mx = Math.max(end_minute_j, end_minute_k)
                        console.log(beg_mn + " " + beg_mx + " " + end_mn + " " + end_mx)
                        if (beg_mn == beg_mx && end_mn == end_mx ||
                        beg_mn < end_mx && end_mn < beg_mx) {
                            ok = false
                            break
                        }
                    }
                }
                if (ok == false) {
                    break;
                }
            }
            if (ok == true) {
                // funkcja potencjału
                let ranges = [
                    { min: 10000, max: 0 },
                    { min: 10000, max: 0 },
                    { min: 10000, max: 0 },
                    { min: 10000, max: 0 },
                    { min: 10000, max: 0 }
                ]
                for (let j = 0; j < occupied.length; ++j) {
                    let d = occupied[j].day
                    let min_date = new Date("2022-08-01 " + occupied[j].start)
                    let start_minute = min_date.getHours() * 60 + min_date.getMinutes()
                    let max_date = new Date("2022-08-01 " + occupied[j].end)
                    let end_minute = max_date.getHours() * 60 + max_date.getMinutes()
                    console.log("max" + end_minute)
                    ranges[d].min = Math.min(ranges[d].min, start_minute)
                    ranges[d].max = Math.max(ranges[d].max, end_minute)
                }
                let potential = 0
                for (let j = 0; j < 5; ++j) {
                    if (ranges[j].max != 0) {
                        potential += ranges[j].max - ranges[j].min
                    }
                }
                for (let j = 0; j < occupied.length; ++j) {
                    let min_date = new Date("2022-08-01 " + occupied[j].start)
                    let start_minute = min_date.getHours() * 60 + min_date.getMinutes()
                    let max_date = new Date("2022-08-01 " + occupied[j].end)
                    let end_minute = max_date.getHours() * 60 + max_date.getMinutes()
                    potential -= end_minute - start_minute
                }
                if (potential < best) {
                    best = potential
                    this.candidate = i
                }
            }
        }
        console.log("cand " + this.candidate)
        let next_id = 0
        let mask = []
        for (let j = 0; j < this.courses_dates.length; ++j) {
            mask.push(this.candidate % this.courses_dates[j].length)
            this.candidate = Math.floor(this.candidate/this.courses_dates[j].length)
        }
        const events = []
        for (let j = 0; j < this.courses_dates.length; ++j) {
            for (let k = 0; k < this.courses_dates[j][mask[j]].dates.length; ++k) {
                console.log(this.courses_dates[j][mask[j]].dates[k].start + " " +
                this.courses_dates[j][mask[j]].dates[k].end)
                if (this.courses_dates[j][mask[j]].dates[k].day == 0) {
                events.push({
                    id: next_id++,
                    start: "2022-08-01T" + this.courses_dates[j][mask[j]].dates[k].start,
                    end: "2022-08-01T" + this.courses_dates[j][mask[j]].dates[k].end,
                    text: this.courses_dates[j][mask[j]].name
                })
                } else if (this.courses_dates[j][mask[j]].dates[k].day == 1) {
                events.push({
                    id: next_id++,
                    start: "2022-08-02T" + this.courses_dates[j][mask[j]].dates[k].start,
                    end: "2022-08-02T" + this.courses_dates[j][mask[j]].dates[k].end,
                    text: this.courses_dates[j][mask[j]].name
                })
                } else if (this.courses_dates[j][mask[j]].dates[k].day == 2) {
                events.push({
                    id: next_id++,
                    start: "2022-08-03T" + this.courses_dates[j][mask[j]].dates[k].start,
                    end: "2022-08-03T" + this.courses_dates[j][mask[j]].dates[k].end,
                    text: this.courses_dates[j][mask[j]].name
                })  
                } else if (this.courses_dates[j][mask[j]].dates[k].day == 3) {
                events.push({
                    id: next_id++,
                    start: "2022-08-04T" + this.courses_dates[j][mask[j]].dates[k].start,
                    end: "2022-08-04T" + this.courses_dates[j][mask[j]].dates[k].end,
                    text: this.courses_dates[j][mask[j]].name
                })  
                } else if (this.courses_dates[j][mask[j]].dates[k].day == 4) {
                events.push({
                    id: next_id++,
                    start: "2022-08-05T" + this.courses_dates[j][mask[j]].dates[k].start,
                    end: "2022-08-05T" + this.courses_dates[j][mask[j]].dates[k].end,
                    text: this.courses_dates[j][mask[j]].name
                })  
                } 
                
            }
        }
        this.calendar.update({events});
    }
  }
}
  </script>
 <style>
fieldset[disabled] .multiselect{pointer-events:none}.multiselect__spinner{position:absolute;right:1px;top:1px;width:48px;height:35px;background:#fff;display:block}.multiselect__spinner:after,.multiselect__spinner:before{position:absolute;content:"";top:50%;left:50%;margin:-8px 0 0 -8px;width:16px;height:16px;border-radius:100%;border-color:#41b883 transparent transparent;border-style:solid;border-width:2px;box-shadow:0 0 0 1px transparent}.multiselect__spinner:before{animation:a 2.4s cubic-bezier(.41,.26,.2,.62);animation-iteration-count:infinite}.multiselect__spinner:after{animation:a 2.4s cubic-bezier(.51,.09,.21,.8);animation-iteration-count:infinite}.multiselect__loading-enter-active,.multiselect__loading-leave-active{transition:opacity .4s ease-in-out;opacity:1}.multiselect__loading-enter,.multiselect__loading-leave-active{opacity:0}.multiselect,.multiselect__input,.multiselect__single{font-family:inherit;font-size:16px;-ms-touch-action:manipulation;touch-action:manipulation}.multiselect{box-sizing:content-box;display:block;position:relative;width:100%;min-height:40px;text-align:left;color:#35495e}.multiselect *{box-sizing:border-box}.multiselect:focus{outline:none}.multiselect--disabled{opacity:.6}.multiselect--active{z-index:1}.multiselect--active:not(.multiselect--above) .multiselect__current,.multiselect--active:not(.multiselect--above) .multiselect__input,.multiselect--active:not(.multiselect--above) .multiselect__tags{border-bottom-left-radius:0;border-bottom-right-radius:0}.multiselect--active .multiselect__select{transform:rotate(180deg)}.multiselect--above.multiselect--active .multiselect__current,.multiselect--above.multiselect--active .multiselect__input,.multiselect--above.multiselect--active .multiselect__tags{border-top-left-radius:0;border-top-right-radius:0}.multiselect__input,.multiselect__single{position:relative;display:inline-block;min-height:20px;line-height:20px;border:none;border-radius:5px;background:#fff;padding:0 0 0 5px;width:100%;transition:border .1s ease;box-sizing:border-box;margin-bottom:8px;vertical-align:top}.multiselect__input::-webkit-input-placeholder{color:#35495e}.multiselect__input:-ms-input-placeholder{color:#35495e}.multiselect__input::placeholder{color:#35495e}.multiselect__tag~.multiselect__input,.multiselect__tag~.multiselect__single{width:auto}.multiselect__input:hover,.multiselect__single:hover{border-color:#cfcfcf}.multiselect__input:focus,.multiselect__single:focus{border-color:#a8a8a8;outline:none}.multiselect__single{padding-left:5px;margin-bottom:8px}.multiselect__tags-wrap{display:inline}.multiselect__tags{min-height:40px;display:block;padding:8px 40px 0 8px;border-radius:5px;border:1px solid #e8e8e8;background:#fff;font-size:14px}.multiselect__tag{position:relative;display:inline-block;padding:4px 26px 4px 10px;border-radius:5px;margin-right:10px;color:#fff;line-height:1;background:#41b883;margin-bottom:5px;white-space:nowrap;overflow:hidden;max-width:100%;text-overflow:ellipsis}.multiselect__tag-icon{cursor:pointer;margin-left:7px;position:absolute;right:0;top:0;bottom:0;font-weight:700;font-style:normal;width:22px;text-align:center;line-height:22px;transition:all .2s ease;border-radius:5px}.multiselect__tag-icon:after{content:"\D7";color:#266d4d;font-size:14px}.multiselect__tag-icon:focus,.multiselect__tag-icon:hover{background:#369a6e}.multiselect__tag-icon:focus:after,.multiselect__tag-icon:hover:after{color:#fff}.multiselect__current{min-height:40px;overflow:hidden;padding:8px 12px 0;padding-right:30px;white-space:nowrap;border-radius:5px;border:1px solid #e8e8e8}.multiselect__current,.multiselect__select{line-height:16px;box-sizing:border-box;display:block;margin:0;text-decoration:none;cursor:pointer}.multiselect__select{position:absolute;width:40px;height:38px;right:1px;top:1px;padding:4px 8px;text-align:center;transition:transform .2s ease}.multiselect__select:before{position:relative;right:0;top:65%;color:#999;margin-top:4px;border-style:solid;border-width:5px 5px 0;border-color:#999 transparent transparent;content:""}.multiselect__placeholder{color:#adadad;display:inline-block;margin-bottom:10px;padding-top:2px}.multiselect--active .multiselect__placeholder{display:none}.multiselect__content-wrapper{position:absolute;display:block;background:#fff;width:100%;max-height:240px;overflow:auto;border:1px solid #e8e8e8;border-top:none;border-bottom-left-radius:5px;border-bottom-right-radius:5px;z-index:1;-webkit-overflow-scrolling:touch}.multiselect__content{list-style:none;display:inline-block;padding:0;margin:0;min-width:100%;vertical-align:top}.multiselect--above .multiselect__content-wrapper{bottom:100%;border-bottom-left-radius:0;border-bottom-right-radius:0;border-top-left-radius:5px;border-top-right-radius:5px;border-bottom:none;border-top:1px solid #e8e8e8}.multiselect__content::webkit-scrollbar{display:none}.multiselect__element{display:block}.multiselect__option{display:block;padding:12px;min-height:40px;line-height:16px;text-decoration:none;text-transform:none;vertical-align:middle;position:relative;cursor:pointer;white-space:nowrap}.multiselect__option:after{top:0;right:0;position:absolute;line-height:40px;padding-right:12px;padding-left:20px;font-size:13px}.multiselect__option--highlight{background:#41b883;outline:none;color:#fff}.multiselect__option--highlight:after{content:attr(data-select);background:#41b883;color:#fff}.multiselect__option--selected{background:#f3f3f3;color:#35495e;font-weight:700}.multiselect__option--selected:after{content:attr(data-selected);color:silver}.multiselect__option--selected.multiselect__option--highlight{background:#ff6a6a;color:#fff}.multiselect__option--selected.multiselect__option--highlight:after{background:#ff6a6a;content:attr(data-deselect);color:#fff}.multiselect--disabled{background:#ededed;pointer-events:none}.multiselect--disabled .multiselect__current,.multiselect--disabled .multiselect__select,.multiselect__option--disabled{background:#ededed;color:#a6a6a6}.multiselect__option--disabled{cursor:text;pointer-events:none}.multiselect__option--group{background:#ededed;color:#35495e}.multiselect__option--group.multiselect__option--highlight{background:#35495e;color:#fff}.multiselect__option--group.multiselect__option--highlight:after{background:#35495e}.multiselect__option--disabled.multiselect__option--highlight{background:#dedede}.multiselect__option--group-selected.multiselect__option--highlight{background:#ff6a6a;color:#fff}.multiselect__option--group-selected.multiselect__option--highlight:after{background:#ff6a6a;content:attr(data-deselect);color:#fff}.multiselect-enter-active,.multiselect-leave-active{transition:all .15s ease}.multiselect-enter,.multiselect-leave-active{opacity:0}.multiselect__strong{margin-bottom:8px;line-height:20px;display:inline-block;vertical-align:top}[dir=rtl] .multiselect{text-align:right}[dir=rtl] .multiselect__select{right:auto;left:1px}[dir=rtl] .multiselect__tags{padding:8px 8px 0 40px}[dir=rtl] .multiselect__content{text-align:right}[dir=rtl] .multiselect__option:after{right:auto;left:0}[dir=rtl] .multiselect__clear{right:auto;left:12px}[dir=rtl] .multiselect__spinner{right:auto;left:1px}@keyframes a{0%{transform:rotate(0)}to{transform:rotate(2turn)}}
</style>
