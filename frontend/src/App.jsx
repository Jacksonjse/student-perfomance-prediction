import React, { useState } from "react";
import "./styles.css";

const App = () => {
  const [formData, setFormData] = useState({
    weekly_self_study_hours: "",
    attendance_percentage: "",
    class_participation: "",
    total_score: "",
  });

  const [result, setResult] = useState(null);
  const [probability, setProbability] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Use environment variable or Render backend URL
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setProbability(null);

    try {
      console.log("API Base URL:", API_BASE_URL);
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          weekly_self_study_hours: parseFloat(formData.weekly_self_study_hours),
          attendance_percentage: parseFloat(formData.attendance_percentage),
          class_participation: parseFloat(formData.class_participation),
          total_score: parseFloat(formData.total_score),
        }),
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();
      setResult(data.prediction);
      setProbability((data.probability * 100).toFixed(2));
    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🎓 Student Performance Predictor</h1>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Weekly Self Study Hours:</label>
          <input
            type="number"
            name="weekly_self_study_hours"
            value={formData.weekly_self_study_hours}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Attendance Percentage:</label>
          <input
            type="number"
            name="attendance_percentage"
            value={formData.attendance_percentage}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Class Participation (1–10):</label>
          <input
            type="number"
            name="class_participation"
            value={formData.class_participation}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Total Score (0–100):</label>
          <input
            type="number"
            name="total_score"
            value={formData.total_score}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && (
        <div className={`result ${result === "pass" ? "pass" : "fail"}`}>
          <h2>Prediction: {result.toUpperCase()}</h2>
          {probability && <p>Confidence: {probability}%</p>}
        </div>
      )}
    </div>
  );
};

export default App;
