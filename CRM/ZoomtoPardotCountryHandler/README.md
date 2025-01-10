
# Zoom to Pardot Country and State Mapping

This JavaScript script is designed for use with **Zapier** to automate the mapping of country and state abbreviations from **Zoom** webinar registration data to full names compatible with **Pardot**.

---

## Features

- **Country Mapping**: Converts two-letter country abbreviations (e.g., `US`) to full names (e.g., `United States`).
- **State Mapping**: Converts US state, Canadian province, and other regional abbreviations to full names.
- **Fallback Handling**: If no mapping is found, the original abbreviation is returned.
- **Customizable**: Extend or modify the `countryMap` and `stateMap` as required.

---

## Requirements

- **Zapier** account.
- Zoom and Pardot integration setup in Zapier.
- Webinar registration data containing `countryAbbr` and `stateAbbr`.

---

## Setup Instructions

### 1. Create a Zap in Zapier

1. **Trigger**: Set the Zap trigger to **Zoom Webinar Registration Created**.
2. **Action**: Use **Code by Zapier** and select **Run JavaScript**.

### 2. Configure the JavaScript Action

1. **Paste the Script**: Copy and paste the provided JavaScript into the **Code by Zapier** editor.
2. **Input Fields**: Ensure the following input fields are provided:
   - `countryAbbr`: The two-letter country code.
   - `stateAbbr`: The abbreviation for the state, province, or region.

3. **Output Fields**: The script will output:
   - `fullCountryName`: Full name of the country.
   - `fullStateName`: Full name of the state or region.

---

## Example

### Input
```json
{
  "countryAbbr": "US",
  "stateAbbr": "NY"
}
```

### Output
```json
{
  "fullCountryName": "United States",
  "fullStateName": "New York"
}
```

---

## Customization

### Adding New Mappings

1. **Country Mapping**: Add or modify entries in the `countryMap` object:
   ```javascript
   const countryMap = {
       "XX": "Example Country"
   };
   ```

2. **State Mapping**: Add or modify entries in the `stateMap` object:
   ```javascript
   const stateMap = {
       "XX": "Example State"
   };
   ```

---

## Testing

1. **Run a Test Zap**: Ensure that the script correctly maps country and state abbreviations.
2. **Verify Output**: Check that the `fullCountryName` and `fullStateName` fields contain the expected values.

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this script.

---

## Support

For assistance, contact your technical team or refer to Zapier’s support documentation.
