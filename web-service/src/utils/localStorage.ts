import { UserProgress } from '../types';

const STORAGE_KEY = 'subway-story-progress';

export function getUserProgress(): UserProgress {
  if (typeof window === 'undefined') {
    return { viewedEpisodes: [], savedEpisodes: [] };
  }
  
  const data = localStorage.getItem(STORAGE_KEY);
  if (!data) {
    return { viewedEpisodes: [], savedEpisodes: [] };
  }
  
  try {
    return JSON.parse(data);
  } catch {
    return { viewedEpisodes: [], savedEpisodes: [] };
  }
}

export function saveUserProgress(progress: UserProgress) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

export function markEpisodeAsViewed(episodeId: string) {
  const progress = getUserProgress();
  if (!progress.viewedEpisodes.includes(episodeId)) {
    progress.viewedEpisodes.push(episodeId);
    saveUserProgress(progress);
  }
}

export function toggleSavedEpisode(episodeId: string) {
  const progress = getUserProgress();
  const index = progress.savedEpisodes.indexOf(episodeId);
  
  if (index === -1) {
    progress.savedEpisodes.push(episodeId);
  } else {
    progress.savedEpisodes.splice(index, 1);
  }
  
  saveUserProgress(progress);
}
