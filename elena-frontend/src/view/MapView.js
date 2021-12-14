
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

const MapView = (path) => {

    const mapContainer = useRef(null);
    let map;
    const [lng, setLng] = useState(-72.526711);
    const [lat, setLat] = useState(42.391155);
    const [zoom, setZoom] = useState(15);

    useEffect(() => {
        map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v10',
            center: [lng, lat],
            zoom: zoom,
        });


        /* map.on('move', () => {
            setLng(map.getCenter().lng.toFixed(4));
            setLat(map.getCenter().lat.toFixed(4));
            setZoom(map.getZoom().toFixed(2));
        }); */

    });

    useEffect(() => {
        if (JSON.stringify(path.path) !== '{}') {
            map.on('load', () => {
                map.addSource('elevation-route', {
                    'type': 'geojson',
                    'data': path.path.elevation_path,
                });
                console.log(path.path.elevation_path.geometry.coordinates[0])

                const marker1 = new mapboxgl.Marker({ color: 'black' })
                    .setLngLat(path.path.elevation_path.geometry.coordinates[0])
                    .addTo(map);

                const marker2 = new mapboxgl.Marker({ color: 'black' })
                    .setLngLat(path.path.elevation_path.geometry.coordinates[path.path.elevation_path.geometry.coordinates.length - 1])
                    .addTo(map);

                map.addLayer({
                    'id': 'elevation-route',
                    'type': 'line',
                    'source': 'elevation-route',
                    'properties': {
                        'description': "Ford's Theater",
                        'icon': 'theatre-15'
                    },
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round',
                    },
                    'paint': {
                        'line-color': '#008000',
                        'line-width': 5
                    }
                });

                map.addSource('shortest-route', {
                    'type': 'geojson',
                    'data': path.path.shortest_path,
                });

                map.addLayer({
                    'id': 'shortest-route',
                    'type': 'line',
                    'source': 'shortest-route',
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#000000',
                        'line-width': 5
                    }
                });
            })

        }


    }, [path])




    return (
        <div className="mapView">
            <div ref={mapContainer} className="map-container" />
        </div>
    );


}



export default MapView