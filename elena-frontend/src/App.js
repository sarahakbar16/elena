import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import MapView from "./view/MapView"
import OverlayView from "./view/OverlayView"


/**
 * Function to run the entire application 
 */
function App() {

  //Keeps track of the path the map needs to display
  const [p, setP] = useState({})

  /**
   * Sets the path for the map to display
   * @param {} my_path 
   */
  const setPath = (my_path) => {
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
