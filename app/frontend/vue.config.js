if (process.env.API_TARGET) {
  console.log(`Targetting the API ${process.env.API_TARGET}`)
}

module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000
      }
    }
  },
  devServer: {
    proxy: {
      '^/api/': {
        target: process.env.API_TARGET || 'http://backend:8000/',
        pathRewrite: {
          '^/api': '/gwells/api/v2'
        }
      }
    }
  }
}
