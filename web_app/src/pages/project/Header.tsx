import React, { useCallback } from 'react';
import { Box, Stack, Typography, Button } from '@mui/material';

const BorderColor = 'rgba(144, 202, 249, 0.5)';

export const Header = ({appName}: {appName: string}) => {
    const handleBuild = useCallback(() => {

    }, []);

    return (
        <Box width="100%" height="60px" sx={{ flex: '0 0 60px' }}>
            <Stack direction="row" alignItems="center" justifyContent="space-between" width="100%" height="100%">
                <Box marginLeft="36px">
                    <Typography>{appName}</Typography>
                </Box>
                <Stack marginRight="36px">
                    <Button variant="outlined" onClick={handleBuild}>Build & ReDeploy</Button>
                </Stack>
            </Stack>
        </Box>
    )
}