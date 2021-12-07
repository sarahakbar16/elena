import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import MapView from "./view/MapView"
import OverlayView from "./view/OverlayView"

function App() {
  const [p, setP] = useState({})

  const setPath = (my_path) => {
    console.log("MY PATH BE", my_path)
    setP(my_path)
  }

  return (
    <div className="App">
      <MapView path={p} />
      <OverlayView setMyPath={setPath} />
    </div>
  )
}

export default App;
