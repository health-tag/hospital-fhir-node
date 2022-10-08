const TsconfigPathsPlugin = require("tsconfig-paths-webpack-plugin");

module.exports = {
  style: {
    postcss: {
      loaderOptions: (postcssLoaderOptions) => {
        postcssLoaderOptions.postcssOptions.config = true;
        return postcssLoaderOptions;
      },
    },
  },
  plugins: [
    {
      plugin: {
        overrideWebpackConfig: ({ webpackConfig }) => {
          webpackConfig.resolve.plugins.push(new TsconfigPathsPlugin());
          return webpackConfig;
        },
      },
    },
  ],
};
