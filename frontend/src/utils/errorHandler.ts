export const handleApiError = (error: any): string => {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    
    if (error.message) {
      return error.message;
    }
    
    return 'An unknown error occurred. Please try again.';
  };
  