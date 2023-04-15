$(document).ready(function() {
  // Check for saved language preference in cookie
  var language = getStorage("language");
  if (language) {
      toggleLanguage(language);
  }

  // Language toggle switch
  $("#language-checkbox").change(function() {
      if ($(this).is(":checked")) {
          // $(".languages").fadeIn(200);
          toggleLanguage("arabic");
      } else {
          //$(".languages").fadeOut(200);
          toggleLanguage("english");
      }
  });

  // Language dropdown menu
  $(".languages a").click(function() {
      var language = $(this).attr("data-language");
      toggleLanguage(language);
      $(".languages").fadeOut(200);
  });


  function toggleLanguage(language) {
      setStorage("language", language, 365);
      if (language == "arabic") {
          $(".language-toggle").addClass("language-arabic");
      } else {
          $(".language-toggle").removeClass("language-arabic");
      }
      $("div.english").toggle(language == "english");
      $("div.arabic").toggle(language == "arabic");
      $(".english").toggle(language == "english");
      $(".arabic").toggle(language == "arabic");
      $("h1.english").toggle(language == "english");
      $("h1.arabic").toggle(language == "arabic");
      $("p.english").toggle(language == "english");
      $("p.arabic").toggle(language == "arabic");
      $("a.english").toggle(language == "english");
      $("a.arabic").toggle(language == "arabic");
      $("form.english").toggle(language == "english");
      $("form.arabic").toggle(language == "arabic");
  }

  // Set a value in local storage
  function setStorage(name, value) {
      localStorage.setItem(name, JSON.stringify(value));
  }

  // Get a value from local storage
  function getStorage(name) {
      var value = localStorage.getItem(name);
      return value && JSON.parse(value);
  }
});