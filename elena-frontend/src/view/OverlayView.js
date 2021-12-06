import React, { useState, useRef, useEffect } from 'react'
import Button from '@mui/material/Button'
import postGetPath from "../controller/APIManager"


const OverlayView = () => {

    const dummyData = {
        "source_coords_lat": 125.6,
        "source_coords_long": 45.9,
        "destination_coords_lat": 82.9,
        "destinations_coords_long": 45.2,
        "is_elevation_max": "True",
        "percentage": "50",
        "algorithm": "dijk"
    }


    const onClickButton = () => {
        postGetPath(JSON.stringify(dummyData))
    }

    return <div className="overlayView">
        <Button variant="contained" onClick={onClickButton}>Click</Button>
    </div>


}

export default OverlayView