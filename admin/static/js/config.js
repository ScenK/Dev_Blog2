seajs.config({
  charset: 'utf-8',

  //Debug
  debug: true,

  //Enable plugins
  plugins: ['shim'],

  // Configure alias
  alias: {
    'jquery': {
      src: 'jquery-1.7.1.min.js',
      exports: 'jQuery'
    },
    'dataTable' : {
      src: 'jquery.dataTables.min.js',
      exports: 'dataTable'
    },
    'autoResize' : {
      src: 'autoresize.jquery.min.js',
      exports: 'autoresize'
    },
    'chosen' : {
      src: 'chosen.jquery.min.js',
      exports: 'chosen'
    },
    'alerts' : {
      src: 'jquery.alerts.js',
      exports: 'alerts'
    }
  }

});
