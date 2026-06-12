export type Project = {
  id: string;
  name: string;
  owner: string;
  rank: number | null;
  page: number | null;
  stars: string;
  starsValue: number;
  forks: string;
  forksValue: number;
  language: string;
  category: string;
  categoryId: string;
  hotComment: string;
  description: string;
  detailUrl: string;
  avatarUrl: string;
  sourceUrl: string;
  scrapedAt: string;
};

export type ProjectDataset = {
  generatedAt: string;
  total: number;
  imports: Array<{
    directory: string;
    file: string;
    categoryId: string;
    selectedCategory: string;
    count: number;
  }>;
  categories: string[];
  languages: string[];
  projects: Project[];
};

export type SortKey = 'relevance' | 'stars' | 'forks' | 'name';
