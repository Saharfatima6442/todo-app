// frontend/src/auth/auth_provider.js

class AuthProvider {
  constructor() {
    this.currentUser = null;
    this.token = null;
  }

  /**
   * Initialize auth provider by checking for existing token (client-side only)
   */
  async init() {
    if (typeof window === 'undefined') return; // ← SSR guard

    this.token = localStorage.getItem('jwt_token');
    if (this.token) {
      // Verify token is still valid
      try {
        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
        const response = await fetch(`${baseUrl}/api/me`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });

        if (response.ok) {
          this.currentUser = await response.json();
        } else {
          this.logout();
        }
      } catch (error) {
        console.error('Error verifying token:', error);
        this.logout();
      }
    }
  }

  async login(username, password) {
    if (typeof window === 'undefined') return { success: false, error: 'Cannot login on server' };

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        this.token = data.token;
        this.currentUser = data.user;
        localStorage.setItem('jwt_token', this.token);
        return { success: true, user: this.currentUser };
      } else {
        const error = await response.json();
        return { success: false, error: error.message };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  }

  logout() {
    this.token = null;
    this.currentUser = null;
    if (typeof window !== 'undefined') localStorage.removeItem('jwt_token');
  }

  getCurrentUser() {
    return this.currentUser;
  }

  isAuthenticated() {
    return !!this.token;
  }

  getToken() {
    return this.token;
  }
}

// Export singleton
export const authProvider = new AuthProvider();
