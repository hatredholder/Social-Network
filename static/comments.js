// Open / hide post comment
$( document ).ready(function() {
    let display = false
    $(".cmt_btn").click(function () {
        if (display===false) {
            $(this).next(".comment-box").show("slow");
            display=true
        } else {
            $(this).next(".comment-box").hide("slow");
            display=false
        }  
    });
})
