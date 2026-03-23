export interface Station {
  id: string;
  name: string;
  position: { x: number; y: number };
}

export interface Episode {
  id: string;
  stationId: string;
  title: string;
  content: string;
  imageUrl: string;
}

export interface UserProgress {
  viewedEpisodes: string[]; // episode ids
  savedEpisodes: string[]; // episode ids
}
