$(document).ready(function(){

    $('.watch-video-like-form').submit(function(e){
        e.preventDefault();
        const video_id=$('.like-button').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method:"POST",
            url:url,
            headers:{'X-CSRFToken': token},
            data:{
                'video_id': video_id
            },
            success:function(response){
                if(response.like===true){
                    $('.like-icon').removeClass('material-icons-outlined')
                    $('.like-icon').addClass('material-icons')
                    $('.dislike-icon').removeClass('material-icons')
                    $('.dislike-icon').addClass('material-icons-outlined')
                  }else{
                    $('.like-icon').removeClass('material-icons')
                    $('.like-icon').addClass('material-icons-outlined')
                  }

                    like=$('#total-likes').text(response.total_likes)
                    parseInt(like)

                    dislike=$('#total-dislikes').text(response.total_dislikes)
                    parseInt(dislike)

                    console.log(response)
            },
            error:function(response){
                console.log('Failed', response)
            }
        })
    })

    $('.watch-video-dislike-form').submit(function(e){
        e.preventDefault();
        const video_id=$('.dislike-button').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method:"POST",
            url:url,
            headers:{'X-CSRFToken': token},
            data:{
                'video_id': video_id
            },
            success:function(response){
                if(response.dislike===true){
                    $('.dislike-icon').removeClass('material-icons-outlined')
                    $('.dislike-icon').addClass('material-icons')
                    $('.like-icon').removeClass('material-icons')
                    $('.like-icon').addClass('material-icons-outlined')
                  }else{
                    $('.dislike-icon').removeClass('material-icons')
                    $('.dislike-icon').addClass('material-icons-outlined')
                  }

                    dislikes=$('#total-dislikes').text(response.total_dislikes)
                    parseInt(dislikes)

                    likes=$('#total-likes').text(response.total_likes)
                    parseInt(likes)

                    console.log(response)
            },
            error:function(response){
                console.log('Failed', response)
            }
        })
    })
})