import { renderHook, act } from '@testing-library/react-hooks';
import useToken from './useToken';

describe('useToken hook', () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  test('initial token is null when sessionStorage is empty', () => {
    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBeNull();
  });

  test('initial token is retrieved from sessionStorage', () => {
    sessionStorage.setItem('login_status', 'test-token');

    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBe('test-token');
  });

  test('setToken saves token to sessionStorage and state', () => {
    const { result } = renderHook(() => useToken());

    act(() => {
      result.current.setToken('new-token');
    });

    expect(result.current.token).toBe('new-token');
    expect(sessionStorage.getItem('login_status')).toBe('new-token');
  });

  test('setToken updates the token value', () => {
    const { result } = renderHook(() => useToken());

    act(() => {
      result.current.setToken('updated-token');
    });

    expect(result.current.token).toBe('updated-token');
    expect(sessionStorage.getItem('login_status')).toBe('updated-token');
  });

  test('getToken retrieves token from sessionStorage correctly', () => {
    sessionStorage.setItem('login_status', 'another-token');
    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBe('another-token');
  });
});