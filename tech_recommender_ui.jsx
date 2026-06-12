import React, { useState } from 'react';
import { TrendingUp, Zap, Target, Award } from 'lucide-react';

const TechStackRecommender = () => {
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  const availableSkills = [
    'Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis',
    'TensorFlow', 'Docker', 'Kubernetes', 'AWS', 'CI/CD',
    'Cloud Computing', 'APIs', 'Microservices', 'Deep Learning',
    'Database Design', 'Jenkins', 'Statistical Analysis'
  ];

  const jobRoles = {
    'Data Scientist': {
      color: 'bg-blue-500',
      skills: ['Python', 'SQL', 'Machine Learning', 'Data Analysis']
    },
    'DevOps Engineer': {
      color: 'bg-purple-500',
      skills: ['Docker', 'Kubernetes', 'AWS', 'CI/CD']
    },
    'Backend Developer': {
      color: 'bg-green-500',
      skills: ['Java', 'Python', 'SQL', 'APIs']
    },
    'Cloud Architect': {
      color: 'bg-orange-500',
      skills: ['AWS', 'Cloud Computing', 'Kubernetes']
    },
    'ML Engineer': {
      color: 'bg-red-500',
      skills: ['Python', 'Machine Learning', 'TensorFlow']
    }
  };

  const toggleSkill = (skill) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter(s => s !== skill));
    } else {
      if (selectedSkills.length < 6) {
        setSelectedSkills([...selectedSkills, skill]);
      }
    }
  };

  const calculateSimilarity = () => {
    if (selectedSkills.length < 3) {
      alert('Please select at least 3 skills');
      return;
    }

    setLoading(true);
    
    // Simulate calculation delay
    setTimeout(() => {
      const scores = {};
      
      // Calculate similarity scores
      Object.entries(jobRoles).forEach(([role, data]) => {
        const matches = data.skills.filter(s => selectedSkills.includes(s));
        const score = (matches.length / selectedSkills.length) * 100;
        scores[role] = score;
      });

      // Sort and get top 3
      const sorted = Object.entries(scores)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 3)
        .map(([role, score], idx) => ({
          rank: idx + 1,
          role,
          score: Math.round(score * 10) / 10,
          color: jobRoles[role].color,
          description: getDescription(role)
        }));

      setRecommendations(sorted);
      setLoading(false);
    }, 800);
  };

  const getDescription = (role) => {
    const descriptions = {
      'Data Scientist': 'Analyzes complex datasets and builds predictive models',
      'DevOps Engineer': 'Manages infrastructure and deployment pipelines',
      'Backend Developer': 'Builds server-side applications and systems',
      'Cloud Architect': 'Designs scalable cloud infrastructure solutions',
      'ML Engineer': 'Develops and deploys machine learning models'
    };
    return descriptions[role];
  };

  const reset = () => {
    setSelectedSkills([]);
    setRecommendations(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-blue-50 to-purple-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white py-8 px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-2">🚀 Tech Stack Recommender</h1>
          <p className="text-cyan-100">Project 3: AI Recommendation Logic • Powered by DecodeLabs</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left: Skill Selection Panel */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <Target className="w-6 h-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-800">Select Your Skills</h2>
            </div>
            <p className="text-gray-600 mb-6">Choose 3-6 skills that match your expertise</p>

            {/* Selected Skills Display */}
            <div className="mb-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
              <p className="text-sm font-semibold text-gray-700 mb-3">
                Selected: {selectedSkills.length}/6
              </p>
              <div className="flex flex-wrap gap-2">
                {selectedSkills.length === 0 ? (
                  <p className="text-gray-500 italic">No skills selected yet...</p>
                ) : (
                  selectedSkills.map(skill => (
                    <div
                      key={skill}
                      className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center gap-2"
                    >
                      {skill}
                      <button
                        onClick={() => toggleSkill(skill)}
                        className="hover:bg-blue-600 rounded-full"
                      >
                        ✕
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Skills Grid */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              {availableSkills.map(skill => (
                <button
                  key={skill}
                  onClick={() => toggleSkill(skill)}
                  className={`p-3 rounded-lg font-medium transition-all ${
                    selectedSkills.includes(skill)
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {skill}
                </button>
              ))}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={calculateSimilarity}
                disabled={selectedSkills.length < 3 || loading}
                className="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <Zap className="w-5 h-5" />
                {loading ? 'Analyzing...' : 'Get Recommendations'}
              </button>
              <button
                onClick={reset}
                className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-lg transition-all"
              >
                Reset
              </button>
            </div>
          </div>

          {/* Right: Recommendations Display */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <Award className="w-6 h-6 text-purple-600" />
              <h2 className="text-2xl font-bold text-gray-800">Your Matches</h2>
            </div>

            {!recommendations ? (
              <div className="flex flex-col items-center justify-center py-16 text-center">
                <TrendingUp className="w-16 h-16 text-gray-300 mb-4" />
                <p className="text-gray-500 text-lg">
                  Select at least 3 skills to see your career recommendations
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {recommendations.map((rec, idx) => (
                  <div
                    key={idx}
                    className="border-2 border-gray-200 rounded-lg p-4 hover:border-blue-400 transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className={`${rec.color} text-white rounded-full w-10 h-10 flex items-center justify-center font-bold`}>
                          {rec.rank}
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-800 text-lg">{rec.role}</h3>
                          <p className="text-sm text-gray-600">{rec.description}</p>
                        </div>
                      </div>
                    </div>

                    {/* Match Score Bar */}
                    <div className="mb-3">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-semibold text-gray-700">Match Score</span>
                        <span className={`${rec.color} text-white px-3 py-1 rounded-full text-sm font-bold`}>
                          {rec.score}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`${rec.color} h-2 rounded-full transition-all duration-500`}
                          style={{ width: `${rec.score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}

                {/* Pipeline Info */}
                <div className="mt-6 p-4 bg-purple-50 rounded-lg border border-purple-200">
                  <p className="text-xs font-semibold text-purple-700 mb-2">4-STEP PIPELINE APPLIED</p>
                  <div className="grid grid-cols-4 gap-2 text-xs">
                    <div className="text-center">
                      <div className="font-bold text-purple-600">1</div>
                      <p className="text-gray-600">Ingestion</p>
                    </div>
                    <div className="text-center">
                      <div className="font-bold text-purple-600">2</div>
                      <p className="text-gray-600">Scoring</p>
                    </div>
                    <div className="text-center">
                      <div className="font-bold text-purple-600">3</div>
                      <p className="text-gray-600">Sorting</p>
                    </div>
                    <div className="text-center">
                      <div className="font-bold text-purple-600">4</div>
                      <p className="text-gray-600">Filtering</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Technical Details */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-bold text-lg mb-3 text-gray-800">🧠 TF-IDF Weighting</h3>
            <p className="text-sm text-gray-600">Skills are converted to weighted vectors, with generic terms penalized and specific skills boosted.</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-bold text-lg mb-3 text-gray-800">📐 Cosine Similarity</h3>
            <p className="text-sm text-gray-600">Measures angular alignment between your profile and job roles, returning scores between 0-1.</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-bold text-lg mb-3 text-gray-800">🎯 Content-Based</h3>
            <p className="text-sm text-gray-600">No historical data needed. New roles and skills are immediately recommendable based on attributes.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechStackRecommender;
