<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import 'leaflet-edgebuffer'
import 'leaflet-gesture-handling'
import { tiledMapLayer } from 'esri-leaflet'

import aquiferLayers from '../layers'
import { buildLegendHTML } from '../legend'
import associatedWellsIcon from '../../common/assets/images/wells-associated.svg'
import emsWellsIcon from '../../common/assets/images/wells-ems.svg'

const LEGEND_ASSOCIATED_WELLS = { layerName: 'Wells associated to aquifer', legend: associatedWellsIcon, show: false }
const LEGEND_EMS_WELLS = { layerName: 'EMS wells associated to aquifer', legend: emsWellsIcon, show: false }

export default {
  name: 'SingleAquiferMap',
  props: ['aquifer-id', 'geom', 'wells', 'loading'],
  data () {
    return {
      map: null,
      legendControlContent: null,
      activeLayers: {}
    }
  },
  mounted () {
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    this.$nextTick(function () {
      this.initLeaflet()
      this.initMap()
    })
  },
  destroyed () {
    this.map.remove()
  },
  methods: {
    initLeaflet () {
      // There is a known issue using leaflet with webpack, this is a workaround
      // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png')
      })
    },
    initMap () {
      // Create map, with default centered and zoomed to show entire BC.
      this.map = L.map(this.$el, {
        gestureHandling: true,
        preferCanvas: true,
        minZoom: 4,
        maxZoom: 17
      }).setView([54.5, -126.5], 5)
      L.control.scale().addTo(this.map)
      // Add map layers.
      tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)

      // Aquifer outlines
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
        transparent: true
      }).addTo(this.map)
      const layersControl = L.control.layers(null, aquiferLayers, { collapsed: false })
      layersControl.addTo(this.map)
      const cadastralLayer = aquiferLayers['Cadastral']
      cadastralLayer.addTo(this.map)

      Object.keys(aquiferLayers).forEach((layerName) => {
        const layer = aquiferLayers[layerName]
        this.activeLayers[layerName] = {
          layerName: layer.options.name,
          legend: layer.options.legend,
          show: false
        }
      })
      this.activeLayers[cadastralLayer.options.name].show = true

      // Add non-image tile layer for EMS wells
      this.activeLayers.associatedWells = LEGEND_ASSOCIATED_WELLS
      this.activeLayers.emsWells = LEGEND_EMS_WELLS
      this.activeLayers.associatedWells.show = true
      this.addWellsLayersControl(layersControl)

      this.map.addControl(this.getLegendControl())

      this.canvasRenderer = L.canvas({ padding: 0.1 })

      this.canvasLayer = L.layerGroup()
      this.canvasLayer.addTo(this.map)

      this.updateCanvasLayer()
      if (this.geom) {
        this.zoomToAquifer()
      }

      this.listenForLayerAdd()
      this.listenForLayerRemove()
      this.listenForLayerToggle()

      this.$emit('activeLayers', this.activeLayers)
    },
    addWellsLayersControl (layersControl) {
      const overlaysContainer = layersControl.getContainer().querySelector('.leaflet-control-layers-overlays')

      const layerNames = [ 'associatedWells', 'emsWells' ]

      layerNames.forEach((name) => {
        const checked = this.activeLayers[name].show ? 'checked' : ''
        const wellsLayerControlLabel = document.createElement('label')
        wellsLayerControlLabel.innerHTML =
        '<div>' +
          '<input type="checkbox" class="leaflet-control-layers-selector" ' + checked + '>' +
          '<span> ' + this.activeLayers[name].layerName + '</span>' +
        '</div>'
        const emsWellsCheckbox = wellsLayerControlLabel.querySelector('input')
        emsWellsCheckbox.onchange = (e) => {
          this.activeLayers[name].show = e.currentTarget.checked
          this.updateCanvasLayer()
          this.$emit('activeLayers', this.activeLayers)
        }

        overlaysContainer.appendChild(wellsLayerControlLabel)
      })
    },
    getLegendControl () {
      const self = this
      return new (L.Control.extend({
        options: {
          position: 'bottomright'
        },
        onAdd (map) {
          const container = L.DomUtil.create('div', 'leaflet-control-legend')
          const content = L.DomUtil.create('div', 'leaflet-control-legend-content')
          self.legendControlContent = content
          content.innerHTML = `<div class="m-1">Legend</div>`
          container.appendChild(content)
          return container
        }
      }))()
    },
    listenForLayerToggle () {
      this.$on('activeLayers', (data) => {
        this.legendControlContent.innerHTML = buildLegendHTML(data)
      })
    },
    listenForLayerRemove () {
      this.map.on('overlayremove', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = false
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    listenForLayerAdd () {
      this.map.on('overlayadd', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = true
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    updateCanvasLayer () {
      this.canvasLayer.clearLayers()

      this.addAquiferGeomToCanvasLayer()

      this.addWellsToCanvasLayer()

      if (!this.loading) {
        if (this.aquiferLayer) {
          this.canvasLayer.addLayer(this.aquiferLayer)
        }

        if (this.activeLayers.associatedWells.show) {
          this.canvasLayer.addLayer(this.wellsLayer)
        }

        if (this.activeLayers.emsWells.show) {
          this.canvasLayer.addLayer(this.emsWellsLayer)
        }
      }
    },
    addAquiferGeomToCanvasLayer () {
      if (!this.geom) { return }

      if (this.aquiferLayer) {
        this.aquiferLayer.remove()
      }

      const options = {
        style: {
          color: 'red'
        },
        renderer: this.canvasRenderer
      }
      this.aquiferLayer = L.geoJSON(this.geom, options)
      this.aquiferLayer.bindTooltip(`Aquifer ${this.aquiferId}`, { sticky: true })
    },
    addWellsToCanvasLayer (wells) {
      const defaultCircleMarkerOptions = {
        color: 'black',
        weight: 1,
        fillColor: '#0162fe',
        fillOpacity: 1,
        radius: 3,
        renderer: this.canvasRenderer
      }

      const emsWellCircleMarkerOptions = {
        color: 'black',
        weight: 1,
        fillColor: '#0ca287',
        fillOpacity: 1,
        radius: 3,
        renderer: this.canvasRenderer
      }

      if (this.emsWellsLayer) {
        this.emsWellsLayer.remove()
      }
      if (this.wellsLayer) {
        this.wellsLayer.remove()
      }
      this.emsWellsLayer = L.layerGroup()
      this.wellsLayer = L.layerGroup()

      this.wells.forEach((well) => {
        const { latitude, longitude, ems } = well

        if (!latitude || !longitude) { return } // wells might not have lat / lng

        const hasEmsData = Boolean(ems)

        const options = hasEmsData ? emsWellCircleMarkerOptions : defaultCircleMarkerOptions

        const wellCircleMarker = L.circleMarker(L.latLng(latitude, longitude), options)
        const wellTooltip = [
          `Well Tag Number: ${well.well_tag_number}`,
          well.ems ? `EMS ID: ${well.ems}` : null,
          `Address: ${well.street_address || 'N/A'}`
        ].filter(Boolean)

        wellCircleMarker.bindTooltip(wellTooltip.join('<br>'))

        if (hasEmsData) {
          this.emsWellsLayer.addLayer(wellCircleMarker)
        } else {
          this.wellsLayer.addLayer(wellCircleMarker)
        }
      })
    },
    zoomToAquifer () {
      // Set map view to aquifer
      this.map.fitBounds(this.aquiferLayer.getBounds())
    }
  },
  watch: {
    geom (newGeom, oldGeom) {
      if (oldGeom || newGeom) {
        this.updateCanvasLayer()
        this.zoomToAquifer()
      }
    },
    wells (newWells, oldWells) {
      if (oldWells || newWells) {
        this.updateCanvasLayer()
      }
    },
    loading () {
      this.updateCanvasLayer()
    }
  }
}
</script>
<style>
@import "~leaflet/dist/leaflet.css";
@import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

.map {
  height: 500px;
}

.leaflet-control-legend {
  background-color: white;
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
  border-radius: 0.1em;
}

.leaflet-control-legend li {
  line-height: 20px;
}

.leaflet-control-layers label:last-child {
  margin-bottom: 0;
}
</style>
