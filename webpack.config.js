const path = require('path');

module.exports = {
  entry: {
    signup: './app/static/js/signup.js',
    adminLogin: './app/static/js/adminLogin.js',
    adminDashboard: './app/static/js/adminDashboard.js'
  },
  output: {
    filename: '[name].bundle.js',
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
  // Add this for better debugging
  devtool: 'source-map'
};