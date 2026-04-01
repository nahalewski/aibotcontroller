import React, { useState, useEffect } from 'react';

const Dashboard: React.FC = () => {
    const [isRunning, setIsRunning] = useState(false);
    const [image, setImage] = useState<string | null>(null);
    const [metrics, setMetrics] = useState({ fps: 0, latency_ms: 0, last_action: 'None' });

    // Mock WebSocket connection for now
    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws');
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'frame_update') {
                setImage(data.image);
                setMetrics(data.metrics);
            }
        };
        return () => socket.close();
    }, []);

    const toggleRuntime = async () => {
        const endpoint = isRunning ? 'stop' : 'start';
        const response = await fetch(`http://localhost:8000/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                provider: 'openai', 
                api_key: 'YOUR_KEY_HERE' // This will come from ModelSetup
            })
        });
        if (response.ok) setIsRunning(!isRunning);
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>Mission Control</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ 
                            width: 10, height: 10, borderRadius: '50%', 
                            background: isRunning ? 'var(--success)' : 'var(--error)' 
                        }} />
                        <span className="label" style={{ marginBottom: 0 }}>
                            {isRunning ? 'System Active' : 'System Offline'}
                        </span>
                    </div>
                    <button onClick={toggleRuntime} className={isRunning ? 'danger' : ''}>
                        {isRunning ? 'Emergency Stop' : 'Initiate Runtime'}
                    </button>
                </div>
            </header>

            <div className="grid">
                <div className="panel" style={{ flex: 2 }}>
                    <span className="label">Live Tactical Stream</span>
                    <div style={{ 
                        width: '100%', aspectRatio: '16/9', background: '#000', 
                        borderRadius: '8px', overflow: 'hidden', display: 'flex', 
                        justifyContent: 'center', alignItems: 'center',
                        border: '1px solid var(--panel-border)'
                    }}>
                        {image ? (
                            <img src={`data:image/jpeg;base64,${image}`} style={{ width: '100%', height: '100%', objectFit: 'contain' }} alt="Capture" />
                        ) : (
                            <span style={{ color: 'var(--text-secondary)' }}>No Frame Data Pipeline</span>
                        )}
                    </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="panel" style={{ flex: 1 }}>
                        <span className="label">Telemetry</span>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                            <div>
                                <h3 style={{ color: 'var(--accent-color)' }}>{metrics.fps}</h3>
                                <span className="label">FPS</span>
                            </div>
                            <div>
                                <h3 style={{ color: 'var(--success)' }}>{metrics.latency_ms}ms</h3>
                                <span className="label">LATENCY</span>
                            </div>
                        </div>
                    </div>

                    <div className="panel" style={{ flex: 2 }}>
                        <span className="label">AI Logic Strategy</span>
                        <div style={{ padding: '0.5rem', background: 'rgba(0,0,0,0.2)', borderRadius: '4px', height: '100px', overflowY: 'auto' }}>
                            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                {metrics.last_action || "Awaiting strategy input..."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
