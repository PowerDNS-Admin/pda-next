import { Navigate, Outlet } from 'react-router-dom';
import { useAppSelector } from '@app/store/store';

const PrivateRoute = () => {
  const isLoggedIn = useAppSelector((state) => state.auth.currentUser);
  return isLoggedIn ? <Outlet /> : <Navigate to={`/user/login`} />;
};

export default PrivateRoute;
