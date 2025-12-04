import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {useFormik} from 'formik';
import {useTranslation} from 'react-i18next';
import * as Yup from 'yup';
import {setWindowClass} from '@app/utils/helpers';
import {Form, InputGroup} from 'react-bootstrap';
import {Checkbox} from '@profabric/react-components';

import {setCurrentUser} from '@app/store/reducers/auth';
import {Button} from '@app/styles/common';
import {authService} from '@app/services/auth';
import {useAppDispatch} from '@app/store/store';

const Register = () => {
    const [isAuthLoading, setAuthLoading] = useState(false);
    const [isGoogleAuthLoading] = useState(false);
    const [isFacebookAuthLoading] = useState(false);
    const [t] = useTranslation();
    const dispatch = useAppDispatch();

    const navigate = useNavigate();

    const register = async (email: string, password: string) => {
        try {
            setAuthLoading(true);
            //const result = await registerWithEmail(email, password);
            // TODO
            //dispatch(setCurrentUser(result?.user as any));
            toast.success('Registration successful!');
            navigate('/');
        } catch (error: any) {
            toast.error(error.message || 'Registration Failed!');
            setAuthLoading(false);
        }
    };

    const {handleChange, values, handleSubmit, touched, errors, submitForm} =
        useFormik({
            initialValues: {
                email: '',
                password: '',
                passwordRetype: '',
            },
            validationSchema: Yup.object({
                email: Yup.string().email('Invalid email address').required('Required'),
                password: Yup.string()
                    .min(5, 'Must be 5 characters or more')
                    .max(30, 'Must be 30 characters or less')
                    .required('Required'),
                passwordRetype: Yup.string()
                    .min(5, 'Must be 5 characters or more')
                    .max(30, 'Must be 30 characters or less')
                    .required('Required'),
            }),
            onSubmit: (values) => {
                register(values.email, values.password);
            },
        });

    setWindowClass('hold-transition register-page');

    return (
        <div className="register-box">
            <div className="card card-outline card-primary">
                <div className="card-header text-center">
                    <Link to="https://powerdnsadmin.org" target="_blank" className="h1">
                        <b>PowerDNS</b>
                        <span>Admin</span>
                    </Link>
                </div>
                <div className="card-body">
                    <p className="login-box-msg">{t('register.registerNew')}</p>
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

                        <div className="mb-3">
                            <InputGroup className="mb-3">
                                <Form.Control
                                    id="passwordRetype"
                                    name="passwordRetype"
                                    type="password"
                                    placeholder="Retype password"
                                    onChange={handleChange}
                                    value={values.passwordRetype}
                                    isValid={touched.passwordRetype && !errors.passwordRetype}
                                    isInvalid={touched.passwordRetype && !!errors.passwordRetype}
                                />

                                {touched.passwordRetype && errors.passwordRetype ? (
                                    <Form.Control.Feedback type="invalid">
                                        {errors.passwordRetype}
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
                            <div className="col-7">
                                <div style={{display: 'flex', alignItems: 'center'}}>
                                    <Checkbox checked={false}/>
                                    <label style={{margin: 0, padding: 0, paddingLeft: '4px'}}>
                                        <span>I agree to the </span>
                                        <Link to="/">terms</Link>{' '}
                                    </label>
                                </div>
                            </div>
                            <div className="col-5">
                                <Button
                                    onClick={submitForm}
                                    loading={isAuthLoading}
                                    disabled={isGoogleAuthLoading || isFacebookAuthLoading}
                                >
                                    {t('register.label')}
                                </Button>
                            </div>
                        </div>
                    </form>
                    <Link to="/user/login" className="text-center">
                        {t('register.alreadyHave')}
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Register;
