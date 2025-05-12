import { useState, useEffect } from "react";
import "./App.css";

function App() {
    const [fileContent, setFileContent] = useState("");

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            setFileContent(data.content);
        } else {
            const errorText = await response.text(); // Log backend error message
            console.error("Upload failed:", response.status, errorText);
            alert("Failed to upload file. Please check the console for details.");
        }
    };

    return (
        <>
            <div>
                <h1>Upload a Text File</h1>
                <input type="file" accept=".txt" onChange={handleFileUpload} />
                {fileContent && (
                    <div>
                        <h2>File Content:</h2>
                        <pre>{fileContent}</pre>
                    </div>
                )}
            </div>
        </>
    ); // pass lyrics to the LyricList component and display it
}

export default App;
