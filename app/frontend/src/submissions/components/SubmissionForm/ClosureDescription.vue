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
        <legend :id="id">Decommission Description</legend>
        <p>Enter depth intervals from the top of the hole to the bottom.</p>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <div class="table-responsive">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Decommission Material</th>
                <th>Observations</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr
                  v-for="(item, index) in closureDescriptionSetData"
                  :key="`closureDescription${index}`"
                  :id="`closureDescription${index}`">

                <td class="input-width-small">
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureFrom${index}`"
                      type="number"
                      v-model="item.start"
                      :errors="getClosureError(index).start"
                      :loaded="getFieldsLoaded(index).start"
                  />
                </td>
                <td class="input-width-small">
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureTo${index}`"
                      v-model="item.end"
                      type="number"
                      :errors="getClosureError(index).end"
                      :loaded="getFieldsLoaded(index).end"
                  />
                </td>
                <td>
                  <form-input
                      group-class="mt-1 mb-0"
                      select
                      :id="`decommissionMaterial${index}`"
                      :options="codes.decommission_materials"
                      text-field="description"
                      value-field="code"
                      placeholder="Select material"
                      value="Select material"
                      v-model="item.material"
                      :errors="getClosureError(index).material"
                      :loaded="getFieldsLoaded(index).material"
                  />
                </td>
                <td>
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureObservations${index}`"
                      v-model="item.observations"
                      :errors="getClosureError(index).observations"
                      :loaded="getFieldsLoaded(index).observations"
                  />
                </td>
                <td class="align-middle">
                  <b-btn size="sm" variant="primary" @click="removeClosureRow(index)" :id="`removeClosureRowButton${index}`"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <b-btn size="sm" variant="primary" @click="addClosureRow" id="addClosureRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
    closureDescriptionSet: {
      type: Array,
      default: () => ([])
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: Object,
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
      closureDescriptionSetData: [],
      pageLoaded: false
    }
  },
  computed: {
    ...mapGetters(['codes']),
    computedClosureDescriptionSet: function () {
      return Object.assign({}, this.closureDescriptionSetData)
    }
  },
  watch: {
    computedClosureDescriptionSet: {
      deep: true,
      handler: function (n, o) {
        let closures = []
        this.closureDescriptionSetData.forEach((d) => {
          if (!Object.values(d).every(x => (x === ''))) {
            closures.push(d)
          }
        })
        if (this.pageLoaded && this.saveDisabled) {
          closures.push(this.emptyObject())
        }
        this.$emit('update:closureDescriptionSet', closures)
      }
    }
  },
  methods: {
    addClosureRow () {
      this.closureDescriptionSetData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        start: '',
        end: '',
        material: '',
        observations: ''
      }
    },
    removeClosureRow (rowNumber) {
      this.closureDescriptionSetData.splice(rowNumber, 1)
    },
    getClosureError (index) {
      if (this.errors && 'decommission_description_set' in this.errors && index in this.errors['decommission_description_set']) {
        return this.errors['decommission_description_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'decommission_description_set' in this.fieldsLoaded && index in this.fieldsLoaded['decommission_description_set']) {
        return this.fieldsLoaded['decommission_description_set'][index]
      }
      return {}
    }
  },
  created () {
    if (!this.closureDescriptionSet.length) {
      for (let i = 0; i < 10; i++) {
        this.addClosureRow()
      }
    } else {
      Object.assign(this.closureDescriptionSetData, this.closureDescriptionSet)
      this.addClosureRow()
    }
  },
  updated () {
    this.pageLoaded = true
  }
}
</script>

<style>

</style>
