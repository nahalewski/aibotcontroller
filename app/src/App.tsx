import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import CaptureSetup from './components/CaptureSetup';
import ModelSetup from './components/ModelSetup';
import InputMapping from './components/InputMapping';
import './index.css';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard />;
      case 'capture': return <CaptureSetup />;
      case 'model': return <ModelSetup />;
      case 'mapping': return <InputMapping />;
      default: return <Dashboard />;
    }
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2 style={{ marginBottom: '2rem', color: 'var(--accent-color)' }}>GamePilot AI</h2>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <button 
            className={activeTab === 'dashboard' ? '' : 'secondary'} 
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={activeTab === 'capture' ? '' : 'secondary'} 
            onClick={() => setActiveTab('capture')}
          >
            Capture Setup
          </button>
          <button 
            className={activeTab === 'model' ? '' : 'secondary'} 
            onClick={() => setActiveTab('model')}
          >
            Model Setup
          </button>
          <button 
            className={activeTab === 'mapping' ? '' : 'secondary'} 
            onClick={() => setActiveTab('mapping')}
          >
            Input Mapping
          </button>
        </nav>
      </aside>
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
};

export default App;
