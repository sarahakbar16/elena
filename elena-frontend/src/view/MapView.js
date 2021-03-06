
import React, { useState, useRef, useEffect } from 'react';
import "./MapViewStyles.scss"

import config from '../assets/mapbox.json'
import mapboxgl, { accessToken } from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';
import Alert from '@mui/material/Alert';

// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass = require('worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker').default;
const tkn = 'pk.eyJ1Ijoic2FrYmFyIiwiYSI6ImNrd3BpZ3R5dDBkNmwydnM2MGczZWczejMifQ.ogaGLHvGYHqJ8Y8ThXf8yQ';
mapboxgl.accessToken = tkn

/**
 * Creates component for the Map portion of the application 
 * @param {} path 
 * @returns 
 */
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

    });

    /**
     * This useEffect displays the path and relevant information once it is generated. 
     */
    useEffect(() => {
        if (JSON.stringify(path.path) !== '{}') {

            map.on('load', () => {
                map.addSource('elevation-route', {
                    'type': 'geojson',
                    'data': path.path.elevation_path,
                });

                if (path.path.elevation_path.geometry) {
                    const marker1 = new mapboxgl.Marker({ color: 'black' })
                        .setLngLat(path.path.elevation_path.geometry.coordinates[0])
                        .addTo(map);

                    const marker2 = new mapboxgl.Marker({ color: 'black' })
                        .setLngLat(path.path.elevation_path.geometry.coordinates[path.path.elevation_path.geometry.coordinates.length - 1])
                        .addTo(map);

                }


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
            {(path.path.popup_flag === 0) &&
                <Alert variant="filled"  severity="error">Please enter in a source and/or destination in the range of Amherst, MA. </Alert>

            }
            <div ref={mapContainer} className="map-container" />
        </div>
    );


}



export default MapView