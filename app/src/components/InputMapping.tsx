import React, { useState } from 'react';

const InputMapping: React.FC = () => {
    const [mappings, setMappings] = useState([
        { action: 'Move Forward', key: 'W', type: 'key' },
        { action: 'Move Left', key: 'A', type: 'key' },
        { action: 'Move Back', key: 'S', type: 'key' },
        { action: 'Move Right', key: 'D', type: 'key' },
        { action: 'Primary Attack', key: 'Left Click', type: 'mouse' },
    ]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <header>
                <h1>Neural Interface Mapping</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Translate AI logic into physical game inputs.</p>
            </header>

            <div className="panel">
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--panel-border)' }}>
                            <th style={{ padding: '1rem' }}>AI ACTION</th>
                            <th style={{ padding: '1rem' }}>PHYSICAL BINDING</th>
                            <th style={{ padding: '1rem' }}>INPUT TYPE</th>
                            <th style={{ padding: '1rem' }}>SENSITIVITY</th>
                        </tr>
                    </thead>
                    <tbody>
                        {mappings.map((m, i) => (
                            <tr key={i} style={{ borderBottom: '1px solid var(--panel-border)' }}>
                                <td style={{ padding: '1rem' }}>{m.action}</td>
                                <td style={{ padding: '1rem' }}>
                                    <input type="text" value={m.key} onChange={() => {}} style={{ background: 'transparent', border: 'none' }} />
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <span style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', background: 'var(--accent-muted)', borderRadius: '4px' }}>
                                        {m.type.toUpperCase()}
                                    </span>
                                </td>
                                <td style={{ padding: '1rem' }}>1.0</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
                    <button className="secondary">Reset to Defaults</button>
                    <button>Save Control Profile</button>
                </div>
            </div>
        </div>
    );
};

export default InputMapping;
