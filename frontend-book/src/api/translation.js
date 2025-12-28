// API client for translation endpoints
const API_BASE_URL = 'http://localhost:8000/api';

class TranslationAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Get original chapter content
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

  // Translate chapter to Urdu
  async translateChapterToUrdu(chapterId, token) {
    try {
      const response = await fetch(`${this.baseURL}/chapter/${chapterId}/translate/urdu`, {
        method: 'GET', // Using GET as per API design
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
      console.error('Error translating chapter to Urdu:', error);
      throw error;
    }
  }
}

export default new TranslationAPI();