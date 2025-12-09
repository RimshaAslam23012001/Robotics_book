// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive guide to robotics, simulation, and AI integration',
  favicon: 'img/favicon.ico',

  url: 'https://your-book.github.io',
  baseUrl: '/',

  organizationName: 'your-organization',
  projectName: 'physical-ai-humanoid-robotics',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          path: './docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.js',

          // Only include markdown/mdx files from docs directory
          include: ['**/*.md', '**/*.mdx'],

          // Exclusions for docs plugin
          exclude: [
            '**/node_modules/**',
            '**/__pycache__/**',
            '**/*.py',
            '**/*.pyc',
            '**/*.xml',
            '**/*.launch',
            '**/*.launch.py',
            '**/*.sdf',
            '**/*.urdf',
            '**/*.egg-info/**',
            '**/*.prompt.md',
            '**/*.mdx~',
            '**/*.py~',
            '**/*.xml~',
            '**/venv/**',
            '**/env/**',
            '**/.specify/**',
            '**/.claude/**',
            '**/history/**',
            '**/specs/**',
            '**/ros2_ws/**',
            '**/build/**',
            '**/dist/**',
            '**/temp/**',
            '**/tmp/**',
            '**/vercel-deploy/**',
            '**/temp_dirs/**'
          ],

          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig: ({
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Robotics Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: Robot Communication',
              to: '/docs/module-1/communication-architecture',
            },
            {
              label: 'Module 2: Virtual Environment',
              to: '/docs/module-2/virtual-environment',
            },
            {
              label: 'Module 3: Perception & Navigation',
              to: '/docs/module-3/perception-navigation',
            },
            {
              label: 'Module 4: VLA System',
              to: '/docs/module-4/vla-system',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  }),

  plugins: [
    './src/plugins/exclude-files-plugin.js'
  ],

};

export default config;
