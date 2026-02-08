'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authProvider } from '@/auth/auth_provider';

const AuthenticatedLayout = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      await authProvider.init();
      const authenticated = authProvider.isAuthenticated();
      setIsAuthenticated(authenticated);
      
      if (!authenticated) {
        router.push('/auth');
      }
    };
    
    checkAuth();
  }, [router]);

  // Show loading state while checking authentication
  if (isAuthenticated === null) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated, don't render children (they should be redirected by now)
  if (!isAuthenticated) {
    return null;
  }

  // Only render children if authenticated
  return (
    <>
      {children}
    </>
  );
};

export default AuthenticatedLayout;