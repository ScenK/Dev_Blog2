define(function(require, exports, module) {

   var $          = require('jquery'),
       autoResize = require('autoResize'),
       alerts     = require('alerts'),
       dataTable  = require('dataTable'),
       wysiwyg    = require('wysiwyg'),
       wysiwygLink= require('wysiwygLink'),
       chosen     = require('chosen');

  //********************* TABLE (NEWS) *********************//
  $('#example').dataTable({
    "sPaginationType": "full_numbers"
  });

  //********************* autorisize *********************//
	$('textarea.resize-text').autoResize();

  $("input[type=file]").change(function(){
    $(this).parents(".uploader").find(".filename").val($(this).val());
  });

	$("input[type=file]").each(function(){
    if($(this).val()==""){
      $(this).parents(".uploader").find(".filename").val("No file selected...");
    }
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
        exec: function () { alert (7); }
      }
    }
  });

});
