import { renderHook, act } from '@testing-library/react-hooks';
import useToken from '../Components/useToken';  // Importiere den Hook

// Mock für localStorage
const localStorageMock = (function () {
  let store = {};
  return {
    getItem(key) {
      return store[key] || null;
    },
    setItem(key, value) {
      store[key] = value.toString();
    },
    clear() {
      store = {};
    },
    removeItem(key) {
      delete store[key];
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('useToken Hook', () => {
  afterEach(() => {
    window.localStorage.clear();
  });

  test('should return null initially when no token is set', () => {
    const { result } = renderHook(() => useToken());
    expect(result.current.token).toBeNull();
  });

  test('should save and return token', () => {
    const { result } = renderHook(() => useToken());
    
    act(() => {
      result.current.setToken('test-token');
    });

    expect(result.current.token).toBe('test-token');
    expect(window.localStorage.getItem('access_token')).toBe('test-token');
  });

  test('should get token from localStorage if already set', () => {
    window.localStorage.setItem('access_token', 'existing-token');
    
    const { result } = renderHook(() => useToken());

    expect(result.current.token).toBe('existing-token');
  });

  test('should update token', () => {
    const { result } = renderHook(() => useToken());
    
    act(() => {
      result.current.setToken('initial-token');
    });

    expect(result.current.token).toBe('initial-token');

    act(() => {
      result.current.setToken('updated-token');
    });

    expect(result.current.token).toBe('updated-token');
    expect(window.localStorage.getItem('access_token')).toBe('updated-token');
  });
});
