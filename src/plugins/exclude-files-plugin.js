// @ts-check

/**
 * @param {import('@docusaurus/types').DocusaurusConfig} context
 * @returns {import('@docusaurus/types').Plugin}
 */
module.exports = function excludeFilesPlugin(context) {
  return {
    name: 'exclude-files-plugin',
    configureWebpack(config, isServer, utils) {
      return {
        module: {
          rules: [
            {
              test: /\.(py|pyc|xml|launch|sdf|urdf|egg-info|prompt\.md|html)$/i,
              type: 'asset/resource',
              generator: {
                filename: 'assets/ignored/[name].[hash:8][ext]'
              }
            },
          ],
        },
      };
    },
  };
};