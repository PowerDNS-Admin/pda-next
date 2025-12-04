import * as React from 'react';
import {
    Dialog,
    DialogProps,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Typography,
    Box,
    Grid,
    Stack,
    Button,
    TextField,
    FormGroup,
    FormControl,
    FormControlLabel,
    InputLabel,
    Select,
    MenuItem,
    Checkbox,

} from '@mui/material';
import i18n from '@app/utils/i18n';

export default function UserFormDialog() {
    const [open, setOpen] = React.useState(false);
    const [fullWidth, setFullWidth] = React.useState(true);
    const [maxWidth, setMaxWidth] = React.useState<DialogProps['maxWidth']>('md');

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleSave = () => {
        //setOpen(false);
    };

    return (
        <React.Fragment>
            <Button variant="contained" onClick={handleClickOpen}>
                {i18n.t('dialogs.auth.userDialog.createButton')}
            </Button>
            <Dialog
                fullWidth={fullWidth}
                maxWidth={maxWidth}
                open={open}
                onClose={handleClose}
            >
                <DialogTitle>{i18n.t('dialogs.auth.userDialog.create.title')}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {i18n.t('dialogs.auth.userDialog.create.headerText')}
                    </DialogContentText>
                    <Grid container marginY={2}>
                        <Grid size={{xs: 12, md: 6}}>
                            <Typography variant="h6" align="center" gutterBottom>User Information</Typography>
                            <Stack component="form" spacing={3} onSubmit={handleSave} noValidate>
                                {/* Username Input */}
                                <TextField
                                    label="Username"
                                    name="username"
                                    variant="outlined" // Common variant for forms
                                    fullWidth
                                    required
                                />

                                {/* Password Input */}
                                <TextField
                                    label="Password"
                                    name="password"
                                    type="password" // Masks the input for security
                                    variant="outlined"
                                    fullWidth
                                    required
                                />

                                {/* Email Input */}
                                <TextField
                                    label="Email"
                                    name="email"
                                    type="email" // Ensures correct keyboard type on mobile and basic validation
                                    variant="outlined"
                                    fullWidth
                                    required
                                />

                                {/* Status Select/Dropdown */}
                                <FormControl fullWidth variant="outlined">
                                    <InputLabel id="status-label">Status</InputLabel>
                                    <Select
                                        labelId="status-label"
                                        id="status"
                                        name="status"
                                        label="Status"
                                    >
                                        <MenuItem value="">
                                            <em>None</em>
                                        </MenuItem>
                                        <MenuItem value={'active'}>Active</MenuItem>
                                        <MenuItem value={'inactive'}>Inactive</MenuItem>
                                        <MenuItem value={'pending'}>Pending</MenuItem>
                                    </Select>
                                </FormControl>

                                {/* Tenant Select/Dropdown */}
                                <FormControl fullWidth variant="outlined">
                                    <InputLabel id="tenant-label">Tenant</InputLabel>
                                    <Select
                                        labelId="tenant-label"
                                        id="tenant"
                                        name="tenant"
                                        label="Tenant"
                                    >
                                        <MenuItem value="">
                                            <em>None</em>
                                        </MenuItem>
                                        <MenuItem value={'t1'}>Tenant 1</MenuItem>
                                        <MenuItem value={'t2'}>Tenant 2</MenuItem>
                                        <MenuItem value={'t3'}>Tenant 3</MenuItem>
                                    </Select>
                                </FormControl>
                            </Stack>
                        </Grid>
                        <Grid size={{xs: 12, md: 6}}>
                            <Typography variant="h6" align="center" gutterBottom>User Roles</Typography>
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button variant="contained" color="error" onClick={handleClose}>Cancel</Button>
                    <Button variant="contained" color="success" onClick={handleSave} type="submit">Save</Button>
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
}
