import React from 'react'

const LyricList = ({lyrics}) => {
    return <div>
        <h2>Lyrics</h2>
        <table>
            <thead>
                <tr>
                    <th>Filename</th>
                    <th>Lyrics</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {lyrics.map((lyrics) => (
                    <tr key={lyrics.id}>
                        <td>{lyrics.file_name}</td>
                        <td>{lyrics.content}</td>
                        <td>
                            <button>Update</button>
                            <button>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}
export default LyricList