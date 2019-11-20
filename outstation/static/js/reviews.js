(
  function () {
  Dropzone.autoDiscover = false;
  var dropzones=[];
  var imageDropzone = new Dropzone('div#reviewImagesDropzone', {
      url: '/review/',
      autoProcessQueue: false,
      autoDiscover: false,
      uploadMultiple: true,
      parallelUploads: 2,
      maxFiles: 10,
      paramName: "images",
      addRemoveLinks: true,
      retryChunks: true,
      parallelChunkUploads: true,
      thumbnailWidth : 80,
      thumbnailheight : 80,
      acceptedFiles: 'image/jpeg, image/jpg, image/png'

  });

 imageDropzone.on("maxfilesexceeded", function(file) {
   if($("#reviewImagesDropzone").hasClass("dz-max-files-reached")){
     $('#imageError').removeClass("hide");
     $("#imageUploadError").html("Maximum 10 number of images can be uploaded");
   }
  });

  imageDropzone.on("removedfile", function(file) {
    var maxFile = imageDropzone.options.maxFiles;
    var totalFiles = $("#reviewImagesDropzone").children(".dz-preview").length
     //console.log(maxFile)
     //console.log(totalFiles)
    if(totalFiles<=maxFile){
      $("#imageUploadError").html("");
      $('#imageError').addClass("hide");
    }
  });

  dropzones.push(imageDropzone);
  var videoDropzone = new Dropzone('div#reviewVideosDropzone', {
    url: '/review/',
    autoProcessQueue: false,
    autoDiscover: false,
    uploadMultiple: true,
    parallelUploads: 2,
    maxFiles: 2,
    paramName: "videos",
    addRemoveLinks: true,
    retryChunks: true,
    parallelChunkUploads: true,
    thumbnailWidth : 80,
    thumbnailheight : 80,
    acceptedFiles: 'video/*'
  });

  videoDropzone.on("maxfilesexceeded", function(file) {
    if($("#reviewVideosDropzone").hasClass("dz-max-files-reached")){
      $("#videoUploadError").html("Maximum 2 number of videos can be uploaded");
      $('#videoError').removeClass("hide");
    }
  });
  videoDropzone.on("removedfile", function(file) {
    var maxFile = videoDropzone.options.maxFiles;
    var totalFiles = $("#reviewVideosDropzone").children(".dz-preview").length;
    if(totalFiles<=maxFile){
      $("#videoUploadError").html("");
      $('#videoError').addClass("hide");
    }
  });

  dropzones.push(videoDropzone);

  $('#reviewForm').submit(function(e) {
    e.preventDefault();
    e.stopPropagation();

    resetErrors();

    let reviewForm = document.getElementById('reviewForm');
    let reviewFormData = new FormData(reviewForm);

    if(isValid(reviewFormData)){
      $("#spinnerModal").modal({
        backdrop: 'static',
        keyboard: false
      });

      //let reviewForm = document.getElementById('reviewForm');
      //let reviewFormData = new FormData(reviewForm);
      dropzones.forEach(dropzone => {
        let  { paramName }  = dropzone.options;
        dropzone.files.forEach((file, i) => {
          reviewFormData.append(paramName + '[' + i + ']', file);
        })
      });
      reviewFormData.append('route_id', route.routeId());
      reviewFormData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

      $.ajax({
            url: '/review/',
            method: 'POST',
            data: reviewFormData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data) {
              $('#spinnerModal').modal('toggle');
              if(!data.is_title_spam && !data.is_comment_spam){
                $("#reviews_count").html(data.total_reviews);
                reset();
              } else {
                if(data.is_title_spam){
                  $('#titleError').removeClass("hide");
                  $("#titleError").html("Spam detected in this field");
                  scrollTo('#title');
                }
                if(data.is_comment_spam){
                  $('#commentsError').removeClass("hide");
                  $("#commentsError").html("Spam detected in this field");
                  scrollTo('#title');
                }
              }
            }
        });
      }
  });
  $('#cancelButton').on('click', function(e){
    reset();
  })

  var totalImages = function(){
    var totalImageFiles = $("#reviewImagesDropzone").children(".dz-preview").length;
    return totalImageFiles;
  }

  var totalVideos = function(){
    var totalVideoFiles = $("#reviewVideosDropzone").children(".dz-preview").length;
    return totalVideoFiles;
  }

  var isValid = function(reviewFormData){
    //var isEmptyComments = $('#reviewComments').val()=='';
    var isFormValid = true;
    var scrollToSection="";

    if( $('#reviewComments').val()=='' && totalImages() == 0 && totalVideos() == 0){
      $("#reviewFormError").html("Please provide your comments or upload photos/videos to submit a review.");
      $('#formError').removeClass("hide");
      isFormValid = false;
      return isFormValid;
    }
    /*if( $('#reviewRating').val()==''){
      $("#ratingError").html("Please provide rating.");
      $('#ratingError').removeClass("hide");
      scrollToSection = '#rating';
      isFormValid = false;
    }*/
    if( reviewFormData.get('reviewRating')==null){
      $("#ratingError").html("Please provide rating.");
      $('#ratingError').removeClass("hide");
      scrollToSection = '#rating';
      isFormValid = false;
    }

    if(totalImages() > imageDropzone.options.maxFiles) {
      $('#imageError').removeClass("hide");
      $("#imageUploadError").html("Maximum 10 number of images can be uploaded");
      if(scrollToSection =="") {
        scrollToSection = '#reviewImagesDropzone';
      }
      isFormValid = false;
    }
    if(totalVideos() > videoDropzone.options.maxFiles) {
      $("#videoUploadError").html("Maximum 2 number of videos can be uploaded");
      $('#videoError').removeClass("hide");
      if(scrollToSection =="") {
        scrollToSection = '#reviewVideosDropzone';
      }
      isFormValid = false;
    }
    if(scrollToSection !="") {
      scrollTo(scrollToSection)
    }
    return isFormValid;

  }
  var reset= function(){
    reviewForm.reset();
    resetErrors();

    dropzones.forEach(dropzone => {
      dropzone.removeAllFiles();
    });

    $("#writeReviewPanel").addClass("hide");
    $("#reviewListPanel").removeClass("hide");

    scrollTo('#reviewListPanel');
  }

  var resetErrors = function(){
    $("#reviewFormError").html("");
    $('#formError').addClass("hide");
    $("#imageUploadError").html("");
    $('#imageError').addClass("hide");
    $("#videoUploadError").html("");
    $('#videoError').addClass("hide");
    /*$("#reviewFormError").html("");
    $('#formError').addClass("hide");*/
    $('#titleError').addClass("hide");
    $("#titleError").html("");
    $('#commentsError').addClass("hide");
    $("#commentsError").html("");
    $("#ratingError").html("");
    $('#ratingError').addClass("hide");

  }

  var scrollTo = function(section){
    $("html, body").animate({
      scrollTop: $(section).offset().top
    });
  }

})();
