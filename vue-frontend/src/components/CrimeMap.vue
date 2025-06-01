<template>
  <div id="app">
    <header class="header">
      <h1>🛰️ CrimeMap Intelligence Dashboard</h1>
      <div class="toolbar">
        <button @click="switchTile">{{ tileName }}</button>
        <button @click="zoomOut">🌍 Global View</button>
      </div>
    </header>

    <div class="layout">
      <div class="sidebar">
        <div class="mini-map-title">🛰️ Satellite View</div>
        <div id="miniSatelliteMap" class="mini-map"></div>

        <div class="mini-map-title">🚓 Police Response Map</div>
        <div id="miniPoliceMap" class="mini-map"></div>
      </div>

      <div class="main-map" id="mainMap"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet.markercluster'
import 'leaflet/dist/leaflet.css'

const crimes = ref([])
const policeStations = ref([])
const tileName = ref("🗺️ Dark View")
let tileLayer = null
let clusterLayer = null
let mainMap = null
let policeMap = null
let policeLine = null

const dark = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
const satellite = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"

const switchTile = () => {
  const newTile = tileName.value.includes("Dark") ? satellite : dark
  tileName.value = tileName.value.includes("Dark") ? "🛰️ Satellite View" : "🗺️ Dark View"
  if (tileLayer) tileLayer.setUrl(newTile)
}

const zoomOut = () => {
  mainMap.setView([20, 0], 3)
}

const loadCrimes = async () => {
  try {
    const response = await axios.get('http://localhost:8001/api/crimes')
    crimes.value = response.data
    renderMarkers()
  } catch (err) {
    console.error("❌ Failed to load crimes:", err)
  }
}

const renderMarkers = () => {
  if (clusterLayer) mainMap.removeLayer(clusterLayer)
  clusterLayer = L.markerClusterGroup()

  crimes.value.forEach(crime => {
    const marker = L.marker([crime.latitude, crime.longitude])
      .bindPopup(`<b>${crime.category.toUpperCase()}</b><br><strong>${crime.title}</strong><br>${crime.description}`)
      .on('click', () => zoomToNearestPolice(crime.latitude, crime.longitude))
    clusterLayer.addLayer(marker)
  })

  mainMap.addLayer(clusterLayer)
}

const createMap = (id, coords, tile, zoom = 7) => {
  const map = L.map(id, {
    zoomControl: false,
    attributionControl: false
  }).setView(coords, zoom)

  L.tileLayer(tile).addTo(map)
  return map
}

const loadPoliceStations = async (map) => {
  const query = `
    [out:json];
    node["amenity"="police"](6.5,79.8,7.5,81);
    out body;
  `
  try {
    const response = await axios.post("https://overpass-api.de/api/interpreter", query, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    policeStations.value = response.data.elements
    policeStations.value.forEach(station => {
      L.circleMarker([station.lat, station.lon], {
        radius: 5,
        color: "#00ffff",
        fillOpacity: 0.8
      }).bindPopup(`🚓 ${station.tags.name || "Police Station"}`).addTo(map)
    })
  } catch (error) {
    console.error("❌ Police station fetch failed", error)
  }
}

const zoomToNearestPolice = (lat, lon) => {
  if (!policeStations.value.length) return

  let nearest = policeStations.value[0]
  let minDist = Number.MAX_VALUE

  policeStations.value.forEach(station => {
    const dist = Math.sqrt(
      Math.pow(lat - station.lat, 2) +
      Math.pow(lon - station.lon, 2)
    )
    if (dist < minDist) {
      minDist = dist
      nearest = station
    }
  })

  if (nearest) {
    policeMap.setView([nearest.lat, nearest.lon], 14)

    if (policeLine) {
      policeMap.removeLayer(policeLine)
    }

    policeLine = L.polyline([[lat, lon], [nearest.lat, nearest.lon]], {
      color: '#00ff00',
      weight: 3,
      dashArray: '5, 10'
    }).bindPopup(`Distance to nearest police station`).addTo(policeMap)
  }
}

onMounted(() => {
  mainMap = L.map("mainMap", { attributionControl: false })
  tileLayer = L.tileLayer(dark).addTo(mainMap)
  mainMap.setView([6.9271, 79.8612], 7)

  loadCrimes()
  setInterval(loadCrimes, 10000)

  createMap("miniSatelliteMap", [6.0535, 80.2210], satellite, 7)
  policeMap = createMap("miniPoliceMap", [6.9271, 79.8612], dark, 7)
  loadPoliceStations(policeMap)
})
</script>

<style scoped>
#app {
  height: 100vh;
  width: 100vw;
  background-color: #0a0f0f;
  font-family: 'Consolas', monospace;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #0e1f0e;
  color: #39ff14;
  padding: 10px 20px;
  font-size: 18px;
  box-shadow: 0 0 10px #39ff14;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar button {
  margin: 0 6px;
  background: #122;
  border: 1px solid #39ff14;
  color: #aaffaa;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.toolbar button:hover {
  background: #193319;
  box-shadow: 0 0 10px #39ff14;
}

.layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 25%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  background: #0e1e0e;
  padding: 10px;
}

.mini-map-title {
  text-align: center;
  color: #aaffaa;
  font-weight: bold;
  margin: 5px 0;
}

.mini-map {
  height: 48%;
  border: 2px solid #39ff14;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0, 255, 0, 0.2);
}

.main-map {
  flex: 1;
  height: 100%;
}
</style>
