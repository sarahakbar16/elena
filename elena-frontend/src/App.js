import logo from './logo.svg';
import './App.css';
import MapView from "./view/MapView"
import OverlayView from "./view/OverlayView"

function App() {
  return (
    <div className="App">
      <MapView />
      <OverlayView />
    </div>
  )
}

export default App;
