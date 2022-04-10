const { loaderByName, addBeforeLoader, getLoader } = require("@craco/craco");
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
  webpack: {
    configure: (webpackConfig) => {
      // mdx-loader
      webpackConfig.module.rules[1].oneOf.unshift({
        test: /\.mdx?$/,
        use: [
          {
            loader: "@mdx-js/loader",
            /** @type {import('@mdx-js/loader').Options} */
            options: {},
          },
        ],
      });

      // Workaround for bug https://github.com/facebook/create-react-app/issues/12166
      // file-loader
      webpackConfig.module.rules[1].oneOf.at(-1).exclude = [
        /^$/,
        /\.(js|mjs|jsx|ts|tsx|mdx)$/,
        /\.html$/,
        /\.json$/,
      ];
      return webpackConfig;
    },
  },
  plugins: [
    {
      plugin: {
        overrideWebpackConfig: ({ webpackConfig }) => {
          webpackConfig.resolve.plugins.push(new TsconfigPathsPlugin({}));
          return webpackConfig;
        },
      },
    },
  ],
};
