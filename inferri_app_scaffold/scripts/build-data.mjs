import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const outDir = path.join(root, 'public', 'data');
const outFile = path.join(outDir, 'projects.json');

function parseCompactNumber(value) {
  if (value == null || value === '') return 0;
  const text = String(value).trim().replace(/,/g, '');
  const match = text.match(/^(\d+(?:\.\d+)?)([KkMm])?$/);
  if (!match) return 0;
  const number = Number(match[1]);
  const unit = match[2]?.toLowerCase();
  if (unit === 'm') return Math.round(number * 1_000_000);
  if (unit === 'k') return Math.round(number * 1_000);
  return number;
}

function projectIdFromUrl(url) {
  const match = String(url || '').match(/\/projects\/([^/?#]+)/);
  return match?.[1] ?? null;
}

function normalizeProject(project, source) {
  const detailUrl = project.detailUrl || '';
  const id = project.id || projectIdFromUrl(detailUrl) || `${project.owner || 'unknown'}:${project.name || 'unknown'}`;
  const category = project.category || source.selectedCategory?.replace(/\d+$/, '') || '未分类';
  return {
    id,
    name: project.name || '',
    owner: project.owner || '',
    rank: project.rank ?? null,
    page: project.page ?? project.scrapedFromPage ?? null,
    stars: project.stars || '',
    starsValue: parseCompactNumber(project.stars),
    forks: project.forks || '',
    forksValue: parseCompactNumber(project.forks),
    language: project.language || '',
    category,
    categoryId: source.categoryId || project.categoryId || '',
    hotComment: project.hotComment || '',
    description: project.description || '',
    detailUrl,
    avatarUrl: project.avatarUrl || '',
    sourceUrl: project.scrapedFromUrl || source.sourceUrl || source.sourceStartUrl || '',
    scrapedAt: source.scrapedAt || ''
  };
}

const directories = fs
  .readdirSync(root, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && entry.name.startsWith('category_'))
  .map((entry) => path.join(root, entry.name));

const projectsById = new Map();
const imports = [];

for (const directory of directories) {
  const jsonFile = fs.readdirSync(directory).find((file) => file.endsWith('.json'));
  if (!jsonFile) continue;
  const filePath = path.join(directory, jsonFile);
  const source = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const projects = Array.isArray(source.projects) ? source.projects : [];
  imports.push({
    directory: path.basename(directory),
    file: jsonFile,
    categoryId: source.categoryId || '',
    selectedCategory: source.selectedCategory || '',
    count: projects.length
  });
  for (const project of projects) {
    const normalized = normalizeProject(project, source);
    projectsById.set(normalized.id, {
      ...projectsById.get(normalized.id),
      ...normalized
    });
  }
}

const projects = [...projectsById.values()].sort((a, b) => {
  if (b.starsValue !== a.starsValue) return b.starsValue - a.starsValue;
  return a.name.localeCompare(b.name, 'zh-CN');
});

const categories = [...new Set(projects.map((project) => project.category).filter(Boolean))].sort((a, b) =>
  a.localeCompare(b, 'zh-CN')
);
const languages = [...new Set(projects.map((project) => project.language).filter(Boolean))].sort((a, b) =>
  a.localeCompare(b, 'zh-CN')
);

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(
  outFile,
  JSON.stringify(
    {
      generatedAt: new Date().toISOString(),
      total: projects.length,
      imports,
      categories,
      languages,
      projects
    },
    null,
    2
  ),
  'utf8'
);

console.log(`Wrote ${projects.length} projects to ${path.relative(root, outFile)}`);
