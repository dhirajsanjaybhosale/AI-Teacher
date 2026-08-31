import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
});

export const getFullMediaUrl = (relativeUrl) => {
  if (!relativeUrl) return '';
  if (relativeUrl.startsWith('http://') || relativeUrl.startsWith('https://')) {
    return relativeUrl;
  }
  return `${API_BASE}${relativeUrl.startsWith('/') ? '' : '/'}${relativeUrl}`;
};

export const createLesson = async ({ pdfFile, topic, level, timeMinutes, language }) => {
  const formData = new FormData();
  if (pdfFile) {
    formData.append('pdf_file', pdfFile);
  }
  if (topic) {
    formData.append('topic', topic);
  }
  formData.append('level', level || 'beginner');
  formData.append('time_minutes', timeMinutes || 10);
  formData.append('language', language || 'en');

  const res = await api.post('/api/lesson/create', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const getLesson = async (lessonId) => {
  const res = await api.get(`/api/lesson/${lessonId}`);
  return res.data;
};

export const renderSegmentVideo = async ({ lessonId, segmentId }) => {
  const res = await api.post('/api/segment/render', {
    lesson_id: lessonId,
    segment_id: segmentId,
  });
  return res.data;
};

export const submitAnswer = async ({ lessonId, segmentId, userAnswer, language }) => {
  const res = await api.post('/api/interact/submit-answer', {
    lesson_id: lessonId,
    segment_id: segmentId,
    user_answer: userAnswer,
    language: language || 'en',
  });
  return res.data;
};

export const getQuiz = async (lessonId) => {
  const res = await api.get(`/api/assessment/quiz/${lessonId}`);
  return res.data;
};

export const submitQuiz = async ({ lessonId, quizId, answers }) => {
  const res = await api.post('/api/assessment/submit-quiz', {
    lesson_id: lessonId,
    quiz_id: quizId,
    answers,
  });
  return res.data;
};

export const checkHealth = async () => {
  try {
    const res = await api.get('/api/health');
    return res.data;
  } catch (err) {
    return { status: 'offline', gpu_available: false, device: 'unknown' };
  }
};
