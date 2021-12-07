
import React, { useState, useRef, useEffect } from 'react';
import "./MapViewStyles.scss"

import config from '../assets/mapbox.json'
import mapboxgl, { accessToken } from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';

// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass = require('worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker').default;
const tkn = 'pk.eyJ1Ijoic2FrYmFyIiwiYSI6ImNrd3BpZ3R5dDBkNmwydnM2MGczZWczejMifQ.ogaGLHvGYHqJ8Y8ThXf8yQ';
mapboxgl.accessToken = tkn

const MapView = () => {

    const mapContainer = useRef(null);
    const [lng, setLng] = useState(-72.526711);
    const [lat, setLat] = useState(42.391155);
    const [zoom, setZoom] = useState(14);

    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [lng, lat],
            zoom: zoom,
        });


        map.on('move', () => {
            setLng(map.getCenter().lng.toFixed(4));
            setLat(map.getCenter().lat.toFixed(4));
            setZoom(map.getZoom().toFixed(2));
        });

    });


    return (
        <div className="mapView">
            <div ref={mapContainer} className="map-container" />
        </div>
    );


}



export default MapView