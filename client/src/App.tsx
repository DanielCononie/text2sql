import { useState } from "react"
// import type { SqlResponse } from "./types/SqlResponse";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from "@mui/material";

function App() {

  const [question, setQuestion] = useState("")
  const [sqlResponse, setSqlResponse] = useState<any>()
  
  const sendQuestion = async () => {

    if (!question.trim()) {
      return;
    }

    const response = await fetch("http://localhost:8000/generate-sql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    })
    const data = await response.json()

    console.log(data)
    setSqlResponse(data);

    return;
  }

  return (
    <>
      <Box
      component="form"
      sx={{ '& > :not(style)': { m: 1, width: '25ch' } }}
      noValidate
      autoComplete="off"
    >
      <TextField id="outlined-basic" label="Outlined" variant="outlined" onChange={(e) => { setQuestion(e?.target?.value)
        
      }}/>
    </Box>

    <Button onClick={sendQuestion}>Send Question</Button>

    <Box>
      <pre>{JSON.stringify(sqlResponse, null, 2)}</pre>
    </Box>
    </>
  )
}

export default App
