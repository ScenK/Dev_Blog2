define(function(require, exports, module) {

   var $            = require('jquery'),
       alerts       = require('alerts'),
       dataTable    = require('dataTable'),
       wysiwyg      = require('wysiwyg'),
       wysiwygLink  = require('wysiwygLink'),
       fineUploader = require('fineUploader'),
       chosen       = require('chosen');

  //********************* TABLE (NEWS) *********************//
  $('#example').dataTable({
    "sPaginationType": "full_numbers"
  });

  //*********************  FORMS   *********************//
  $(".chzn-select").chosen(); 

  //*******************  TAGS  *******************//
  if($('input[name="tags"]').length > 0 ){
    var str = $('input[name="tags"]').val(); str = str.replace(/\,$/, '');
    $('input[name="tags"]').val(str);
  }

  //*******************  CATEGORIES  *******************//
  $('#categories_select').change(function(){
    var self = $(this);
    if(self.val() === '创建新分类'){
      jPrompt('新分类名称:', '', '添加新分类', function(cat) {
        $('#categories_select :selected').text(cat);
        $('#categories_select').append('<option>创建新分类</option>');
        $(".chzn-select").trigger("liszt:updated");
      });
    }
  });

  //*******************  EDITOR  *******************//
  $('#wysiwyg_target').wysiwyg({
    autoGrow         : true,
    rmUnusedControls : true,
    createLink       : true,
    controls         : {
      bold                : { visible : true },
      italic              : { visible : true },
      strikeThrough       : { visible : true },
      code                : { visible : true },
      underline           : { visible : true },
      insertOrderedList   : { visible : true },
      insertUnorderedList : { visible : true },
      createLink          : { visible : true },
      insertImage         : { 
        visible : true,
        exec: function () { 
        }
      }
    }
  });

  //*************  PHOTO ADD ALERT  ***************//
  $('.insertImage').fineUploader({
    autoUpload: true,
    uploadButtonText: "",
    request: {
      endpoint: "/admin/diary/add-photo"
    }
  }).on('complete', function(event, id, filename, responseJSON){
    $('#wysiwyg_target').wysiwyg('insertHtml', '<img src="' + responseJSON.url + '">');
  });

});
