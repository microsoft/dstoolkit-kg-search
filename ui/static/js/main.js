// Global Variables
var loading_icon =
  '<div style="height:200px;"><div class="h-center h-100 v-center"><i class="fa fa-spinner fa-spin fa-5x"></i></div></div>';


// AJAX POST: Asynchrnous server communication using JSON strings
$(function() {
  $('button#search_btn').bind('click', function() {
    var form_data = JSON.stringify({
      input_kg_check: $('#form-check').is(":checked"),
      input_keywords: $('#form-keywords').val()
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/search',
      type: 'POST',
      contentType: 'application/json;charset=UTF-8',
      data: form_data,
      dataType: 'json',
      beforeSend: function() {
        // show spinner loader
        $('#results').html(loading_icon);
      }
    }).done(function(response) {
        // render successful search
        $('#results').html(response.data);
    });
  });
});

