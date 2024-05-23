import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LogIn from './LogIn';

jest.mock('axios');

describe('LogIn Component', () => {
  const setToken = jest.fn();

  it('renders the login form', () => {
    render(<LogIn setToken={setToken} />);

    expect(screen.getByPlaceholderText('Enter Username or Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter Password')).toBeInTheDocument();
    expect(screen.getByText("Don't have an account?")).toBeInTheDocument();
  });

  it('submits the login form', async () => {
    const axios = require('axios');
    axios.post.mockResolvedValue({ data: 'mockToken' });

    render(<LogIn setToken={setToken} />);

    fireEvent.change(screen.getByPlaceholderText('Enter Username or Email'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByPlaceholderText('Enter Password'), { target: { value: 'password' } });

    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(setToken).toHaveBeenCalledWith('logged_in');
    });

    expect(screen.getByPlaceholderText('Enter Username or Email').value).toBe('');
    expect(screen.getByPlaceholderText('Enter Password').value).toBe('');
  });

  it('handles login error', async () => {
    const axios = require('axios');
    axios.post.mockRejectedValue(new Error('Login failed'));

    render(<LogIn setToken={setToken} />);

    fireEvent.change(screen.getByPlaceholderText('Enter Username or Email'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByPlaceholderText('Enter Password'), { target: { value: 'password' } });

    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(setToken).not.toHaveBeenCalled();
    });

    expect(screen.getByText('Login failed: Error: Login failed')).toBeInTheDocument();
  });
});