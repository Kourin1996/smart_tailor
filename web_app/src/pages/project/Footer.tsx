import React, { useMemo } from 'react';
import { Box } from '@mui/material';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';

import 'prismjs/components/prism-bash.min';
import 'prismjs/themes/prism.css';

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

export const Footer = ({solidityBuildResult, reactBuildResult}: {solidityBuildResult: string; reactBuildResult: string}) => {
    return (
        <Box height="200px" sx={{flex: '0 0 200px'}}>
            <Box height="190px" sx={{
                margin: '0px 24px',
                overflow: 'hidden',
                ...ReactTabsStyle,
            }}>
                <Tabs style={{ height: '100%' }}>
                    <TabList>
                        <Tab>Solidity Build Result</Tab>
                        <Tab>React Build Result</Tab>
                    </TabList>
                    <TabPanel style={{ height: '100%' }}>
                        <Box height="100%" overflow="auto" sx={{ '&::-webkit-scrollbar': { display: 'none' }, '& > div': {background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px'} }}>
                            <Editor
                                readOnly
                                value={solidityBuildResult}
                                onValueChange={() => { }}
                                highlight={code => highlight(code, languages.bash, 'bash')}
                                padding={20}
                                style={{
                                    fontFamily: '"Fira code", "Fira Mono", monospace',
                                    fontSize: 16,
                                }}
                            />
                        </Box>
                    </TabPanel>
                    <TabPanel style={{ height: '100%' }}>
                        <Box height="100%" overflow="auto" sx={{ '&::-webkit-scrollbar': { display: 'none' }, '& > div': {background: 'rgba(64, 64, 64, 0.2)', paddingBottom: '16px'} }}>
                            <Editor
                                readOnly
                                value={reactBuildResult}
                                onValueChange={() => { }}
                                highlight={code => highlight(code, languages.bash, 'bash')}
                                padding={20}
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