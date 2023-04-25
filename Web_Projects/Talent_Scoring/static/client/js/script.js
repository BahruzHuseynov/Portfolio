//Shevron rotate for language function

$(".btn-lang").click(function () {
  $(".chevron-language").toggleClass("rotated");
});
$(window).click(function () {
  $(".chevron-language").removeClass("rotated");
});
$(".btn-lang").click(function (event) {
  event.stopPropagation();
});

// Shevron rotate for cabinet function
$(".btn-cabinet").click(function () {
  $(".chevron-cabinet").toggleClass("rotated");
});
$(window).click(function () {
  $(".chevron-cabinet").removeClass("rotated");
});
$(".btn-cabinet").click(function (event) {
  event.stopPropagation();
});

// Function to toggle the bar and click side hide responsive-menu

var $el = $(".menu-bar");
var $ee = $(".navlist-mobile");
var $over = $(".overlay_leftsidebar");
$el.click(function (e) {
  e.stopPropagation();
  $(".navlist-mobile").toggleClass("expand");
  $(".overlay_leftsidebar").toggleClass("overlay-expand");
  $(".body").toggleClass("body-overflow");
});
$over.click(function (e) {
  e.preventDefault();
  console.log("Salam");
  $(".navlist-mobile").removeClass("expand");
  $(".overlay_leftsidebar").removeClass("overlay-expand");
  $(".body").removeClass("body-overflow");
});

// Password eye change for register functions
$(document).ready(function(){
  $("#eye1").on("click", function() {
    var image_1 = $("#eyeImage1");
    var img1_src = "assets/icons/eye.png";
    var img2_src = "assets/icons/close-eye.png";
  
    if (image_1.attr("src") == img1_src) {
  
        image_1.attr("src", img2_src);
      } else {
        image_1.attr("src", img1_src);
      }
  });
  
  const passwordInput = document.querySelector("#password");
  const eye1 = document.querySelector("#eye1");
  
  eye1.addEventListener("click", function(){
  
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
    passwordInput.setAttribute("type", type)
  })
})

  
$(document).ready(function(){
  $("#eye2").on("click", function () {
    var image_2 = $("#eyeImage2");
    var img1_src = "assets/icons/eye.png";
    var img2_src = "assets/icons/close-eye.png";

    if (image_2.attr("src") == img1_src) {
      image_2.attr("src", img2_src);
    } else {
      image_2.attr("src", img1_src);
    }
  });
  const rePasswordInput = document.querySelector("#rePassword");
  const eye2 = document.querySelector("#eye2");

  eye2.addEventListener("click", function () {
    const type2 =
      rePasswordInput.getAttribute("type") === "password" ? "text" : "password";
    rePasswordInput.setAttribute("type", type2);
  });
})
 


// For reset show password
$(document).ready(function(){
  $("#eyereset").on("click", function () {
    var image_3 = $("#eyeImageReset");
    var img1_src = "assets/icons/eye.png";
    var img2_src = "assets/icons/close-eye.png";
  
    if (image_3.attr("src") == img1_src) {
      image_3.attr("src", img2_src);
    } else {
      image_3.attr("src", img1_src);
    }
  });
  
  const resetPasswordInput = document.querySelector("#resetpassword");
  const eyeReset = document.querySelector("#eyereset");
  
  eyeReset.addEventListener("click", function () {
    const type2 =
      resetPasswordInput.getAttribute("type") === "password"
        ? "text"
        : "password";
    resetPasswordInput.setAttribute("type", type2);
  });
})

$(document).ready(function(){
  $("#eyerereset").on("click", function () {
    var image_4 = $("#eyeImagerereset");
    var img1_src = "assets/icons/eye.png";
    var img2_src = "assets/icons/close-eye.png";
  
    if (image_4.attr("src") == img1_src) {
      image_4.attr("src", img2_src);
    } else {
      image_4.attr("src", img1_src);
    }
  });
  
  const reResetPasswordInput = document.querySelector("#reresetpassword");
  const eyereReset = document.querySelector("#eyerereset");
  
  eyereReset.addEventListener("click", function () {
    const type2 =
      reResetPasswordInput.getAttribute("type") === "password"
        ? "text"
        : "password";
    reResetPasswordInput.setAttribute("type", type2);
  });
})

// For login password 
$(document).ready(function(){
  $("#eye-log").on("click", function() {
    var image_3 = $("#eyeImageLog");
    var img3_src = "assets/icons/eye.png";
    var img4_src = "assets/icons/close-eye.png";
      
    if (image_3.attr("src") == img3_src) {
        
        image_3.attr("src", img4_src);
      } else {
        image_3.attr("src", img3_src);
      }
  });
  
  const logPasswordInput = document.querySelector("#logPassword");
  const eyeLog = document.querySelector("#eye-log");
  
  eyeLog.addEventListener("click", function(){
    
    const type3 = logPasswordInput.getAttribute("type") === "password" ? "text" : "password"
    logPasswordInput.setAttribute("type", type3)
  })
})

