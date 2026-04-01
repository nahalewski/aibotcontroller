import React, { useState } from 'react';

const ModelSetup: React.FC = () => {
    const [provider, setProvider] = useState('openai');
    const [apiKey, setApiKey] = useState('');
    const [baseUrl, setBaseUrl] = useState('https://api.openai.com/v1');
    const [model, setModel] = useState('gpt-4o');
    const [prompt, setPrompt] = useState('You are GamePilot AI...');

    const saveConfig = () => {
        // Save to local storage or backend
        localStorage.setItem('gp_model_config', JSON.stringify({
            provider, apiKey, baseUrl, model, prompt
        }));
        alert('Model Configuration Persisted');
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <header>
                <h1>AI Directives</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Configure the brains behind GamePilot AI.</p>
            </header>

            <div className="grid">
                <div className="panel" style={{ flex: 1 }}>
                    <span className="label">Inference Provider</span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
                        <div>
                            <span className="label">Service Pipeline</span>
                            <select value={provider} onChange={(e) => setProvider(e.target.value)}>
                                <option value="openai">OpenAI (GPT-4o)</option>
                                <option value="local">Local Inference (Ollama/LM Studio)</option>
                                <option value="custom">Custom Endpoint</option>
                            </select>
                        </div>
                        <div>
                            <span className="label">Endpoint URL</span>
                            <input type="text" value={baseUrl} onChange={(e) => setBaseUrl(e.target.value)} />
                        </div>
                        <div>
                            <span className="label">Private Key / Auth</span>
                            <input type="password" placeholder="sk-..." value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
                        </div>
                        <button onClick={saveConfig} style={{ width: '100%' }}>Secure and Save</button>
                    </div>
                </div>

                <div className="panel" style={{ flex: 2 }}>
                    <span className="label">System Behavioral Directives</span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%' }}>
                        <textarea 
                            style={{ 
                                flex: 1, minHeight: '300px', background: 'rgba(0,0,0,0.2)', 
                                border: '1px solid var(--panel-border)', color: 'white', 
                                padding: '1rem', borderRadius: '6px', fontSize: '0.9rem',
                                resize: 'none'
                            }}
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                        <span className="label">Define the tactical scope and safety rules for the AI.</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModelSetup;
