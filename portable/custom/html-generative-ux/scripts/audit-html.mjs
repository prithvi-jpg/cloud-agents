#!/usr/bin/env node

import {readdir, readFile, stat, writeFile} from 'node:fs/promises';
import path from 'node:path';

const args = process.argv.slice(2);
const outputIndex = args.indexOf('--output');
const outputPath = outputIndex >= 0 ? args[outputIndex + 1] : null;
const roots = args.filter((arg, index) => {
  if (arg === '--output') return false;
  if (outputIndex >= 0 && index === outputIndex + 1) return false;
  return true;
});

if (roots.length === 0) {
  console.error('Usage: audit-html.mjs <root> [<root> ...] [--output report.json]');
  process.exit(2);
}

const count = (text, pattern) => (text.match(pattern) || []).length;

const cleanText = (value) =>
  value
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/\s+/g, ' ')
    .trim();

const uniqueMatches = (text, pattern, group = 1, limit = 40) =>
  [...new Set([...text.matchAll(pattern)].map((match) => match[group]).filter(Boolean))].slice(0, limit);

const getTagText = (html, tag) =>
  [...html.matchAll(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'gi'))]
    .map((match) => cleanText(match[1]))
    .filter(Boolean)
    .slice(0, 30);

const walk = async (root) => {
  const files = [];
  const visit = async (current) => {
    const entries = await readdir(current, {withFileTypes: true});
    for (const entry of entries) {
      if (entry.name === '.git') continue;
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) await visit(full);
      if (entry.isFile() && entry.name.toLowerCase().endsWith('.html')) files.push(full);
    }
  };
  await visit(root);
  return files.sort();
};

const inspectFile = async (root, file) => {
  const html = await readFile(file, 'utf8');
  const fileStat = await stat(file);
  const cssBlocks = [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]);
  const scriptBlocks = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((match) => match[1]);
  const css = cssBlocks.join('\n');
  const js = scriptBlocks.join('\n');
  const withoutData = html.replace(/data:[^"'()\s>]+/gi, 'data:[omitted]');
  const titleMatch = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);

  const eventTypes = uniqueMatches(js, /addEventListener\(\s*['"]([^'"]+)['"]/g);
  const cssVariables = uniqueMatches(css, /(--[a-z0-9-_]+)\s*:/gi);
  const fontFamilies = uniqueMatches(css, /font-family\s*:\s*([^;}{]+)/gi);
  const externalHosts = uniqueMatches(
    withoutData,
    /https?:\/\/([^/"'\s)<>]+)/gi,
  );

  return {
    repository: path.basename(root),
    path: path.relative(root, file).replaceAll(path.sep, '/'),
    bytes: fileStat.size,
    lines: html.split(/\r?\n/).length,
    title: titleMatch ? cleanText(titleMatch[1]) : '',
    headings: {
      h1: getTagText(withoutData, 'h1'),
      h2: getTagText(withoutData, 'h2'),
      h3: getTagText(withoutData, 'h3'),
    },
    structure: {
      sections: count(withoutData, /<section\b/gi),
      articles: count(withoutData, /<article\b/gi),
      navs: count(withoutData, /<nav\b/gi),
      asides: count(withoutData, /<aside\b/gi),
      dialogs: count(withoutData, /<dialog\b/gi),
      details: count(withoutData, /<details\b/gi),
      tables: count(withoutData, /<table\b/gi),
      lists: count(withoutData, /<(?:ul|ol)\b/gi),
      codeBlocks: count(withoutData, /<(?:pre|code)\b/gi),
    },
    media: {
      svg: count(withoutData, /<svg\b/gi),
      canvas: count(withoutData, /<canvas\b/gi),
      images: count(withoutData, /<img\b/gi),
      video: count(withoutData, /<video\b/gi),
      audio: count(withoutData, /<audio\b/gi),
      dataUris: count(html, /data:/gi),
      externalHosts,
    },
    controls: {
      buttons: count(withoutData, /<button\b/gi),
      links: count(withoutData, /<a\b/gi),
      inputs: count(withoutData, /<input\b/gi),
      selects: count(withoutData, /<select\b/gi),
      textareas: count(withoutData, /<textarea\b/gi),
      contentEditable: count(withoutData, /contenteditable\b/gi),
    },
    accessibility: {
      ariaAttributes: count(withoutData, /\saria-[a-z-]+\s*=/gi),
      roles: uniqueMatches(withoutData, /\srole\s*=\s*['"]([^'"]+)['"]/gi),
      altAttributes: count(withoutData, /\salt\s*=/gi),
      labels: count(withoutData, /<label\b/gi),
    },
    css: {
      blocks: cssBlocks.length,
      bytes: Buffer.byteLength(css),
      variables: cssVariables,
      fontFamilies,
      mediaQueries: count(css, /@media\b/gi),
      keyframes: uniqueMatches(css, /@keyframes\s+([a-z0-9-_]+)/gi),
      animationDeclarations: count(css, /\banimation(?:-name)?\s*:/gi),
      transitionDeclarations: count(css, /\btransition(?:-property)?\s*:/gi),
      gridDeclarations: count(css, /display\s*:\s*grid/gi),
      flexDeclarations: count(css, /display\s*:\s*flex/gi),
      absoluteDeclarations: count(css, /position\s*:\s*absolute/gi),
      fixedDeclarations: count(css, /position\s*:\s*fixed/gi),
      stickyDeclarations: count(css, /position\s*:\s*sticky/gi),
      clampUses: count(css, /\bclamp\(/gi),
      colorMixUses: count(css, /\bcolor-mix\(/gi),
    },
    javascript: {
      blocks: scriptBlocks.length,
      bytes: Buffer.byteLength(js),
      eventTypes,
      querySelectors: count(js, /querySelector(?:All)?\(/g),
      localStorageUses: count(js, /\blocalStorage\b/g),
      requestAnimationFrameUses: count(js, /\brequestAnimationFrame\(/g),
      observers: uniqueMatches(js, /\b([A-Z][A-Za-z]+Observer)\b/g),
      keyboardLogic: count(js, /\b(?:keydown|keyup|KeyboardEvent)\b/g),
      pointerLogic: count(js, /\b(?:pointerdown|pointermove|pointerup|PointerEvent)\b/g),
      dragLogic: count(js, /\b(?:dragstart|dragover|drop|draggable)\b/g),
      timers: count(js, /\b(?:setTimeout|setInterval)\(/g),
    },
    conventions: {
      classNames: uniqueMatches(withoutData, /\bclass\s*=\s*['"]([^'"]+)['"]/gi, 1, 60),
      dataAttributes: uniqueMatches(withoutData, /\s(data-[a-z0-9-]+)(?:\s*=|\s|>)/gi, 1, 40),
      usesSlides: /\bslide(?:s|deck)?\b/i.test(withoutData),
      usesEditor: /\beditor\b/i.test(withoutData),
      usesDashboard: /\bdashboard\b/i.test(withoutData),
      usesTimeline: /\btimeline\b/i.test(withoutData),
      usesTabs: /\btab(?:s|list|panel)?\b/i.test(withoutData),
    },
  };
};

const files = [];
for (const rootArgument of roots) {
  const root = path.resolve(rootArgument);
  const htmlFiles = await walk(root);
  for (const file of htmlFiles) files.push(await inspectFile(root, file));
}

const report = {
  generatedAt: new Date().toISOString(),
  roots: roots.map((root) => path.resolve(root)),
  fileCount: files.length,
  totalBytes: files.reduce((sum, file) => sum + file.bytes, 0),
  totalLines: files.reduce((sum, file) => sum + file.lines, 0),
  files,
};

const serialized = `${JSON.stringify(report, null, 2)}\n`;
if (outputPath) {
  await writeFile(path.resolve(outputPath), serialized, 'utf8');
}
process.stdout.write(serialized);
