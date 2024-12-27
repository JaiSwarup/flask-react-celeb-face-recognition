import { Toaster } from 'react-hot-toast'
import './App.css'
import WebcamCapture from './components/WebcamCampture'

function App() {

  return (
    <>
      <h1>Which Celeb are you?</h1>
      <WebcamCapture />
      <Toaster />
    </>
  )
}

export default App
