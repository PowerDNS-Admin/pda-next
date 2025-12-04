import {Grid} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {GridDataSource, GridGetRowsParams, GridGetRowsResponse} from "@mui/x-data-grid";
import {DataGridPro, GridColDef, GridActionsCellItem} from '@mui/x-data-grid-pro';
import {ContentHeader} from '@components';

const Dashboard = () => {

    const handleEdit = (id: string) => {
        console.log('Edit row with id:', id);
    };

    const handleDelete = (id: string) => {
        console.log('Delete row with id:', id);
    };

    const handleDataSourceError = (error: any) => {
        console.error(error);
    };

    const columns: readonly GridColDef<any>[] = [
        {field: 'id', headerName: 'User ID', width: 300},
        {field: 'tenant_id', headerName: 'Tenant ID', width: 300},
        {field: 'username', headerName: 'Username', width: 300},
        {field: 'status', headerName: 'Status', width: 100},
        {field: 'created_at', headerName: 'Created', width: 175},
        {field: 'updated_at', headerName: 'Updated', width: 175},
        {field: 'authenticated_at', headerName: 'Last Login', width: 175},
        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 100,
            getActions: (params) => [
                <GridActionsCellItem
                    icon={<EditIcon/>}
                    label="Edit"
                    onClick={() => handleEdit(params.row.id)}
                    showInMenu
                />,
                <GridActionsCellItem
                    icon={<DeleteIcon/>}
                    label="Delete"
                    onClick={() => handleDelete(params.row.id)}
                    showInMenu
                />,
            ],
        },
    ];

    const dataSource: GridDataSource = {
        getRows: async (params: GridGetRowsParams): Promise<GridGetRowsResponse> => {
            const response = await fetch('/api/v1/auth/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(params),
            });

            const data = await response.json();

            return {
                rows: data.records,
                rowCount: data.total,
            };
        },
    }

    return (
        <Grid container>
            <Grid size={12}>
                <ContentHeader title="Users Administration"/>
            </Grid>
            <Grid size={12}>
                <DataGridPro
                    autoHeight
                    pagination
                    sortingMode="server"
                    filterMode="server"
                    paginationMode="server"
                    pageSizeOptions={[5, 10, 25, 50, 100]}
                    columns={columns}
                    dataSource={dataSource}
                    onDataSourceError={handleDataSourceError}
                    initialState={{
                        pinnedColumns: {
                            right: ['actions'],
                        },
                    }}
                />
            </Grid>
        </Grid>
    );
};

export default Dashboard;
