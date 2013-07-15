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
    'chosen' : {
      src: 'chosen.jquery.min.js',
      exports: 'chosen'
    },
    'tipTip' : {
      src: 'jquery.tipTip.minified.js',
      exports: 'tipTip'
    },
    'wysiwyg' : {
      src: 'editor/jquery.wysiwyg.js',
      exports: 'wysiwyg'
    },
    'wysiwygLink' : {
      src: 'editor/wysiwyg.link.js',
      exports: 'wysiwygLink'
    },
    'fineUploader' : {
      src: 'fineuploader/fineuploader.min.js',
      exports: 'fineUploader'
    },
    'alerts' : {
      src: 'jquery.alerts.js',
      exports: 'alerts'
    },
    'uploadifive': {
      src: 'uploadifive/jquery.uploadifive.min.js',
      exports: 'uploadifive'
    }
  }

});
