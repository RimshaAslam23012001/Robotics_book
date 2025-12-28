// @ts-check
import { themes as prismThemes } from "prism-react-renderer";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Physical AI & Humanoid Robotics",
  tagline: "A comprehensive guide to robotics, simulation, and AI integration",
  favicon: "img/favicon.ico",

  url: "https://RimshaAslam23012001.github.io",
  baseUrl: "/",

  organizationName: "RimshaAslam23012001",
  projectName: "Robotics_book",

  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          path: "./docs",
          routeBasePath: "/",
          sidebarPath: "./sidebars.js",
          include: ["**/*.md", "**/*.mdx"],
          exclude: [
            "**/node_modules/**",
            "**/__pycache__/**",
            "**/*.py",
            "**/*.pyc",
            "**/*.xml",
            "**/*.launch",
            "**/*.launch.py",
            "**/*.sdf",
            "**/*.urdf",
            "**/*.egg-info/**",
            "**/*.prompt.md",
            "**/*.mdx~",
            "**/*.py~",
            "**/*.xml~",
            "**/venv/**",
            "**/env/**",
            "**/.specify/**",
            "**/.claude/**",
            "**/history/**",
            "**/specs/**",
            "**/ros2_ws/**",
            "**/build/**",
            "**/dist/**",
            "**/temp/**",
            "**/tmp/**",
            "**/vercel-deploy/**",
            "**/temp_dirs/**",
            "**/simulation/**",
          ],
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
        pages: {
          path: "./src/pages",
        },
      },
    ],
  ],

  themeConfig: {
    image: "img/OIP.jpeg",
    navbar: {
      title: "Physical AI & Humanoid Robotics",
      logo: {
        alt: "Physical AI & Humanoid Robotics Logo",
        src: "img/OIP.jpeg",
      },
      style: "dark",
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "BOOK",
        },
        {
          href: "https://github.com/RimshaAslam23012001/Robotics_book",
          label: "GITHUB",
          position: "right",
        },
        {
          type: 'html',
          position: 'right',
          value: '<span id="auth-buttons-placeholder"></span>',
        },
        {
          type: 'html',
          position: 'right',
          value: '<button id="translation-toggle-btn" class="navbar__link translation-toggle-btn">اردو ترجمہ</button>',
        },

      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "GETTING STARTED",
          items: [
            { label: "Introduction", to: "/intro" },
            { label: "Quickstart", to: "/quickstart" },
            { label: "About", to: "/about" },
          ],
        },
        {
          title: "ASSISTANT",
          items: [{ label: "Chat with AI", to: "/chat" }],
        },
        {
          title: "CORE MODULES",
          items: [
            { label: "Module 1: Communication", to: "/module-1/communication-architecture" },
            { label: "Module 2: Environment", to: "/module-2/virtual-environment" },
            { label: "Module 3: Navigation", to: "/module-3/perception-navigation" },
            { label: "Module 4: VLA System", to: "/module-4/vla-system" },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Physical AI & Humanoid Robotics`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },

  plugins: ["./src/plugins/exclude-files-plugin.js"],

  clientModules: [
    require.resolve('./src/utils/translationHandler.js'),
  ],
};

export default config;
