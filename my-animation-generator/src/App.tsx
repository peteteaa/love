import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setApiResponse(null);
    
    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      // First, let's check what type of content we're receiving
      const contentType = response.headers.get('content-type');
      console.log('Content-Type:', contentType);

      // If it's not JSON, let's see the raw text
      if (!contentType?.includes('application/json')) {
        const textResponse = await response.text();
        console.log('Raw Response:', textResponse);
        setApiResponse({
          error: 'Invalid response format',
          rawResponse: textResponse,
          contentType: contentType
        });
        return;
      }
      
      const data = await response.json();
      setApiResponse(data);
      console.log('API Response:', data);
      
    } catch (error) {
      console.error('Error:', error);
      setApiResponse({ 
        error: String(error),
        details: 'Check the console for full response details'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Love Bubbles</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              rows={4}
              style={{
                width: '300px',
                padding: '10px',
                margin: '10px 0',
                borderRadius: '5px',
              }}
            />
          </div>
          <button 
            type="submit"
            disabled={isLoading || !prompt.trim()}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              borderRadius: '5px',
              cursor: 'pointer',
              backgroundColor: '#61dafb',
              border: 'none',
              color: '#282c34',
            }}
          >
            {isLoading ? 'Generating...' : 'Generate Animation'}
          </button>
        </form>

        {isLoading && <p>Loading...</p>}
        
        {apiResponse && (
          <div style={{ 
            marginTop: '20px',
            padding: '20px',
            backgroundColor: '#1e1e1e',
            borderRadius: '8px',
            maxWidth: '80%',
            overflow: 'auto'
          }}>
            <h3>API Response:</h3>
            <pre style={{ 
              textAlign: 'left',
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word'
            }}>
              {JSON.stringify(apiResponse, null, 2)}
            </pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
