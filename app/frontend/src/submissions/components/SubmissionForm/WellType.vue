/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
    <fieldset>
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Well Class</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-row v-if="isStaffEdit">
        <b-col cols="12" md="3" xl="2">
          <form-input
              id="wellTagNumberStaff"
              label="Well Tag Number"
              type="text"
              :value="$route.params.id"
              disabled
          ></form-input>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
            select
            v-model="wellStatusCodeInput"
            :options="codes.well_status_codes"
            value-field="well_status_code"
            text-field="description"
            label="Well Status"
            placeholder="Select status"
            :errors="errors['well_status']"
            :loaded="fieldsLoaded['well_status']"
            id="wellStatusCodeInput"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4">
          <b-form-group
              id="wellClass"
              label="Class of Well"
              aria-describedby="wellClassInvalidFeedback">
            <b-form-select
                v-model="wellClassInput"
                :options="codes.well_classes"
                value-field="well_class_code"
                text-field="description"
                :state="errors['well_class'] ? false : null">
              <template slot="first">
                <option value="" disabled>Select class</option>
              </template>
            </b-form-select>
            <b-form-invalid-feedback id="wellClassInvalidFeedback">
              <div v-for="(error, index) in errors['well_class']" :key="`wellClass error ${index}`">
                {{ error }}
              </div>
            </b-form-invalid-feedback>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <b-form-group
              id="wellSubclass"
              label="Well Subclass"
              aria-describedby="wellSubclassInvalidFeedback">
            <b-form-select
                v-model="wellSubclassInput"
                :options="subclasses"
                value-field="well_subclass_guid"
                text-field="description"
                :disabled="!subclasses.length"
                :state="errors['well_subclass'] ? false : null">
              <template slot="first">
                <option value="" disabled>Select subclass</option>
              </template>
            </b-form-select>
            <b-form-invalid-feedback id="wellSubclassInvalidFeedback">
              <div v-for="(error, index) in errors['well_subclass']" :key="`wellSubclass error ${index}`">
                {{ error }}
              </div>
            </b-form-invalid-feedback>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
            select
            v-model="intendedWaterUseInput"
            :options="codes.intended_water_uses"
            value-field="intended_water_use_code"
            text-field="description"
            label="Intended Water Use"
            placeholder="Select intended use"
            :errors="errors['intended_water_use']"
            :loaded="fieldsLoaded['intended_water_use']"
            id="intendedWaterUse"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4"  v-if="!isStaffEdit">
          <b-form-group>
            <label>Well Tag Number (if known) <span class="font-weight-bold"></span></label>
            <v-select
              v-model="wellTagNumberInput"
              :disabled="wells === null"
              id="wellTagNumberSelect"
              :filterable="false"
              label="well_tag_number"
              :options="wellTagOptions"
              @search="onWellTagSearch"
              ref="wellTagNumber"
              @search:blur="handleSearchBlur">
              <template slot="no-options">
                  Search by well tag number or owner name
              </template>
              <template slot="option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }} ({{ option.owner_full_name }})
                </div>
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }}
                </div>
              </template>
            </v-select>
            <small id="wellTagNumberSelectHint" class="form-text text-muted">
              *displays a maximum of {{MAX_RESULTS}} results
            </small>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
              id="idPlateNumber"
              label="Well Identification Plate Number"
              type="number"
              v-model="idPlateNumberInput"
              :errors="errors['identification_plate_number']"
              :loaded="fieldsLoaded['identification_plate_number']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
              id="wellPlateAttached"
              label="Where Identification Plate Attached"
              type="text"
              v-model="wellPlateAttachedInput"
              :errors="errors['well_identification_plate_attached']"
              :loaded="fieldsLoaded['well_identification_plate_attached']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="4" v-if="isStaffEdit">
          <form-input
              id="wellPlateAttachedBy"
              label="Identification Plate Attached By"
              type="text"
              v-model="idPlateAttachedByInput"
              :errors="errors['id_plate_attached_by']"
              :loaded="fieldsLoaded['id_plate_attached_by']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row v-if="isStaffEdit">
        <b-col cols="12" md="4">
          <form-input
              id="waterSupplySystem"
              label="Water Supply System Name"
              type="text"
              v-model="waterSupplySystemInput"
              :errors="errors['water_supply_system_name']"
              :loaded="fieldsLoaded['water_supply_system_name']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
              id="waterSupplyWell"
              label="Water Supply Well Name"
              type="text"
              v-model="waterSupplyWellInput"
              :errors="errors['water_supply_system_well_name']"
              :loaded="fieldsLoaded['water_supply_system_well_name']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row v-if="!isStaffEdit">
        <b-col cols="12" md="6">
          <form-input
              id="workStartDateInput"
              type="date"
              label="Start Date of Work *"
              placeholder="YYYY-MM-DD"
              v-model="workStartDateInput"
              :errors="errors.work_start_date"
              :loaded="fieldsLoaded['work_start_date']">
          </form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="workEndDateInput"
              type="date"
              label="End Date of Work *"
              placeholder="YYYY-MM-DD"
              v-model="workEndDateInput"
              :errors="errors.work_end_date"
              :loaded="fieldsLoaded['work_end_date']">
          </form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'

export default {
  mixins: [inputBindingsMixin],
  props: {
    units: String,
    wellTagNumber: null,
    wellStatusCode: String,
    workStartDate: String,
    workEndDate: String,
    personResponsible: Object,
    drillerName: String,
    idPlateNumber: null,
    wellPlateAttached: String,
    idPlateAttachedBy: String,
    wellClass: String,
    intendedWaterUse: String,
    wellSubclass: String,
    drillerSameAsPersonResponsible: Boolean,
    waterSupplySystem: String,
    waterSupplyWell: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      wellTagOptions: [],
      MAX_RESULTS: 50
    }
  },
  computed: {
    subclasses () {
      if (this.codes && this.codes.well_classes && this.wellClass) {
        return this.codes.well_classes.find(x => x.well_class_code === this.wellClass).wellsubclasscode_set
      } else {
        return []
      }
    },
    ...mapGetters(['codes', 'userRoles', 'wells'])
  },
  methods: {
    match (item, search) {
      // On some browsers indexOf is faster than contains and vice versa. The trends seems to be that indexOf is faster
      return (item.owner_full_name != null && item.owner_full_name.toUpperCase().indexOf(search) !== -1) || String(item.well_tag_number).indexOf(search) !== -1
    },
    onWellTagSearch (search, loading) {
      // Only do search if something has been typed.
      this.wellTagOptions = []
      if (search && search.length >= 1 && this.wells) {
        // Save time, by converting to uppercase for search only once.
        search = search.toUpperCase()
        // We iterate manually instead of using .filter in order that we can limit the number
        // of search results, and run faster.
        for (let i = 0; i < this.wells.length && this.wellTagOptions.length < this.MAX_RESULTS; ++i) {
          if (this.match(this.wells[i], search)) {
            this.wellTagOptions.push(this.wells[i])
          }
        }
      }
    },
    handleSearchBlur () {
      if (this.wellTagOptions && this.$refs.wellTagNumber.typeAheadPointer < this.wellTagOptions.length) {
        const target = this.wellTagOptions[this.$refs.wellTagNumber.typeAheadPointer]
        if (target) {
          this.wellTagNumberInput = target.well_tag_number
        }
      }
    }
  },
  watch: {
    wellTagNumber (val) {
      // reset list of people when user finished selecting a person
      this.wellTagOptions = []
    },
    wellClass (val, prev) {
      if (prev !== '') {
        this.wellSubclassInput = ''
      }
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
.v-select i.open-indicator {
  width: 0px;
  visibility: hidden;
}
</style>
