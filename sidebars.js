// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'quickstart',
      ],
    },
    {
      type: 'category',
      label: 'Modules',
      items: [
        'module-1/communication-architecture',
        'module-2/virtual-environment',
        'module-3/perception-navigation',
        'module-4/vla-system',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: [
        'capstone/integrated-project',
      ],
    },
    {
      type: 'category',
      label: 'System Validation',
      items: [
        'validation',
        'troubleshooting',
      ],
    },
  ],
};

export default sidebars;