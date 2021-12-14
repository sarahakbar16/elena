import "./OverlayViewStyles.scss"

import React, { useState, useRef, useEffect } from 'react'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import postGetPath from "../controller/APIManager"
import MapboxAutocomplete from 'react-mapbox-autocomplete';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';


import FormControlLabel from '@mui/material/FormControlLabel';
import { blue } from '@mui/material/colors';



const tkn = 'pk.eyJ1Ijoic2FrYmFyIiwiYSI6ImNrd3BpZ3R5dDBkNmwydnM2MGczZWczejMifQ.ogaGLHvGYHqJ8Y8ThXf8yQ';


/**
 * Creates the component for the overlay. 
 * @param {*} param0 
 * @returns 
 */
const OverlayView = ({ setMyPath }) => {

    const [validData, setValidData] = useState(false)

    const [sourceLat, setSourceLat] = useState("")
    const [sourceLng, setSourceLng] = useState("")


    const [destLat, setDestLat] = useState("")
    const [destLng, setDestLng] = useState("")

    const [x, setX] = useState("")

    const [minMax, setMinMax] = useState("")
    const [algorithm, setAlgorithm] = useState("")

    const [error, setError] = useState()

    const handleAlgorithmChange = (event) => {
        setAlgorithm(event.target.value);
    }

    const handleMinMaxChange = (event) => {
        setMinMax(event.target.value);
    }

    const [pathStats, setPathStats] = useState()

    const setThisPath = (path) => {
        setMyPath(path)
    }

    const onChangeSource = (result, lat, lng, text) => {
        setSourceLat(lat)
        setSourceLng(lng)
    }

    const onChangeDest = (result, lat, lng, text) => {
        setDestLat(lat)
        setDestLng(lng)
    }

    const onChangeX = (e) => {
        setX(e.target.value)
    }


    useEffect(() => {
        if (sourceLat !== "" && sourceLng !== "" && destLat !== "" && destLng !== "" && x !== "" && minMax !== "" && algorithm !== "") {
            setValidData(true)
        }
    }, [sourceLat, sourceLng, destLat, destLng, x, minMax, algorithm])

    useEffect(() => {
        console.log("An error was found!")
    }, [error])



    const onClickButton = async () => {
        let data = {
            "source_coords_lat": sourceLat,
            "source_coords_long": sourceLng,
            "destination_coords_lat": destLat,
            "destinations_coords_long": destLng,
            "is_elevation_max": minMax,
            "percentage": x,
            "algorithm": algorithm
        }
        let path = await postGetPath(JSON.stringify(data)) //Sends the data to the controller 

        setPathStats(path)
        setThisPath(path)

    }


    const label = { inputProps: { 'aria-label': 'Switch demo' } };

    return <div> <div className="overlayView">

        <div className="input">
            <div className="inputText">Source: </div>

            <MapboxAutocomplete publicKey={tkn}
                inputClass='form-control search'
                onSuggestionSelect={onChangeSource}
                country='us'
                resetSearch={false}
            />

        </div>


        <div className="input">
            <div className="inputText">Destination: </div>
            <MapboxAutocomplete publicKey={tkn}
                inputClass='form-control search'
                onSuggestionSelect={onChangeDest}
                country='us'
                resetSearch={false}
            />
        </div>

        <TextField variant="standard" inputProps={{ sx: { color: 'white' } }} id="x" label="x%" onChange={onChangeX} />

        <div className="title">Elevation Gain:</div>

        <RadioGroup
            aria-label="minmax"
            name="controlled-radio-buttons-group"
            value={minMax}
            onChange={handleMinMaxChange}
            style={{ color: "white" }}
        >
            <FormControlLabel value={false} control={<Radio sx={{
                color: blue[50],
                '&.Mui-checked': {
                    color: blue[50],
                },
            }} />} label="Minimize" />
            <FormControlLabel value={true} control={<Radio sx={{
                color: blue[50],
                '&.Mui-checked': {
                    color: blue[50],
                },
            }} />} label="Maximize" />
        </RadioGroup>


        <div className="title">Algorithm:</div>

        <RadioGroup
            aria-label="algorithm"
            name="controlled-radio-buttons-group"
            value={algorithm}
            onChange={handleAlgorithmChange}
            style={{ color: "white" }}
        >
            <FormControlLabel value="a*" control={<Radio sx={{
                color: blue[50],
                '&.Mui-checked': {
                    color: blue[50],
                },
            }} />} label="A*" />
            <FormControlLabel value="dijk" control={<Radio sx={{
                color: blue[50],
                '&.Mui-checked': {
                    color: blue[50],
                },
            }} />} label="Dijkstra's" />
        </RadioGroup>




        <Button variant="contained" disabled={!validData} onClick={onClickButton}>Search</Button>

    </div>

        {pathStats && pathStats.shortest_dist && pathStats.shortest_gain && pathStats.elevation_dist && pathStats.elevation_gain &&
            <div className="stats-bar">
                <div className="stats">

                    <div className="title">
                        Total Distance for Shortest Route (Black):
                    </div>

                    <div className="item">
                        {pathStats.shortest_dist.toFixed(2)}m
                    </div>

                    <div className="title">
                        Elevation Gain :
                    </div>
                    <div className="item">
                        {pathStats.shortest_gain}m
                    </div>

                    <div className="title">
                        Total Distance for Elevation Route (Green):
                    </div>
                    <div className="item">
                        {pathStats.elevation_dist.toFixed(2)}m
                    </div>

                    <div className="title">
                        Elevation Gain:
                    </div>
                    <div className="item">
                        {pathStats.elevation_gain}m
                    </div>

                </div>
            </div>
        }



    </div >


}

export default OverlayView