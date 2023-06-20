import React, { useCallback, useMemo, useState } from 'react';
import { Box } from '@mui/material';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';

import 'react-tabs/style/react-tabs.css';
import 'prismjs/components/prism-jsx.min'
import 'prismjs/components/prism-solidity.min'
import 'prismjs/themes/prism.css';

const CircleColor = 'rgba(144, 202, 249, 0.7)'
const TextColor = 'rgba(144, 202, 249, 1.0)'
const BorderColor = 'rgba(144, 202, 249, 0.5)';

const ReactTabsStyle = {
    '& .react-tabs__tab': {
        color: 'rgba(240,240,240,0.8)'
    },
    '& .react-tabs__tab-list': {
        borderBottom: `1px solid rgba(144, 202, 249, 0.5)`
    },
    '& .react-tabs__tab--selected': {
        color: 'rgba(240,240,240,0.8)',
        background: 'rgba(47,79,79,0.3)',
        borderColor: 'rgba(144, 202, 249, 0.5)',
    },
    '& .react-tabs__tab--selected:focus:after': {
        background: 'transparent',
        height: 0,
        content: 'none',
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
    }
}

export const EditorPane = () => {
    const [code, setCode] = useState(`
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import reportWebVitals from './reportWebVitals';
    import './index.css';
    
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    
    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
    reportWebVitals(); 
    
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import reportWebVitals from './reportWebVitals';
    import './index.css';
    
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    
    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
    reportWebVitals(); 

    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import reportWebVitals from './reportWebVitals';
    import './index.css';
    
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    
    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
    reportWebVitals(); 
`);

    return (
        <Box width="100vw" sx={{ flex: '0 0 200px' }}>
            <Box width="100%" sx={{
                margin: '0px 24px',
                overflow: 'hidden',
                ...ReactTabsStyle,
            }}>
                <Tabs style={{ height: '100%' }}>
                    <TabList>
                        <Tab>Solidity</Tab>
                        <Tab>React</Tab>
                    </TabList>
                    <TabPanel>
                        <Box height="850px" overflow="auto" sx={{ '&::-webkit-scrollbar': { display: 'none' }, '& > div': { background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px' } }}>
                            <Editor
                                value={code}
                                onValueChange={code => setCode(code)}
                                highlight={code => highlight(code, languages.jsx, 'jsx')}
                                style={{
                                    fontFamily: '"Fira code", "Fira Mono", monospace',
                                    fontSize: 16,
                                }}
                            />
                        </Box>
                    </TabPanel>
                    <TabPanel>
                        <Box height="850px" overflow="auto" sx={{ '&::-webkit-scrollbar': { display: 'none' }, '& > div': { background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px' } }}>
                            <Editor
                                value={code}
                                onValueChange={code => setCode(code)}
                                highlight={code => highlight(code, languages.jsx, 'jsx')}
                                style={{
                                    fontFamily: '"Fira code", "Fira Mono", monospace',
                                    fontSize: 16,
                                }}
                            />
                        </Box>
                    </TabPanel>
                </Tabs>
            </Box>
        </Box>
    )
}