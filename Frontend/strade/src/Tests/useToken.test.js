import { renderHook, act } from '@testing-library/react-hooks';
import useToken from '../Components/useToken';

describe('useToken hook', () => {
  beforeEach(() => {
    // Mock sessionStorage
    sessionStorage.clear();
  });

  it('should return null when token is not set', () => {
    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBeNull();
  });

  it('should return token after setting it', () => {
    const { result } = renderHook(() => useToken());

    act(() => {
      result.current.setToken('test_token');
    });

    expect(result.current.token).toBe('test_token');
    expect(sessionStorage.getItem('access_token')).toBe('test_token');
  });

  it('should clear token when setToken is called with null', () => {
    const { result } = renderHook(() => useToken());

    act(() => {
      result.current.setToken('test_token');
    });

    expect(result.current.token).toBe('test_token');
    expect(sessionStorage.getItem('access_token')).toBe('test_token');

    act(() => {
      result.current.setToken(null);
    });

    expect(result.current.token).toBeNull();

  });

  it('should initialize with existing token from sessionStorage', () => {
    sessionStorage.setItem('access_token', 'initial_token');

    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBe('initial_token');
  });
});
