const path = require('path');

module.exports = {
  entry: './static/main/js/chatbot/index.js',  // Make sure this path is correct
  output: {
    filename: 'chatbot-bundle.js',
    path: path.resolve(__dirname, 'static/main/js'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
};