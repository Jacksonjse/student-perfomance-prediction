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
  const [loading, setLoading] = useState(false);

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

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setResult(data.prediction);
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
          <label htmlFor="weekly_self_study_hours">
            Weekly Self Study Hours:
          </label>
          <input
            type="number"
            id="weekly_self_study_hours"
            name="weekly_self_study_hours"
            value={formData.weekly_self_study_hours}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="attendance_percentage">Attendance Percentage:</label>
          <input
            type="number"
            id="attendance_percentage"
            name="attendance_percentage"
            value={formData.attendance_percentage}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="class_participation">
            Class Participation (1–10):
          </label>
          <input
            type="number"
            id="class_participation"
            name="class_participation"
            value={formData.class_participation}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="total_score">Total Score (0–100):</label>
          <input
            type="number"
            id="total_score"
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
        <div className={`result ${result === "Pass" ? "pass" : "fail"}`}>
          <h2>Prediction: {result}</h2>
        </div>
      )}
    </div>
  );
};

export default App;
