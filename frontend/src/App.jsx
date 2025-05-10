import { useState, useEffect } from 'react'
import LyricList from './LyricList'
import './App.css'

function App() {
  const [lyrics, setLyrics] = useState([{ "file_name": "file.txt", "content": "Hello World" }])

  useEffect(() => {
    // fetchLyrics() // call the function to fetch lyrics
  }, [])

  const fetchLyrics = async () => {
    const response = await fetch("http://127.0.0.1:5000/lyrics") // GET response to the backend
    const data = await response.json() // turn that response into json
    setLyrics(data.lyrics) // set the lyrics to the json data
    console.log(data.lyrics)
  }

  return (
    <LyricList lyrics={lyrics} /> // pass the lyrics to the LyricList component
  )
}

export default App
