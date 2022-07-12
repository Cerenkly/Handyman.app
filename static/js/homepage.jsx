
function HandymanResult(props) {
    return (
      <div className="card">
        <a href={`/search_result/${props.id}`}>
          <li> Name: {props.name} </li>
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
    } else {
      alert("Geocode was not successful for the following reason: " + status);
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
      else {
        alert("Geocode was not successful for the following reason: " + status);
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
                addYelpMarker([...results, ...result]);
                setResults(results => [...results, ...result]);
            });
        fetch("/db/search_result", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "service": service }),
        })
            .then((response2) => response2.json())
            .then((result) => {
                console.log("result before getting db", results )
                console.log("combined with db", [...results, ...Object.values(result)])
                //console.log("db businesses", result);

                // *** Try putting this here: codeAddress(window.zipCode, [...results, ...Object.values(result)])
                codeAddress(window.zipCode);
                //console.log(latLon);
                addDBMarker([...results, ...Object.values(result)]);
                setResults(results => [...results, ...Object.values(result)]);
                // console.log(props)
                // updateResults(result);
                //updateDBResults(result2);
                
            });
    }
    //const yelpList = [];
    const resultsList = [];
    for (const x of results) {
        resultsList.push(
            <HandymanResult
                key={x.id}
              name={x.name}
                id={x.id}
            />,
        );
    }
    //console.log("results:", results)
    React.useEffect(() => {
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
    return (
      <React.Fragment>
        <div>
            <h2 className="center">Welcome!</h2>
        </div>
        <div>
            <h2 className="center">Which service do you need today?</h2>
        </div>
        <div className="center">
            {/* <input 
                value={service} 
                onChange={(event) => searchService(event.target.value)}
                className="example-input" 
                type="text" 
                placeholder="E.g. cleaning, painting, moving"
            /> */}
            {/* <button type="button" className="example-button" onClick={searchButton}><i className="fa fa-search"></i></button> */}

            <select className="example-input" name="search" id="search" onChange={(event) => searchService(event.target.value)}>
                <option value={service}>--Please choose a service--</option>
                <option value="cleaning">Cleaning</option>
                <option value="moving">Moving</option>
                <option value="painting">Painting</option>
            </select>
            <input value={zip} className="example-zip" id="zip" name="zip" type="text" pattern="[0-9]*" placeholder="Enter zip code" onChange={(event) => searchZip(event.target.value)}/>
            <button type="button" id="search-button" className="example-button" onClick={searchButton}><i className="fa fa-search"></i></button>

                
        </div>
        <br></br>
        <br></br>
        <br></br>
        <div>{resultsList}</div>
        <div id="homepage"></div>


      </React.Fragment>
    );
}

// function SearchContainer() {
//     const [results, setResultSearch] = React.useState([]);

//     function updateResults(newResults) {
//         const currentResults = [...results];
//         setResultSearch([...currentResults, newResults]);

//     }
//     const res = [];
//     return (
//         <React.Fragment>
//             <Search updateResults={updateResults} />
//         </React.Fragment>
//     );
// }
 
ReactDOM.render(<Search />, document.getElementById('app'));
//ReactDOM.render(<App />, document.getElementById('app'));
//ReactDOM.render(<SearchContainer />, document.getElementById('app'));

