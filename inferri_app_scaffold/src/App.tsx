import { useEffect, useMemo, useState } from 'react';
import {
  ArrowDownAZ,
  ArrowUpRight,
  BadgeInfo,
  Database,
  ExternalLink,
  Filter,
  Github,
  RotateCcw,
  Search,
  Star,
  X
} from 'lucide-react';
import type { Project, ProjectDataset, SortKey } from './types';

const minimumStarsOptions = [
  { label: '不限', value: 0 },
  { label: '>= 500', value: 500 },
  { label: '>= 2K', value: 2_000 },
  { label: '>= 10K', value: 10_000 },
  { label: '>= 50K', value: 50_000 }
];

const sortOptions: Array<{ label: string; value: SortKey }> = [
  { label: '相关度', value: 'relevance' },
  { label: 'Stars', value: 'stars' },
  { label: 'Forks', value: 'forks' },
  { label: '名称', value: 'name' }
];

function tokenize(text: string) {
  return text
    .toLowerCase()
    .split(/\s+/)
    .map((part) => part.trim())
    .filter(Boolean);
}

function formatNumber(value: number) {
  return new Intl.NumberFormat('zh-CN').format(value);
}

function projectSearchText(project: Project) {
  return [
    project.name,
    project.owner,
    project.language,
    project.category,
    project.hotComment,
    project.description
  ]
    .join(' ')
    .toLowerCase();
}

function scoreProject(project: Project, query: string) {
  if (!query.trim()) return 0;
  const haystack = projectSearchText(project);
  const terms = tokenize(query);
  let score = 0;
  for (const term of terms) {
    if (project.name.toLowerCase().includes(term)) score += 8;
    if (project.owner.toLowerCase().includes(term)) score += 5;
    if (project.category.toLowerCase().includes(term)) score += 4;
    if (project.language.toLowerCase().includes(term)) score += 3;
    if (haystack.includes(term)) score += 1;
  }
  return score;
}

function ProjectCard({ project }: { project: Project }) {
  return (
    <article className="project-card">
      <div className="project-card__top">
        <img
          className="project-card__avatar"
          src={project.avatarUrl}
          alt=""
          loading="lazy"
          referrerPolicy="no-referrer"
        />
        <div className="project-card__identity">
          <div className="project-card__name-row">
            <h2>{project.name}</h2>
            {project.rank ? <span className="rank">#{project.rank}</span> : null}
          </div>
          <div className="owner">{project.owner}</div>
        </div>
      </div>

      {project.hotComment ? <p className="hot-comment">{project.hotComment}</p> : null}
      {project.description ? <p className="description">{project.description}</p> : null}

      <div className="project-card__meta">
        <span title={`${project.starsValue} stars`}>
          <Star size={14} />
          {project.stars || formatNumber(project.starsValue)}
        </span>
        <span title={`${project.forksValue} forks`}>
          <Github size={14} />
          {project.forks || formatNumber(project.forksValue)}
        </span>
        {project.language ? <span>{project.language}</span> : null}
        <span className="category">{project.category}</span>
      </div>

      <div className="project-card__actions">
        <a href={project.detailUrl} target="_blank" rel="noreferrer">
          原站详情
          <ArrowUpRight size={14} />
        </a>
      </div>
    </article>
  );
}

function FilterButton({
  label,
  active,
  onClick,
  count
}: {
  label: string;
  active: boolean;
  onClick: () => void;
  count?: number;
}) {
  return (
    <button className={active ? 'filter-chip filter-chip--active' : 'filter-chip'} type="button" onClick={onClick}>
      <span>{label}</span>
      {typeof count === 'number' ? <span className="filter-chip__count">{count}</span> : null}
    </button>
  );
}

export function App() {
  const [dataset, setDataset] = useState<ProjectDataset | null>(null);
  const [loadError, setLoadError] = useState('');
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [language, setLanguage] = useState('');
  const [minimumStars, setMinimumStars] = useState(0);
  const [sortKey, setSortKey] = useState<SortKey>('relevance');

  useEffect(() => {
    fetch('/data/projects.json')
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<ProjectDataset>;
      })
      .then(setDataset)
      .catch((error) => {
        setLoadError(error instanceof Error ? error.message : String(error));
      });
  }, []);

  const categoryCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const project of dataset?.projects ?? []) {
      counts.set(project.category, (counts.get(project.category) ?? 0) + 1);
    }
    return counts;
  }, [dataset]);

  const languageCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const project of dataset?.projects ?? []) {
      if (!project.language) continue;
      counts.set(project.language, (counts.get(project.language) ?? 0) + 1);
    }
    return counts;
  }, [dataset]);

  const filteredProjects = useMemo(() => {
    const projects = dataset?.projects ?? [];
    const terms = tokenize(query);
    return projects
      .map((project) => ({ project, score: scoreProject(project, query) }))
      .filter(({ project, score }) => {
        if (category && project.category !== category) return false;
        if (language && project.language !== language) return false;
        if (project.starsValue < minimumStars) return false;
        if (terms.length > 0 && score <= 0) return false;
        return true;
      })
      .sort((left, right) => {
        if (sortKey === 'relevance' && query.trim()) {
          if (right.score !== left.score) return right.score - left.score;
          return right.project.starsValue - left.project.starsValue;
        }
        if (sortKey === 'stars' || (sortKey === 'relevance' && !query.trim())) {
          return right.project.starsValue - left.project.starsValue;
        }
        if (sortKey === 'forks') return right.project.forksValue - left.project.forksValue;
        return left.project.name.localeCompare(right.project.name, 'zh-CN');
      })
      .map(({ project }) => project);
  }, [category, dataset, language, minimumStars, query, sortKey]);

  const resetFilters = () => {
    setQuery('');
    setCategory('');
    setLanguage('');
    setMinimumStars(0);
    setSortKey('relevance');
  };

  if (loadError) {
    return (
      <main className="app-shell app-shell--center">
        <div className="empty-state">
          <BadgeInfo size={24} />
          <h1>数据加载失败</h1>
          <p>请先运行 `npm run build:data` 生成 `public/data/projects.json`。</p>
          <code>{loadError}</code>
        </div>
      </main>
    );
  }

  if (!dataset) {
    return (
      <main className="app-shell app-shell--center">
        <div className="loading">正在加载项目数据...</div>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Database size={22} />
          <div>
            <div className="brand__title">Inferri Local</div>
            <div className="brand__subtitle">已汇总 {dataset.total} 个项目</div>
          </div>
        </div>

        <section className="filter-section">
          <div className="section-title">
            <Filter size={16} />
            分类
          </div>
          <div className="filter-list">
            <FilterButton
              label="全部"
              count={dataset.projects.length}
              active={!category}
              onClick={() => setCategory('')}
            />
            {dataset.categories.map((item) => (
              <FilterButton
                key={item}
                label={item}
                count={categoryCounts.get(item)}
                active={category === item}
                onClick={() => setCategory(item === category ? '' : item)}
              />
            ))}
          </div>
        </section>

        <section className="filter-section">
          <div className="section-title">
            <ArrowDownAZ size={16} />
            语言
          </div>
          <div className="filter-list filter-list--compact">
            <FilterButton label="不限" active={!language} onClick={() => setLanguage('')} />
            {dataset.languages.map((item) => (
              <FilterButton
                key={item}
                label={item}
                count={languageCounts.get(item)}
                active={language === item}
                onClick={() => setLanguage(item === language ? '' : item)}
              />
            ))}
          </div>
        </section>
      </aside>

      <section className="content">
        <header className="toolbar">
          <div className="search-box">
            <Search size={18} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜索项目、owner、介绍、分类..."
            />
            {query ? (
              <button className="icon-button" type="button" aria-label="清空搜索" onClick={() => setQuery('')}>
                <X size={16} />
              </button>
            ) : null}
          </div>

          <div className="toolbar-controls">
            <select value={minimumStars} onChange={(event) => setMinimumStars(Number(event.target.value))}>
              {minimumStarsOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  Stars {option.label}
                </option>
              ))}
            </select>
            <select value={sortKey} onChange={(event) => setSortKey(event.target.value as SortKey)}>
              {sortOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  排序：{option.label}
                </option>
              ))}
            </select>
            <button className="reset-button" type="button" onClick={resetFilters}>
              <RotateCcw size={16} />
              重置
            </button>
          </div>
        </header>

        <div className="result-summary">
          <div>
            <strong>{filteredProjects.length}</strong>
            <span> / {dataset.total} 个项目</span>
          </div>
          <div className="result-summary__meta">
            数据生成：{new Date(dataset.generatedAt).toLocaleString('zh-CN')}
          </div>
        </div>

        <div className="active-filters">
          {category ? <span>分类：{category}</span> : null}
          {language ? <span>语言：{language}</span> : null}
          {minimumStars > 0 ? <span>Stars &gt;= {formatNumber(minimumStars)}</span> : null}
          {query ? <span>关键词：{query}</span> : null}
        </div>

        {filteredProjects.length > 0 ? (
          <div className="project-grid">
            {filteredProjects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <Search size={24} />
            <h1>没有匹配项目</h1>
            <p>换个关键词，或放宽分类、语言、Stars 条件。</p>
          </div>
        )}

        <footer className="footer">
          <a href="https://inferri.com/zh-CN/projects" target="_blank" rel="noreferrer">
            打开 Inferri 原站
            <ExternalLink size={14} />
          </a>
        </footer>
      </section>
    </main>
  );
}
