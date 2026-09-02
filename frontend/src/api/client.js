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

export const createLesson = async ({
  documentFile,
  pdfFile,
  topic,
  level,
  timeMinutes,
  goal,
  language,
  teachingStyle,
  existingKnowledge,
  forceWebSearch
}) => {
  const formData = new FormData();
  const fileToUpload = documentFile || pdfFile;
  if (fileToUpload) {
    formData.append('document_file', fileToUpload);
  }
  if (topic) {
    formData.append('topic', topic);
  }
  formData.append('level', level || 'beginner');
  formData.append('time_minutes', timeMinutes || 10);
  formData.append('goal', goal || 'understand');
  formData.append('language', language || 'en');
  if (teachingStyle) {
    formData.append('teaching_style', teachingStyle);
  }
  if (existingKnowledge) {
    formData.append('existing_knowledge', existingKnowledge);
  }
  if (forceWebSearch) {
    formData.append('force_web_search', 'true');
  }

  const res = await api.post('/api/lesson/create', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const switchLanguage = async ({ lessonId, newLanguage, currentSegmentIndex }) => {
  const res = await api.post(`/api/lesson/${lessonId}/switch-language`, {
    lesson_id: lessonId,
    new_language: newLanguage,
    current_segment_index: currentSegmentIndex || 0,
  });
  return res.data;
};

export const getLearnerProgress = async () => {
  const res = await api.get('/api/lesson/progress');
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

export const askTeacher = async ({ lessonId, segmentId, userQuery, language }) => {
  const res = await api.post('/api/interact/ask-teacher', {
    lesson_id: lessonId,
    segment_id: segmentId,
    user_query: userQuery,
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

export const getStudentProfile = async () => {
  const res = await api.get('/api/profile');
  return res.data;
};

export const updateStudentProfile = async (profileData) => {
  const res = await api.post('/api/profile', profileData);
  return res.data;
};

export const recordLessonCompletion = async ({ topic, durationMinutes, quizScorePercentage, language }) => {
  const res = await api.post('/api/profile/record-lesson', {
    topic,
    duration_minutes: durationMinutes,
    quiz_score_percentage: quizScorePercentage,
    language,
  });
  return res.data;
};

export const updateStudyPlan = async (studyPlan) => {
  const res = await api.post('/api/profile/study-plan', { study_plan: studyPlan });
  return res.data;
};

