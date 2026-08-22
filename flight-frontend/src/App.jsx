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
      </Routes>
    </BrowserRouter>
  )
}

export default App
