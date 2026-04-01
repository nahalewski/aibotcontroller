import React, { useState, useEffect } from 'react';

const CaptureSetup: React.FC = () => {
    const [windows, setWindows] = useState<{ id: number, title: string }[]>([]);
    const [selectedWindow, setSelectedWindow] = useState('');
    const [fps, setFps] = useState(15);
    const [scale, setScale] = useState(0.5);

    useEffect(() => {
        fetch('http://localhost:8000/windows')
            .then(res => res.json())
            .then(data => setWindows(data));
    }, []);

    const handleSelect = async (title: string) => {
        setSelectedWindow(title);
        await fetch('http://localhost:8000/select_window', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, fps, scale })
        });
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <header>
                <h1>Capture Configuration</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Identify the game window or display to monitor.</p>
            </header>

            <div className="grid">
                <div className="panel">
                    <span className="label">Available Game Windows</span>
                    <div style={{ height: '300px', overflowY: 'auto', border: '1px solid var(--panel-border)', borderRadius: '6px' }}>
                        {windows.map(win => (
                            <div 
                                key={win.id} 
                                style={{ 
                                    padding: '0.8rem', cursor: 'pointer', 
                                    background: selectedWindow === win.title ? 'var(--accent-muted)' : 'transparent',
                                    borderBottom: '1px solid var(--panel-border)'
                                }}
                                onClick={() => handleSelect(win.title)}
                            >
                                <span style={{ fontSize: '0.9rem' }}>{win.title}</span>
                            </div>
                        ))}
                    </div>
                    <button 
                        className="secondary" 
                        style={{ marginTop: '1rem', width: '100%' }}
                        onClick={() => fetch('http://localhost:8000/windows').then(res => res.json()).then(setWindows)}
                    >
                        Refresh Windows List
                    </button>
                </div>

                <div className="panel">
                    <span className="label">Capture Parameters</span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div>
                            <span className="label">Target FPS Limit</span>
                            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                <input type="range" min="1" max="30" value={fps} onChange={(e) => setFps(parseInt(e.target.value))} />
                                <span style={{ width: '40px', textAlign: 'right' }}>{fps}</span>
                            </div>
                        </div>
                        <div>
                            <span className="label">Resolution Scaling</span>
                            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                <input type="range" min="0.1" max="1.0" step="0.1" value={scale} onChange={(e) => setScale(parseFloat(e.target.value))} />
                                <span style={{ width: '40px', textAlign: 'right' }}>{Math.round(scale * 100)}%</span>
                            </div>
                        </div>
                        <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '1rem', borderRadius: '6px', border: '1px solid var(--accent-muted)' }}>
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                <strong style={{ color: 'var(--accent-color)' }}>Tip:</strong> Lower resolution scaling significantly reduces AI inference latency.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CaptureSetup;
