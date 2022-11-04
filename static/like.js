// Like post without reloading page
$('.like-form').submit(function(e){
  e.preventDefault()

  const post_id = $(this).attr('id')

  const url = $(this).attr('action')

  let res;
  const likes = $(`.like-count${post_id}`).text()
  const trimCount = parseInt(likes)

  $.ajax({
      type: 'POST',
      url: url,
      data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'post_id':post_id,
      },
      success: function(response) {
        console.log(response)
          if(response['like_added']) {
              $(`.like-btn${post_id}`).removeClass('black')
              $(`.like-btn${post_id}`).addClass('negative')
              res = trimCount + 1
          } else {
              $(`.like-btn${post_id}`).removeClass('negative')
              $(`.like-btn${post_id}`).addClass('black')
              res = trimCount - 1
          }

          $(`.like-count${post_id}`).text(res)
      },
      error: function(response) {
          console.log('error', response)
      }
  })
})
