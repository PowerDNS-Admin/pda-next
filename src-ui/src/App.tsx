import {useEffect, useState} from 'react';
import {Routes, Route, useLocation} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import Main from '@modules/main/Main';
import Login from '@modules/login/Login';
import Register from '@modules/register/Register';
import ForgetPassword from '@modules/forgot-password/ForgotPassword';
import RecoverPassword from '@modules/recover-password/RecoverPassword';
import {useWindowSize} from '@app/hooks/useWindowSize';
import {calculateWindowSize} from '@app/utils/helpers';
import {setWindowSize} from '@app/store/reducers/ui';
import ReactGA from 'react-ga4';

import Dashboard from '@pages/Dashboard';
import Blank from '@pages/Blank';
import SubMenu from '@pages/SubMenu';
import Profile from '@pages/profile/Profile';
import AuthUsersView from '@pages/auth/Users';

import PublicRoute from './routes/PublicRoute';
import PrivateRoute from './routes/PrivateRoute';
import {setCurrentUser} from '@store/reducers/auth';
import {authService} from "@app/services/auth";
import {useAppDispatch, useAppSelector} from '@store/store';
import {Loading} from './components/Loading';

const {VITE_NODE_ENV} = import.meta.env;

const App = () => {
    const windowSize = useWindowSize();
    const screenSize = useAppSelector((state) => state.ui.screenSize);
    const dispatch = useAppDispatch();
    const location = useLocation();

    const [isAppLoading, setIsAppLoading] = useState(true);

    useEffect(() => {
        setIsAppLoading(true);

        const unsubscribe = authService.onAuthStateChanged((user) => {
            if (user) {
                dispatch(setCurrentUser(user));
            } else {
                dispatch(setCurrentUser(null));
            }
            setIsAppLoading(false);
        });

        return unsubscribe;
    }, []);

    useEffect(() => {
        const size = calculateWindowSize(windowSize.width);
        if (screenSize !== size) {
            dispatch(setWindowSize(size));
        }
    }, [windowSize]);

    useEffect(() => {
        if (location && location.pathname && VITE_NODE_ENV === 'production') {
            ReactGA.send({
                hitType: 'pageview',
                page: location.pathname,
            });
        }
    }, [location]);

    if (isAppLoading) {
        return <Loading/>;
    }

    return (
        <>
            <Routes>
                <Route path="/user/login" element={<PublicRoute/>}>
                    <Route path="/user/login" element={<Login/>}/>
                </Route>
                <Route path="/user/register" element={<PublicRoute/>}>
                    <Route path="/user/register" element={<Register/>}/>
                </Route>
                <Route path="/user/forgot-password" element={<PublicRoute/>}>
                    <Route path="/user/forgot-password" element={<ForgetPassword/>}/>
                </Route>
                <Route path="/user/recover-password" element={<PublicRoute/>}>
                    <Route path="/user/recover-password" element={<RecoverPassword/>}/>
                </Route>
                <Route path="/" element={<PrivateRoute/>}>
                    <Route path="/" element={<Main/>}>
                        <Route path="/auth/users" element={<AuthUsersView/>}/>
                        <Route path="/sub-menu-2" element={<Blank/>}/>
                        <Route path="/sub-menu-1" element={<SubMenu/>}/>
                        <Route path="/blank" element={<Blank/>}/>
                        <Route path="/user/profile" element={<Profile/>}/>
                        <Route path="/" element={<Dashboard/>}/>
                    </Route>
                </Route>
            </Routes>
            <ToastContainer
                autoClose={3000}
                draggable={false}
                position="top-right"
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnHover
            />
        </>
    );
};

export default App;
