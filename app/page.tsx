"use client";
import { useState } from 'react';

export default function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{role: string, text: string}[]>([]);

  const sendMessage = async () => {
    const newMessages = [...messages, { role: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: input }),
    });
    const data = await response.json();
    setMessages([...newMessages, { role: 'ai', text: data.text }]);
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#000', color: '#0f0', minHeight: '100vh', fontFamily: 'monospace' }}>
      <h1>Canal de Inteligência CyberVenum</h1>
      <div style={{ border: '1px solid #0f0', height: '400px', overflowY: 'scroll', marginBottom: '10px', padding: '10px' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: '10px' }}>
            <strong>{m.role === 'user' ? '> Usuário: ' : '> Agente: '}</strong>{m.text}
          </div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        style={{ width: '80%', padding: '10px', backgroundColor: '#111', color: '#0f0', border: '1px solid #0f0' }}
        placeholder="Digite seu comando..."
      />
      <button onClick={sendMessage} style={{ padding: '10px', marginLeft: '5px', cursor: 'pointer', backgroundColor: '#0f0', color: '#000', border: 'none' }}>Enviar</button>
    </div>
  );
}
