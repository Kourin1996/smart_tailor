import React, { useCallback, useEffect, useState } from 'react';
import { Box, Stack, Typography, Grid, Button } from '@mui/material';
import { useParams } from 'react-router-dom';
import { Footer } from './Footer';
import { EditorPane } from './Editor';
import { PreviewPane } from './Preview';
import { LoadingPanel } from './Loading';
import { Header } from './Header';

const BorderColor = 'rgba(144, 202, 249, 0.5)';

const EditorPage = () => {
    return (
        <Stack
            display="flex"
            direction="column"
            alignItems="space-between"
            minHeight="100vh"
            maxHeight="100vh"
            width="calc(100vw - 36px)"
            sx={{margin: '0px 8px'}}
        >
            <Header />
            <Grid container flexWrap="nowrap" sx={{ padding: '24px 0px', height: "calc(100vh - 250px)", overflow: 'hidden' }}>
                <Grid xs={6} sx={{ maxHeight: "100%", overflow: 'auto', '&::-webkit-scrollbar': { display: 'none' } }}>
                    <EditorPane />
                </Grid>
                <Grid xs={6} sx={{ marginLeft: '16px', marginRight: '16px', maxHeight: "100%", overflowY: 'auto', border: `1px solid ${BorderColor}`, borderRadius: '8px', '&::-webkit-scrollbar': { display: 'none' } }}>
                    <PreviewPane />
                </Grid>
            </Grid>
            <Footer />
        </Stack>
    )
}

export const ProjectPage = () => {
    const { projectId } = useParams();

    const [count, setCount] = useState(0);
    const [record, setRecord] = useState<any>({});

    useEffect(() => {
        if (record?.status === 'COMPLETE') {
            return
        }

        const timer = setTimeout(async () => {
            try {
                const res = await fetch(`http://localhost:8080/projects/${projectId}/status`)
                const data = await res.json();
    
                console.log('new record', data);
    
                setRecord(data);
            } catch(error) {
                console.error(error)
            } finally {
                setCount(c => c + 1)
            }
        }, 1000)

        return () => {
            clearTimeout(timer);
        }
    }, [record, count])

    return record?.status === 'COMPLETE' ? <EditorPage /> : <LoadingPanel status={record.status} />
}