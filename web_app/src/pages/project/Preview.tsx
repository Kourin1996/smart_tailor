import React from 'react';
import { Box } from '@mui/material';

export const PreviewPane = () => {
    return (
        <Box style={{height: "100%", overflow: 'hidden', background: 'white'}}>
            <iframe src={"http://localhost:8000/345cd862-9569-4a14-b6bd-0189ec6fa413"} style={{width: '100%', height: '100%', border: 'none'}}/>  
        </Box>
    )
}