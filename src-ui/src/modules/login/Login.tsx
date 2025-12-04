import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {useFormik} from 'formik';
import {useTranslation} from 'react-i18next';
import {setCurrentUser} from '@store/reducers/auth';
import {setWindowClass} from '@app/utils/helpers';
import {Checkbox} from '@profabric/react-components';
import * as Yup from 'yup';

import {Form, InputGroup} from 'react-bootstrap';
import {Button} from '@app/styles/common';
import {authService} from '@app/services/auth';
import {useAppDispatch} from '@app/store/store';

const Login = () => {
    const [isAuthLoading, setAuthLoading] = useState(false);
    const [isGoogleAuthLoading] = useState(false);
    const [isFacebookAuthLoading] = useState(false);
    const dispatch = useAppDispatch();

    const navigate = useNavigate();
    const [t] = useTranslation();

    const login = async (email: string, password: string) => {
        try {
            setAuthLoading(true);
            await authService.login(email, password);
            toast.success('Authentication Successful!');
            setAuthLoading(false);
            //navigate('/');
        } catch (error: any) {
            setAuthLoading(false);
            toast.error(error.message || 'Authentication Failed');
        }
    };

    const {handleChange, values, handleSubmit, touched, errors} = useFormik({
        initialValues: {
            email: '',
            password: '',
        },
        validationSchema: Yup.object({
            email: Yup.string().email('Invalid email address').required('Required'),
            password: Yup.string()
                .min(4, 'Must be 5 characters or more')
                .max(30, 'Must be 30 characters or less')
                .required('Required'),
        }),
        onSubmit: (values) => {
            login(values.email, values.password);
        },
    });

    setWindowClass('hold-transition login-page');

    return (
        <div className="login-box">
            <div className="card card-outline card-primary">
                <div className="card-header text-center">
                    <Link to="https://powerdnsadmin.org" target="_blank" className="h1">
                        <b>PowerDNS</b>
                        <span>Admin</span>
                    </Link>
                </div>
                <div className="card-body">
                    <p className="login-box-msg">{t('login.label.signIn')}</p>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <InputGroup className="mb-3">
                                <Form.Control
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="Email"
                                    onChange={handleChange}
                                    value={values.email}
                                    isValid={touched.email && !errors.email}
                                    isInvalid={touched.email && !!errors.email}
                                />
                                {touched.email && errors.email ? (
                                    <Form.Control.Feedback type="invalid">
                                        {errors.email}
                                    </Form.Control.Feedback>
                                ) : (
                                    <InputGroup.Append>
                                        <InputGroup.Text>
                                            <i className="fas fa-envelope"/>
                                        </InputGroup.Text>
                                    </InputGroup.Append>
                                )}
                            </InputGroup>
                        </div>
                        <div className="mb-3">
                            <InputGroup className="mb-3">
                                <Form.Control
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder="Password"
                                    onChange={handleChange}
                                    value={values.password}
                                    isValid={touched.password && !errors.password}
                                    isInvalid={touched.password && !!errors.password}
                                />
                                {touched.password && errors.password ? (
                                    <Form.Control.Feedback type="invalid">
                                        {errors.password}
                                    </Form.Control.Feedback>
                                ) : (
                                    <InputGroup.Append>
                                        <InputGroup.Text>
                                            <i className="fas fa-lock"/>
                                        </InputGroup.Text>
                                    </InputGroup.Append>
                                )}
                            </InputGroup>
                        </div>
                        <div className="row">
                            <div className="col-8">
                                <div style={{display: 'flex', alignItems: 'center'}}>
                                    <Checkbox id="chkRememberMe" checked={false}/>
                                    <label htmlFor="chkRememberMe" style={{margin: 0, padding: 0, paddingLeft: '4px'}}>
                                        {t('login.label.rememberMe')}
                                    </label>
                                </div>
                            </div>
                            <div className="col-4">
                                <Button
                                    loading={isAuthLoading}
                                    disabled={isFacebookAuthLoading || isGoogleAuthLoading}
                                    onClick={handleSubmit as any}
                                >
                                    {t('login.button.signIn.label')}
                                </Button>
                            </div>
                        </div>
                    </form>
                    <p className="mb-1">
                        <Link to="/user/forgot-password">{t('login.label.forgotPass')}</Link>
                    </p>
                    <p className="mb-0">
                        <Link to="/user/register" className="text-center">
                            {t('login.label.registerNew')}
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
