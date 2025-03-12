window.onload = function () {
    // Get the username from the URL path
    const path = window.location.pathname;
    const username = path.split('/user/')[1];

    // Update the welcome message
    document.getElementById(
      'dashTitle'
    ).textContent = `${username}'s Dashboard`;
    // const profileLink = document.getElementById('user-profile-link');
    // profileLink.href = `/profile/${username}`;
    // profileLink.textContent = `Go to ${username}'s Profile`;
  };

  const city_form = document.getElementById("findCity");

  city_form.addEventListener("submit", (event) => {
      event.preventDefault();
  
      const city_input = document.getElementById("cityInput");
      const city_value = city_input.value.trim();
      const city_name = city_value.replace(" ", "%20");
      if(!city_name) {
          return;
      }
      long_lat_url = "https://nominatim.openstreetmap.org/search?q=" + city_name + "&format=json";
      fetch(long_lat_url)
      .then(response => response.json()) 
      .then(function(response) {
          lat = response[0]["lat"];
          lon = response[0]["lon"];
          weather_url = "https://api.weather.gov/points/" + lat + "," + lon;
          fetch(weather_url)
          .then(response => {
              if (!response.ok) {
                  alert("City outside of US. Please only enter US cities.");
                  throw new Error(`HTTP Error ${response.status}`);
              }
              return response.json();
          })  
          .then(function(data) {
              const forecastUrl = data.properties.forecast;
              fetch(forecastUrl)
              .then(response => response.json())
              .then(function(response) {
                  let current_forecast = response.properties.periods[0];
  
                  const spanSelect = document.querySelector("span");

                  spanSelect.innerHTML = "";

                  const location = document.createElement("p");
                  const weather_condition = document.createElement("p");
                  const temperature = document.createElement("p");
  
                  location.textContent = "Location: " + city_value;
                  weather_condition.textContent = "Weather Condition(s): " + current_forecast["shortForecast"];
                  temperature.textContent = "Temperature: " + current_forecast["temperature"];
  
                  spanSelect.appendChild(location);
                  spanSelect.appendChild(weather_condition);
                  spanSelect.appendChild(temperature);

                  updateWeatherAnimation(current_forecast["shortForecast"]);
              }); 
          });
      });
  });