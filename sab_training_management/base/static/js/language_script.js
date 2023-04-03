$(document).ready(function() {
  // Check for saved language preference in cookie
  var language = getStorage("language");
  if (language) {
    toggleLanguage(language);
  }

  // Language toggle switch
  $("#language-checkbox").change(function() {
    if ($(this).is(":checked")) {
      toggleLanguage("arabic");
    } else {
      toggleLanguage("english");
    }
  });

  // Function to toggle between English and Arabic languages
  function toggleLanguage(language) {
    setStorage("language", language, 365);

    // Toggle language classes on elements
    if (language == "arabic") {
      $(".language-toggle").addClass("language-arabic");
    } else {
      $(".language-toggle").removeClass("language-arabic");
    }

    // Toggle display of English and Arabic elements
    $("p.english").toggle(language == "english");
    $("p.arabic").toggle(language == "arabic");
    $("a.english").toggle(language == "english");
    $("a.arabic").toggle(language == "arabic");
    $("form.english").toggle(language == "english");
    $("form.arabic").toggle(language == "arabic");
  }

  // Function that sets a value in local storage
  function setStorage(name, value) {
    localStorage.setItem(name, JSON.stringify(value));
  }

  // Function to get a value from local storage
  function getStorage(name) {
    var value = localStorage.getItem(name);
    return value && JSON.parse(value);
  }
});