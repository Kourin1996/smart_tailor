import React, { useMemo } from 'react';
import { Box, Stack, CircularProgress, Typography } from '@mui/material';

const CircleColor = 'rgba(144, 202, 249, 0.7)'
const TextColor = 'rgba(144, 202, 249, 1.0)'

// # Status
// # SETUP
// # GENERATE_REQUIREMENTS
// # GENERATE_SPECIFICATIONS
// # GENERATE_SOLIDITY
// # FIX_SOLIDITY
// # GENERATE_REACT
// # ERROR

export const LoadingPanel = ({status}: {status: string}) => {
    const message = useMemo(() => {
        switch (status) {
            case 'SETUP':
                return 'Setting up project...'
            case 'GENERATE_REQUIREMENTS':
                return 'Generating requirements...'
            case 'GENERATE_SPECIFICATIONS':
                return 'Generating specifications...'
            case 'GENERATE_SOLIDITY':
                return 'Generating solidity code...'
            case 'FIX_SOLIDITY':
                return 'Fixing solidity code automatically...'
            case 'GENERATE_REACT':
                return 'Generating React page...'
            case 'ERROR':
                return 'Error happens, please retry' 
        }
        return ''
    }, [status]);

    return (
        <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
        >
            <Stack flexDirection="column" flexWrap="nowrap" alignItems="center" justifyContent="center">
                <CircularProgress sx={{
                    width: '80px !important',
                    height: '80px !important',
                    '& svg': {
                        color: CircleColor
                    }
                }} />
                <Typography fontSize="18px" sx={{ marginTop: '32px', color: TextColor }}>{message}</Typography>
            </Stack>
        </Box>
    )
}