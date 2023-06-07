document.addEventListener("DOMContentLoaded", init);

async function init() {
    document.getElementById("buyNow").addEventListener("click", function() {
        alert("We regret to inform you that we are currently not offering any products for sale. We kindly request you to revisit our platform at a later time.");
      });

      var imageElement = document.getElementById("shade_effect");
      var imageArray = ["/public/images/transparent.jpeg", "/public/images/dim.png", "/public/images/blackout.png"];
      var currentIndex = 0;
      setInterval(function(){
        imageElement.src = imageArray[currentIndex];
        currentIndex = (currentIndex + 1) % imageArray.length;
      }, 1500);

}
