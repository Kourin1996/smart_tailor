import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Stack, TextField } from '@mui/material';

const BorderColor = 'rgba(144, 202, 249, 0.4)'
const TextColor = 'rgba(144, 202, 249, 1.0)'

export const RootPage = () => {
    const navigate = useNavigate();
    const [query, setQuery] = React.useState('');

    const handleMountInput = useCallback((input: HTMLDivElement | null) => {
        if (input !== null) {
            setTimeout(() => {
                input.focus();
            }, 100)
        }
    }, []);

    const handleSubmit = useCallback(async () => {
        console.log('handleSubmmit', query);

        const response = await fetch('http://localhost:8080/projects', {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            redirect: "follow", 
            body: JSON.stringify({
                query
            }),
          });
        
        const body: {id: string} = await response.json();

        console.log('response body', body);
        
        navigate(`/projects/${body.id}`)
    }, [query]);

    return (
        <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
        >
            <Stack flexDirection="row" flexWrap="nowrap" alignItems="center" justifyContent="center" sx={{ padding: '4px 6px', borderRadius: '8px', border: `1px solid ${BorderColor}` }}>
                <Box minWidth="400px">
                    <TextField
                        placeholder="Input your idea for DApps"
                        fullWidth
                        inputProps={{ref: handleMountInput}}
                        sx={{
                            '& .MuiInputBase-root': {
                                color: TextColor,
                            },
                            "& fieldset": { border: 'none' },
                        }}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </Box>
                <Button variant="text" onClick={handleSubmit}>Order</Button>
            </Stack>
        </Box>
    )
}