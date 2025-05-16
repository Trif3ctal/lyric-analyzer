import { useState } from "react";
import "./App.css";

function App() {
    const [fileContent, setFileContent] = useState("");
    const [userLyrics, setUserLyrics] = useState("");
    const [wordCount, setWordCount] = useState(0);
    const [lineCount, setLineCount] = useState(0);
    const [nouns, setNouns] = useState(0);
    const [verbs, setVerbs] = useState(0);
    const [rhymes_last, setRhymesLast] = useState("");
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
                setVerbs(data.verbs);
                setRhymesLast(data.rhymes_last);
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

    const handleAnalyzeText = async (e) => {
        if (!userLyrics.trim()) {
            setMessage("Please enter lyrics.");
            return;
        }
        setIsLoading(true);
        setMessage("");
        try {
            const response = await fetch("http://127.0.0.1:5000/user-submit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: userLyrics }),
            });

            if (response.ok) {
                const data = await response.json();
                setFileContent(data.content);
                setWordCount(data.wordCount);
                setLineCount(data.lineCount);
                setNouns(data.nouns);
                setVerbs(data.verbs);
                setRhymesLast(data.rhymes_last);
                setMessage("Text analyzed successfully!");
            } else {
                const errorText = await response.text();
                console.error("Analysis failed:", response.status, errorText);
                setMessage("Failed to analyze text. Please try again.");
            }
        } catch (error) {
            console.error("Error during analysis:", error);
            setMessage("An unexpected error occurred.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <h1>EmceeEval</h1>
            <div className="upload-section">
                <label className="file-input-label">
                    <input type="file" accept=".txt" onChange={handleFileUpload} hidden />
                    Upload a Text File...
                </label>
                {isLoading && <div className="spinner"></div>}
                {message && <div className="message">{message}</div>}
            </div>
            <div>
                <p className="submit-text"><label for="submitlyrics">Or write your own...</label></p>
                <textarea id="submitlyrics" name="submitlyrics" rows="4" cols="50" 
                placeholder="Type lyrics here..." value={userLyrics} onChange={e => setUserLyrics(e.target.value)}/>
                <button onClick={handleAnalyzeText}>Submit</button>
            </div>
            {fileContent && (
                <div className="result-card">
                    <h2>File Content:</h2>
                    <pre>{fileContent}</pre>
                    <h3>Word Count: {wordCount}</h3>
                    <h3>Line Count: {lineCount}</h3>
                    <details>
                        <summary>Used Nouns...</summary>
                        <p>{nouns}</p>
                    </details>
                    <details>
                        <summary>Used Verbs...</summary>
                        <p>{verbs}</p>
                    </details>
                    <details>
                        <summary>Words that rhyme with your last used word...</summary>
                        <p>{rhymes_last}</p>
                    </details>
                </div>
            )}
        </div>
    );
}

export default App;
