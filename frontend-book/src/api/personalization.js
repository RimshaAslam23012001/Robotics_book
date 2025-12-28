// API client for personalization endpoints
const API_BASE_URL = 'http://localhost:8000/api';

class PersonalizationAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Get user background preferences
  async getUserBackground(token) {
    try {
      const response = await fetch(`${this.baseURL}/user/background`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user background:', error);
      throw error;
    }
  }

  // Update user background preferences
  async updateUserBackground(token, backgroundData) {
    try {
      const response = await fetch(`${this.baseURL}/user/background`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(backgroundData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating user background:', error);
      throw error;
    }
  }

  // Personalize a chapter
  async personalizeChapter(chapterId, token) {
    try {
      const response = await fetch(`${this.baseURL}/chapter/${chapterId}/personalize`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error personalizing chapter:', error);
      throw error;
    }
  }

  // Get chapter content
  async getChapter(chapterId, token) {
    try {
      const response = await fetch(`${this.baseURL}/chapter/${chapterId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching chapter:', error);
      throw error;
    }
  }
}

export default new PersonalizationAPI();