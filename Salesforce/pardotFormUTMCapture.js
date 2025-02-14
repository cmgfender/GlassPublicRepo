<!-- 
  PARDOT UTM CAPTURE SCRIPT - Version 1.0

  INSTRUCTIONS:
  1. In your Pardot form, create hidden fields for each UTM parameter you want to capture:
       - utm_source
       - utm_medium
       - utm_campaign
       - utm_term
       - utm_content
     Make sure each field is set to HIDDEN so your visitors don’t see it.

  2. Copy and paste this script into your landing page or layout template:
       - You can place it directly above the Pardot form embed code (or in the <head>).
       - This script will look for UTM parameters in the page URL (e.g., ?utm_source=google).
       - If found, it will automatically populate the hidden fields in your form.

  3. Test by adding UTM parameters in a query string (e.g., ?utm_source=google&utm_medium=cpc)
     and submitting the form. Verify in Pardot that the correct UTM values appear in the prospect record.

  NOTES:
  - This script uses DOMContentLoaded to ensure the HTML is ready before accessing form fields.
  - If you need to persist UTM parameters across multiple pages, you can enhance this code
    to store the values in sessionStorage or cookies. 
  - Keep the naming of the hidden fields consistent between Pardot and this script (e.g. 
    if the field is called 'utm_source' in Pardot, use [name="utm_source"] here).

  END OF INSTRUCTIONS
-->

<script>
  // Listen for the 'DOMContentLoaded' event so we can safely manipulate the DOM.
  document.addEventListener("DOMContentLoaded", function() {

    /**
     * getParameterByName()
     * 
     * Helper function to retrieve query parameters from the current page URL.
     * Example usage:
     *    var utmSource = getParameterByName('utm_source');
     *
     * @param {string} name - The name of the parameter to retrieve (e.g., 'utm_source').
     * @returns {string|null} - The decoded parameter value if found, otherwise null.
     */
    function getParameterByName(name) {
      // Escape any special characters in 'name'.
      name = name.replace(/[\[\]]/g, "\\$&");

      // Build a regular expression to search for the parameter in the URL.
      var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
      var results = regex.exec(window.location.search);

      // If the parameter isn't in the URL, return null.
      if (!results) return null;

      // If the parameter exists but has no value, return an empty string.
      if (!results[2]) return '';

      // Decode the parameter value and replace any '+' with spaces.
      return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    // Retrieve each UTM parameter from the URL (if present).
    var utmSource   = getParameterByName('utm_source');
    var utmMedium   = getParameterByName('utm_medium');
    var utmCampaign = getParameterByName('utm_campaign');
    var utmTerm     = getParameterByName('utm_term');
    var utmContent  = getParameterByName('utm_content');

    /**
     * setFieldValue()
     *
     * Helper function to find a form field by its 'name' attribute and set its value.
     *
     * @param {string} fieldName  - The name attribute of the input (e.g. "utm_source").
     * @param {string} fieldValue - The value to assign to that input.
     */
    function setFieldValue(fieldName, fieldValue) {
      if (fieldValue) {
        // Look for an input in the DOM with the matching name.
        var field = document.querySelector('[name="' + fieldName + '"]');
        // If it exists, set the value.
        if (field) {
          field.value = fieldValue;
        }
      }
    }

    // Populate the hidden fields in the Pardot form (if they exist on this page).
    // Ensure your Pardot field names match the ones used here.
    setFieldValue('utm_source',   utmSource);
    setFieldValue('utm_medium',   utmMedium);
    setFieldValue('utm_campaign', utmCampaign);
    setFieldValue('utm_term',     utmTerm);
    setFieldValue('utm_content',  utmContent);

    // After this script runs, any UTM parameters found in the URL
    // should be loaded into the hidden fields automatically.
  });
</script>