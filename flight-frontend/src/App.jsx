import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import LoginPage from './login'
import  FlightsPage  from './flights'
import PilotsPage from './Pilots'
import PlanesPage from './Planes'
import GatesPage from './Gates'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import CreateFlight from './create-flight'
import UpdateFlight from './update-flight'
import CreatePilot from './create-pilot'
import UpdatePilot from './update-pilot'
import CreatePlane from './create-plane'
import UpdatePlane from './update-plane'

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/flights" element={<FlightsPage />} />
        <Route path="/pilots" element={<PilotsPage />} />
        <Route path="/planes" element={<PlanesPage />} />
        <Route path="/gates" element={<GatesPage />} />
        <Route path="/create-flight" element={<CreateFlight />} />
        <Route path="/update-flight" element={<UpdateFlight />} />
        <Route path="/create-pilot" element={<CreatePilot />} />
        <Route path="/update-pilot" element={<UpdatePilot />} />
        <Route path="/create-plane" element={< CreatePlane />} />
        <Route path="update-plane" element={< UpdatePlane />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
