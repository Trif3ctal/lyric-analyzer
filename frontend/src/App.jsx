import { useState } from "react";
import "./App.css";

function App() {
    const [fileContent, setFileContent] = useState("");
    const [wordCount, setWordCount] = useState(0);
    const [lineCount, setLineCount] = useState(0);
    const [nouns, setNouns] = useState(0);
    const [isLoading, setIsLoading] = useState(false); // Loading state
    const [message, setMessage] = useState(""); // Success/error message

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setIsLoading(true);
        setMessage("");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setFileContent(data.content);
                setWordCount(data.wordCount);
                setLineCount(data.lineCount);
                setNouns(data.nouns);
                setMessage("File uploaded successfully!");
            } else {
                const errorText = await response.text();
                console.error("Upload failed:", response.status, errorText);
                setMessage("Failed to upload file. Please try again.");
            }
        } catch (error) {
            console.error("Error during upload:", error);
            setMessage("An unexpected error occurred.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <h1>Lyric Analyzer</h1>
            <div className="upload-section">
                <label className="file-input-label">
                    <input type="file" accept=".txt" onChange={handleFileUpload} hidden />
                    Upload a Text File...
                </label>
                {isLoading && <div className="spinner"></div>}
                {message && <div className="message">{message}</div>}
            </div>
            {fileContent && (
                <div className="result-card">
                    <h2>File Content:</h2>
                    <pre>{fileContent}</pre>
                    <h3>Word Count: {wordCount}</h3>
                    <h3>Line Count: {lineCount}</h3>
                    <h3># of Nouns: {nouns}</h3>
                </div>
            )}
        </div>
    );
}

export default App;
