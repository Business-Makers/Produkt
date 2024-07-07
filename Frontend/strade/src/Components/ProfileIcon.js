import React from 'react';

const ProfileIcon = ({ onClick }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width="40px"
    height="40px"
    fill="#ffffff"
    onClick={onClick}
    style={{ cursor: 'pointer' }}
  >
    <path d="M0 0h24v24H0z" fill="none" />
    <path d="M12 12c2.67 0 8 1.34 8 4v2H4v-2c0-2.66 5.33-4 8-4zm0-2a3 3 0 100-6 3 3 0 000 6zm0 2c-2.67 0-8 1.34-8 4v2c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-2c0-2.66-5.33-4-8-4zm0-2c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3z" />
  </svg>
);

export default ProfileIcon;