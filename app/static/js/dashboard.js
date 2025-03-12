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

  function updateWeatherAnimation(weatherCondition) {
    const cityAnimation = document.querySelector(".cityInfoAnimation");

    if (!cityAnimation) {
        console.error("Error: cityInfoAnimation div not found!");
        return;
    }

    cityAnimation.className = "cityInfoAnimation";
    cityAnimation.innerHTML = ""; 

    // SUNNY CONDITON //
    if (weatherCondition.toLowerCase().includes("sunny")) {
        cityAnimation.classList.add("sunny");

        let sun = document.createElement("div");
        sun.className = "sun";
        cityAnimation.appendChild(sun);

        let hill1 = document.createElement("div");
        hill1.className = "hill hill1";
        cityAnimation.appendChild(hill1);

        let hill2 = document.createElement("div");
        hill2.className = "hill hill2";
        cityAnimation.appendChild(hill2);

        let hill3 = document.createElement("div");
        hill3.className = "hill hill3";
        cityAnimation.appendChild(hill3);

        let hill4 = document.createElement("div");
        hill4.className = "hill hill4";
        cityAnimation.appendChild(hill4);
    } 

    else if (weatherCondition.toLowerCase().includes("rain")) {
        cityAnimation.classList.add("rainy");

        for (let i = 0; i < 3; i++) {
            let cloud = document.createElement("div");
            cloud.className = "rainy-cloud";
            cloud.style.top = `${30 + i * 30}px`;
            cloud.style.right = `${20 + i * 60}px`;
            cityAnimation.appendChild(cloud);
        }
    
        for (let i = 0; i < 2; i++) {
            let cloud = document.createElement("div");
            cloud.className = "rainy-cloud";
            cloud.style.top = `${50 + i * 30}px`;
            cloud.style.left = `${10 + i * 70}px`;
            cityAnimation.appendChild(cloud);
        }
    
        for (let i = 0; i < 10; i++) {
            let raindrop = document.createElement("div");
            raindrop.className = "raindrop";
            raindrop.style.left = `${Math.random() * 100}%`;
            raindrop.style.animationDelay = `${Math.random()}s`;
            cityAnimation.appendChild(raindrop);
        }
    }
    
    else if (weatherCondition.toLowerCase().includes("cloudy")) {
        cityAnimation.classList.add("cloudy");
        for (let i = 0; i < 2; i++) {
            let cloud = document.createElement("div");
            cloud.className = "cloudy-cloud";
            cloud.style.top = `${20 + i * 20}px`;
            cloud.style.left = `${10 + i * 40}px`;
            cityAnimation.appendChild(cloud);
        }

        for(let i = 0; i < 3; i++) {
            let cloud = document.createElement("div");
            cloud.className = "cloudy-cloud";
            cloud.style.bottom = `${40 + i * 30}px`;
            cloud.style.right = `${30 + i * 80}px`;
            cityAnimation.appendChild(cloud);
        }
    } 
    
    else if (weatherCondition.toLowerCase().includes("clear")) {
        cityAnimation.classList.add("clear");
    
        let sun = document.createElement("div");
        sun.className = "clear-sun";
        cityAnimation.appendChild(sun);
    
        for(let i = 0; i < 2; i++) {
            let cloud = document.createElement("div");
            cloud.className = "clear-cloud";
            cloud.style.top = `${40 + i * 30}px`;
            cloud.style.left = `${30 + i * 80}px`;
            cityAnimation.appendChild(cloud);
        }
    }
}



// const ai_button = document.getElementById("ai_button");
  
// ai_button.addEventListener("click", (event) => {
//   event.preventDefault();


// });