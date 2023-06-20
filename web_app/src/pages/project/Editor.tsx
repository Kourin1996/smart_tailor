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

export const EditorPane = (props: {solidityCode: string; reactCode: string}) => {
    const {solidityCode: defaultSolidityCode, reactCode: defaultReactCode} = props;
    const [solidityCode, setSolidityCode] = useState(defaultSolidityCode);
    const [reactCode, setReactCode] = useState(defaultReactCode);

    console.log('solidityCode', solidityCode);

    return (
        <Box height="100%" sx={{ flex: '0 0 200px' }}>
            <Box height="100%" sx={{
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
                        {/* TODO: 高さ調整 */}
                        <Box height="800px" sx={{ overflow: 'scroll', '&::-webkit-scrollbar': { display: 'none' }, '& > div': { background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px' } }}>
                            <Editor
                                value={solidityCode}
                                onValueChange={code => setSolidityCode(code)}
                                highlight={code => highlight(code, languages.sol, 'sol')}
                                style={{
                                    fontFamily: '"Fira code", "Fira Mono", monospace',
                                    fontSize: 16,
                                }}
                            />
                        </Box>
                    </TabPanel>
                    <TabPanel>
                        {/* TODO: 高さ調整 */}
                        <Box height="800px" sx={{ overflow: 'scroll', '&::-webkit-scrollbar': { display: 'none' }, '& > div': { background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px' } }}>
                            <Editor
                                value={reactCode}
                                onValueChange={code => setReactCode(code)}
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