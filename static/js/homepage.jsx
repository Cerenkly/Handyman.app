
function HandymanResult(props) {
    return (
      <div className="card">
        <a href={`/search_result/${props.id}`}>
            <span>{props.count}. {props.name}</span>
        </a>
      </div>
    );
}


function codeAddress(zipCode) {
  geocoder.geocode( { componentRestrictions: {postalCode: zipCode, country: 'US'}}, function(results, status) {
    //console.log(results);
    if (status == google.maps.GeocoderStatus.OK) {
      //Got result, center the map and put it out there
      basicMap.setCenter(results[0].geometry.location);
      
      // var marker = new google.maps.Marker({
      //     map: map,
      //     position: results[0].geometry.location
      // });
    }
  });
}

function addYelpMarker(markerResults) {
  console.log("This is yelp:", markerResults);


  const markers = [];
  for (const result of Object.values(markerResults)) {
    const coord = {"lat": result.coordinates.latitude, "lng": result.coordinates.longitude}; 
    //console.log(coord);
    markers.push(
      new google.maps.Marker({
        position: coord,
        title: result.name,
        map: basicMap,
        label: {
          fontSize: "8px"
        },
        icon: {
          // custom icon
          url: '/static/img/handyman_background.jpeg',
          scaledSize: {
            width: 30,
            height: 30,
          },
        },
      }),
    );
  }
  for (const marker of markers) {
      const markerInfo = `
        <h1>${marker.title}</h1>
      `;
  
      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200,
      });
  
      marker.addListener('click', () => {
        infoWindow.open(basicMap, marker);
      });
    }
}

function addDBMarker(markerResults) {
  console.log("This is from my db:", markerResults);
  const markers = [];
  for (const result of markerResults) {
    //console.log("zip code:", result.zip_code);
    //const coord = console.log("latLong:", codeAddress2(result.zip_code.toString()));
    //const zipCode = parseInt(result.zip_code);
    //console.log(coord);
    geocoder.geocode( { componentRestrictions: {postalCode: zipCode, country: 'US'}}, function(results, status) {
      console.log(results);
      console.log(status);
      if (status == google.maps.GeocoderStatus.OK) {
        const coord = results[0].geometry.location;
        markers.push(
          new google.maps.Marker({
            position: coord,
            title: result.name,
            map: basicMap,
            icon: {
              // custom icon
              url: '/static/img/handyman_background.jpeg',
              scaledSize: {
                width: 30,
                height: 30,
              },
            },
          }),
        );
      }
    });
    
        
  }

  for (const marker of markers) {
      const markerInfo = `
        <h1>${marker.title}</h1>
      `;
  
      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200,
      });
  
      marker.addListener('click', () => {
        infoWindow.open(basicMap, marker);
      });
    }
}

var geocoder; //To use later
var basicMap; //Your map
function initMap() {
    // Code that works with Google Maps here
    geocoder = new google.maps.Geocoder();
    const sfBayCoords = {
        lat: 37.601773,
        lng: -122.20287,
    };
      
    basicMap = new google.maps.Map(document.querySelector('#maps'), {
        center: sfBayCoords,
        zoom: 11,
    });

    //Locations
    const locations = [
        {
          name: 'Hackbright Academy',
          coords: {
            lat: 37.7887459,
            lng: -122.4115852,
          },
        },
        {
          name: 'Powell Street Station',
          coords: {
            lat: 37.7844605,
            lng: -122.4079702,
          },
        },
        {
          name: 'Montgomery Station',
          coords: {
            lat: 37.7894094,
            lng: -122.4013037,
          },
        },
    ];
    const markers = [];
    for (const location of locations) {
      markers.push(
        new google.maps.Marker({
          position: location.coords,
          title: location.name,
          map: basicMap,
          icon: {
            // custom icon
            url: '/static/img/handyman_background.jpeg',
            scaledSize: {
              width: 30,
              height: 30,
            },
          },
        }),
      );
    }
    for (const marker of markers) {
        const markerInfo = `
          <h1>${marker.title}</h1>
          <p>
            Located at: <code>${marker.position.lat()}</code>,
            <code>${marker.position.lng()}</code>
          </p>
        `;
    
        const infoWindow = new google.maps.InfoWindow({
          content: markerInfo,
          maxWidth: 200,
        });
    
        marker.addListener('click', () => {
          infoWindow.open(basicMap, marker);
        });
      }

      //Styling
      const customStyledMap = new google.maps.StyledMapType([
        {
          featureType: 'water',
          elementType: 'geometry.fill',
          stylers: [{ color: '#ffd1e4' }],
        },
      ]);
  
      //basicMap.mapTypes.set('map_style', customStyledMap);
      //basicMap.setMapTypeId('map_style');

}

function Search() {
    const [service, searchService] = React.useState('');
    const [zip, searchZip] = React.useState('');
    const [results, setResults] = React.useState([]);
    var latLon;
    //const [dbResults, setDBResults] = React.useState([]);
 
    function searchButton() {
        // clear the search
        //basicMap.setCenter(new google.maps.LatLng(-34, 151));
        setResults([])
        //console.log("Results after clearing",results)
        console.log("Service selected:", service);
        fetch("/api/search_result", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "service": service , "zip_code": zip}),
        })
            .then((response) => response.json())
            .then((data) => {
                const result = data.businesses;
                console.log("result before getting API", results );
                console.log("combined with API", [...results, ...Object.values(result)])

                // *** Try putting this here: codeAddress(window.zipCode, [...results, ...result])
                codeAddress(window.zipCode);
                //basicMap.setCenter(latLon);
                //console.log(latLon);
                setResults(results => [...results, ...Object.values(result)]);
                addYelpMarker([...result, ...Object.values(result)]);

            });
        fetch("/db/search_result", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "service": service, "zip_code": zip}),
        })
            .then((response2) => response2.json())
            .then((result) => {
                console.log("result before getting db", results )
                console.log("combined with db", [...results, ...Object.values(result)])
                //console.log("db businesses", result);

                // *** Try putting this here: codeAddress(window.zipCode, [...results, ...Object.values(result)])
                codeAddress(window.zipCode);
                //console.log(latLon);
                setResults(results => [...results, ...Object.values(result)]);
                addDBMarker([...results, ...Object.values(result)]);
                // console.log(props)
                // updateResults(result);
                //updateDBResults(result2);
                
            });
    }
    //const yelpList = [];
    const resultsList = [];
    var count = 0;
    for (const x of results) {
        count = count + 1;
        resultsList.push(
            <HandymanResult
                key={x.id}
              name={x.name}
                id={x.id}
                count={count}
            />,
        );
        
    }
    //console.log("results:", results)
    React.useEffect(() => {
        const element = document.documentElement;
        element.classList.add("mystyle");
        const script = document.createElement('script');
        script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyDKupASm9sKWM4dTPY89rllyFZlVQrwunE&callback=initMap";
        script.async = true;
        document.body.appendChild(script);

        return () => {
          document.body.removeChild(script);
        }
    }, []);
    React.useEffect(() => {
      document.querySelector('#zip').addEventListener('change', function(event) {
        const zipCode = event.target.value;
        console.log(zipCode);
        //codeAddress(zipCode, results);
        window.zipCode = zipCode;
        //console.log("handymans:", resultsList2);
      });
    
      // *** Try taking out the next 5 lines.
      // document.querySelector('#search-button').addEventListener('click', function(event) {
      //   codeAddress(window.zipCode, results);
      //   //console.log("Print", results);
      //   //console.log("clicked", window.zipCode);
      // }); 

    }, [results]);
    
    // const dbList = [];
    // const test = dbResults;
    // for (const y of dbResults)    
    // {
    //     console.log(y)
    //     dbList.push(
    //         <HandymanResult
    //             key={y.id}
    //           name={y.name}
    //             id={y.id}
    //         />,
    //     );
    // }

    //console.log(yelpList)
    console.log("state: results", results);
    return (
      <React.Fragment>
        <div id="carouselExampleInterval" className="carousel slide" data-bs-ride="carousel">
          <div className="carousel-inner carousel-adjust">
            <div className="carousel-item active" data-bs-interval="10000">
              <img src="/static/img/moving5.png" className="d-block w-100" height="500" alt="..."/>
            </div>
            <div className="carousel-item" data-bs-interval="2000">
              <img src="/static/img/cleaning6.jpg" className="d-block w-100" height="500" alt="..."/>
            </div>
            <div className="carousel-item">
              <img src="/static/img/painting2.jpg" className="d-block w-100" height="500" alt="..."/>
            </div>
          </div>
          <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="prev">
            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
            <span className="visually-hidden">Previous</span>
          </button>
          <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="next">
            <span className="carousel-control-next-icon" aria-hidden="true"></span>
            <span className="visually-hidden">Next</span>
          </button>
        </div>
          {/* <div className="my-container">
            <p id="homepage"></p>
            <p className="margin-top-auto">
              <br></br>
              <h1>Welcome!</h1>
              <br></br>
              <h2>Which service do you need today?</h2>
            </p>
          </div> */}
          {/* <div align="center">
            <p><img src="/static/img/handyman_background.jpeg" height="100" width="100"/></p>
            <h1>Welcome!</h1>
          </div>
           <h2>Which service do you need today?</h2> */}
          <div className="container">
            <div className="row">
              <div className="col">
                  <div className="card mb-3 linear-grad welcome-card">
                    <div className="row g-0">
                      <div className="col-md-3">
                        <img src="/static/img/handyman_background.jpeg" className="img-fluid rounded-start" alt="..."/>
                      </div>
                      <div className="col-md-9">
                        <div className="card-body">
                          <h4 className="card-title welcome">Welcome!</h4>
                          <h4 className="card-title align-center">Which service do you need today?</h4>
                          {/* <p class="card-text">Which service do you need today?</p> */}
                          {/* <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> */}
                        </div>
                      </div>
                    </div>
                    <div className="row g-0">
                      <div className="col-md-12 search-bar-width">
                        <div>
                          <select className="example-input" name="search" id="search" onChange={(event) => searchService(event.target.value)}>
                              <option value={service}>--Please choose a service--</option>
                              <option value="cleaning">Cleaning</option>
                              <option value="moving">Moving</option>
                              <option value="painting">Painting</option>
                          </select>
                          <input value={zip} className="example-zip" id="zip" name="zip" type="text" pattern="[0-9]*" placeholder="Enter zip code" onChange={(event) => searchZip(event.target.value)}/>
                          <button type="button" id="search-button" className="example-button" onClick={searchButton}><i className="fa fa-search"></i></button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div>{resultsList}</div>
              </div>
              <div className="col welcome-card card" id="maps"></div>
            </div>
          </div>      



          
          

      </React.Fragment>
    );
}

 
ReactDOM.render(<Search />, document.getElementById('app'));
//ReactDOM.render(<App />, document.getElementById('app'));
//ReactDOM.render(<SearchContainer />, document.getElementById('app'));

