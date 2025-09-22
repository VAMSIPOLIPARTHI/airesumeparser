import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [resumeData, setResumeData] = useState({
    name: '',
    experience: '',
    education: '',
    skills: ''
  });

  // Handle field changes
  const handleChange = (e) => {
    setResumeData({
      ...resumeData,
      [e.target.name]: e.target.value
    });
  };

  // Handle Enhance with AI
  const handleEnhance = async (section) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/ai-enhance', {
        section,
        content: resumeData[section]
      });
      setResumeData({
        ...resumeData,
        [section]: response.data.enhanced_content
      });
    } catch (error) {
      console.error(error);
    }
  };

  // Handle Save Resume
  const handleSave = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/save-resume', resumeData);
      alert('Resume saved successfully!');
    } catch (error) {
      console.error(error);
    }
  };

  // Handle Download Resume
  const handleDownload = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(resumeData, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "resume.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  // Handle File Upload (mock parse)
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Mock parsing with dummy data
      setResumeData({
        name: "John Doe",
        experience: "3 years at XYZ Corp",
        education: "B.Tech in Computer Science",
        skills: "React, FastAPI, Python"
      });
      alert(`File "${file.name}" uploaded and parsed successfully (mock).`);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto", fontFamily: "sans-serif" }}>
      <h1>Resume Editor</h1>

      <div style={{ marginBottom: "15px" }}>
        <label><strong>Upload Resume (.pdf/.docx):</strong></label><br />
        <input type="file" accept=".pdf,.docx" onChange={handleFileUpload} />
      </div>

      {["name", "experience", "education", "skills"].map((section) => (
        <div key={section} style={{ marginBottom: "15px" }}>
          <label><strong>{section.toUpperCase()}:</strong></label><br />
          <textarea
            name={section}
            value={resumeData[section]}
            onChange={handleChange}
            rows={section === "experience" ? 4 : 2}
            style={{ width: "100%", padding: "8px", fontSize: "14px" }}
          /><br />
          <button onClick={() => handleEnhance(section)}>Enhance with AI</button>
        </div>
      ))}

      <button onClick={handleSave} style={{ marginRight: "10px" }}>Save Resume</button>
      <button onClick={handleDownload}>Download Resume</button>
    </div>
  );
}

export default App;
