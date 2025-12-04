import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import {StyledBigUserImage, StyledSmallUserImage} from '@app/styles/common';
import {
    UserFooter,
    UserHeader,
    UserMenuDropdown,
} from '@app/styles/dropdown-menus';
import {authService} from "@app/services/auth";
import {useAppSelector} from '@app/store/store';
import {DateTime} from 'luxon';

const UserDropdown = () => {
    const navigate = useNavigate();
    const [t] = useTranslation();
    const currentUser = useAppSelector((state) => state.auth.currentUser);
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const logOut = async (event: any) => {
        await authService.logout();
        event.preventDefault();
        setDropdownOpen(false);
    };

    const navigateToProfile = (event: any) => {
        event.preventDefault();
        setDropdownOpen(false);
        navigate('/user/profile');
    };

    return (
        <UserMenuDropdown isOpen={dropdownOpen} hideArrow>
            <StyledSmallUserImage
                slot="head"
                src={currentUser?.photoURL}
                fallbackSrc="/img/default-profile.png"
                alt="User"
                width={25}
                height={25}
                rounded
            />
            <div slot="body">
                <UserHeader className=" bg-primary">
                    <StyledBigUserImage
                        src={currentUser?.photoURL}
                        fallbackSrc="/img/default-profile.png"
                        alt="User"
                        width={90}
                        height={90}
                        rounded
                    />
                    <p>
                        {currentUser?.email}
                        <small>
                            <span>Member since </span>
                            {currentUser?.createdAt && (
                                <span>
                  {DateTime.fromRFC2822(
                      currentUser?.createdAt
                  ).toFormat('yyyy LLL dd')}
                </span>
                            )}
                        </small>
                    </p>
                </UserHeader>
                <UserFooter>
                    <button
                        type="button"
                        className="btn btn-default btn-flat"
                        onClick={navigateToProfile}
                    >
                        {t('header.user.profile')}
                    </button>
                    <button
                        type="button"
                        className="btn btn-default btn-flat float-right"
                        onClick={logOut}
                    >
                        {t('login.button.signOut')}
                    </button>
                </UserFooter>
            </div>
        </UserMenuDropdown>
    );
};

export default UserDropdown;
