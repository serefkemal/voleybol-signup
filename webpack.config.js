const path = require('path');

module.exports = {
  entry: './app/static/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'app/static/dist'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      '@': path.resolve(__dirname, 'app/static/js'),
    },
  },
};