$(document).ready(function() {
  // select the edit button
  const editBtn = $('.btn-secondary');

  // add a click event listener to the edit button
  editBtn.click(function() {
    // select all input and select fields inside the form
    const formInputs = $('form :input');

    // iterate over the input fields and enable them
    formInputs.each(function() {
      const input = $(this);
      // update the input field attributes to enable editing and set the value to the placeholder
      input.prop('disabled', false);
      input.val(input.attr('placeholder'));
    });

    // enable the save button and disable the edit button
    $('.btn-success').prop('disabled', false);
    editBtn.prop('disabled', true);

    // enable the dropdowns and set the selected value
    $('#organisation, #job_title').prop('disabled', false);
    $('#organisation option[value="' + $('#organisation').attr('placeholder') + '"]').prop('selected', true);
    $('#job_title option[value="' + $('#job_title').attr('placeholder') + '"]').prop('selected', true);
  });
});
