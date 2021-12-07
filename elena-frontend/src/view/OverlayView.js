import React, { useState, useRef, useEffect } from 'react'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import postGetPath from "../controller/APIManager"
import ButtonGroup from '@mui/material/ButtonGroup'
import Autocomplete from '@mui/material/Autocomplete'
import MapboxAutocomplete from 'react-mapbox-autocomplete';


import "./OverlayViewStyles.scss"

const tkn = 'pk.eyJ1Ijoic2FrYmFyIiwiYSI6ImNrd3BpZ3R5dDBkNmwydnM2MGczZWczejMifQ.ogaGLHvGYHqJ8Y8ThXf8yQ';


const OverlayView = ({ setMyPath }) => {

    const [validData, setValidData] = useState(false)

    const [sourceLat, setSourceLat] = useState("")
    const [sourceLng, setSourceLng] = useState("")


    const [destLat, setDestLat] = useState("")
    const [destLng, setDestLng] = useState("")

    const [x, setX] = useState("")

    const [minMax, setMinMax] = useState("")
    const [algorithm, setAlgorithm] = useState("")

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

    const onClickMaximize = () => {
        setMinMax("True")
    }

    const onClickMinimize = () => {
        setMinMax("False")
    }

    const onClickAStar = () => {
        setAlgorithm("a*")
    }

    const onClickDijkstra = () => {
        setAlgorithm("dijk")
    }

    useEffect(() => {
        if (sourceLat !== "" && sourceLng !== "" && destLat !== "" && destLng !== "" && x !== "" && minMax !== "" && algorithm !== "") {
            setValidData(true)
        }
    }, [sourceLat, sourceLng, destLat, destLng, x, minMax, algorithm])

    const dummyData = {
        "source_coords_lat": 125.6,
        "source_coords_long": 45.9,
        "destination_coords_lat": 82.9,
        "destinations_coords_long": 45.2,
        "is_elevation_max": "True",
        "percentage": "50",
        "algorithm": "dijk"
    }

    const onClickButton = async () => {
        console.log(sourceLat, sourceLng, destLat, destLng, x, minMax, algorithm)
        let data = {
            "source_coords_lat": sourceLat,
            "source_coords_long": sourceLng,
            "destination_coords_lat": destLat,
            "destinations_coords_long": destLng,
            "is_elevation_max": minMax,
            "percentage": x,
            "algorithm": algorithm
        }
        let path = await postGetPath(JSON.stringify(data))
        setThisPath(path)
        
    }



    return <div className="overlayView">
        <MapboxAutocomplete publicKey={tkn}
            inputClass='form-control search'
            onSuggestionSelect={onChangeSource}
            country='us'
            resetSearch={false}
        />
        <MapboxAutocomplete publicKey={tkn}
            inputClass='form-control search'
            onSuggestionSelect={onChangeDest}
            country='us'
            resetSearch={false}
        />
        <TextField id="x" label="x%" variant="standard" onChange={onChangeX} />
        <ButtonGroup variant="text" aria-label="text button group">
            <Button onClick={onClickMinimize}>Minimize Elevation</Button>
            <Button onClick={onClickMaximize}>Maximize Elevation</Button>
        </ButtonGroup>

        <ButtonGroup variant="text" aria-label="text button group">
            <Button onClick={onClickAStar}>A* Algorithm</Button>
            <Button onClick={onClickDijkstra}>Dijkstra's Algorithm</Button>
        </ButtonGroup>
        <Button variant="contained" disabled={!validData} onClick={onClickButton}>Click</Button>
    </div>


}

export default OverlayView