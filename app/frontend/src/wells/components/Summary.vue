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
  <legend>Well Summary
    <div class="float-right">
        <a v-if="show.edit" :href="url" class="hide-for-print">
          <button class="btn btn-primary mb-1">Edit</button>
        </a>
        <a v-if="analytics" onclick="ga('send', 'event', 'Button', 'print', 'Wells Summary Print'); window.print();">
          <span title="Print" class="fas fa-print fa-pull-right button hide-for-print cursor-pointer print-button"></span>
        </a>
        <a v-else onclick="window.print();">
          <span title="Print" class="fas fa-print fa-pull-right button hide-for-print cursor-pointer print-button"></span>
        </a>
    </div>
  </legend>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    analytics () {
      return !!window.ga
    },
    show () {
      return {
        edit: !!this.config && this.userRoles.wells.edit === true
      }
    },
    url () {
      return '/gwells/submissions/' + this.wellTag + '/edit'
    },
    wellTag () {
      const wellMeta = document.head.querySelector('meta[name="well.tag_number"]')
      if (wellMeta) {
        return wellMeta.content
      }
      return null
    },
    ...mapGetters(['userRoles', 'config'])
  }
}
</script>

<style>

</style>
