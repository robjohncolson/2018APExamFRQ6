import React, { useState } from 'react';

const APStatLearningFlow = () => {
  const [currentStep, setCurrentStep] = useState(0);
  
  const steps = [
    {
      title: "1. Set Up",
      icon: "📝",
      content: "Grab your materials: pencil, paper, calculator, formula sheet, laptop, and headphones (optional)",
      tips: ["Find a quiet place to focus", "Make sure your laptop is charged"]
    },
    {
      title: "2. Prepare Grok",
      icon: "🤖",
      content: "Open Grok and set up the AI tutor for your specific video",
      tips: ["Copy the provided AP Statistics tutor prompt", "Start a new conversation in Grok"]
    },
    {
      title: "3. Watch Video",
      icon: "📺",
      content: "Actively watch the video (starting with the lowest topic number)",
      tips: ["Take notes on paper", "Work through every example shown"]
    },
    {
      title: "4. Ask Questions",
      icon: "❓",
      content: "If you get confused during the video, pause and ask Grok for help",
      tips: ["Be specific about what confused you", "Return to the video once you understand"]
    },
    {
      title: "5. Practice Problems",
      icon: "🧩",
      content: "After the video, use Grok to work through the practice problems",
      tips: ["Start with multiple choice", "Let Grok guide you through free response questions"]
    }
  ];
  
  const handlePrev = () => {
    setCurrentStep(prev => Math.max(0, prev - 1));
  };
  
  const handleNext = () => {
    setCurrentStep(prev => Math.min(steps.length - 1, prev + 1));
  };

  return (
    <div className="flex flex-col bg-gray-50 p-4 rounded-lg max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-center mb-6">AP Statistics: Using Grok to Help You Learn</h1>
      
      {/* Progress Tracker */}
      <div className="flex justify-between mb-8">
        {steps.map((step, idx) => (
          <div 
            key={idx} 
            className={`flex flex-col items-center cursor-pointer ${idx <= currentStep ? 'text-blue-600' : 'text-gray-400'}`}
            onClick={() => setCurrentStep(idx)}
          >
            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-xl mb-2 ${idx <= currentStep ? 'bg-blue-100' : 'bg-gray-200'}`}>
              {step.icon}
            </div>
            <div className="text-xs font-medium text-center w-20">{step.title}</div>
          </div>
        ))}
      </div>
      
      {/* Step Content */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-bold mb-4">{steps[currentStep].title}</h2>
        <p className="mb-4">{steps[currentStep].content}</p>
        
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-bold text-blue-800 mb-2">Pro Tips:</h3>
          <ul className="list-disc pl-5">
            {steps[currentStep].tips.map((tip, idx) => (
              <li key={idx} className="mb-1">{tip}</li>
            ))}
          </ul>
        </div>
      </div>
      
      {/* Materials List (visible on all screens) */}
      <div className="bg-white p-4 rounded-lg shadow-md mb-6">
        <h3 className="font-bold mb-2">Materials Needed:</h3>
        <div className="grid grid-cols-3 gap-2">
          <div className="flex items-center"><span className="mr-2">📄</span> Paper</div>
          <div className="flex items-center"><span className="mr-2">✏️</span> Pencil</div>
          <div className="flex items-center"><span className="mr-2">🧮</span> Calculator</div>
          <div className="flex items-center"><span className="mr-2">💻</span> Laptop</div>
          <div className="flex items-center"><span className="mr-2">🎧</span> Headphones (optional)</div>
          <div className="flex items-center"><span className="mr-2">📋</span> Clipboard</div>
          <div className="flex items-center"><span className="mr-2">📑</span> AP Exam Formula Sheet</div>
        </div>
      </div>
      
      {/* Navigation Buttons */}
      <div className="flex justify-between">
        <button 
          onClick={handlePrev} 
          className={`px-4 py-2 rounded-lg ${currentStep === 0 ? 'bg-gray-200 text-gray-500' : 'bg-blue-500 text-white'}`}
          disabled={currentStep === 0}
        >
          Previous Step
        </button>
        <button 
          onClick={handleNext} 
          className={`px-4 py-2 rounded-lg ${currentStep === steps.length - 1 ? 'bg-gray-200 text-gray-500' : 'bg-blue-500 text-white'}`}
          disabled={currentStep === steps.length - 1}
        >
          Next Step
        </button>
      </div>
    </div>
  );
};

export default APStatLearningFlow;
