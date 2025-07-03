import React, { createContext, useContext, useEffect, useState } from 'react';
import api from './api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  function saveToken(tok) {
    if (tok) {
      localStorage.setItem('token', tok);
    } else {
      localStorage.removeItem('token');
    }
    setToken(tok);
  }

  async function login(email, password) {
    setLoading(true);
    try {
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);
      const resp = await api.post('/auth/login', form);
      saveToken(resp.data.access_token);
      return true;
    } catch (err) {
      console.error(err);
      return false;
    } finally {
      setLoading(false);
    }
  }

  async function register(email, password) {
    setLoading(true);
    try {
      await api.post('/auth/register', { email, password });
      return login(email, password);
    } catch (err) {
      console.error(err);
      setLoading(false);
      return false;
    }
  }

  function logout() {
    saveToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
} 