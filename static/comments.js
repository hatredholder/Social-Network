// Focus input form
$( document ).ready(function() {
    $(".cmt_btn").click(function () {
      // Get form id from button
      formId = $(this).attr("class").split(/\s+/)[1]

      // Focus input from form
      $(`.form${formId}`)[0][2].focus()
    });
})
