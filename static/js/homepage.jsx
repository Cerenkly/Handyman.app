function HandymanResult(props) {
    return (
      <div className="card">
        <a href={`/search_result/${props.id}`}>
          <li> Name: {props.name} </li>
        </a>
      </div>
    );
}

function Search(props) {
    const [service, searchService] = React.useState('');
    const [results, setResults] = React.useState([]);
    //const [dbResults, setDBResults] = React.useState([]);

    function searchButton() {
        // clear the search
        setResults([])
        fetch("/api/search_result", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "service": service }),
        })
            .then((response) => response.json())
            .then((data) => {
                const result = data.businesses;
                console.log("result before getting API", results );
                console.log("combined with API", [...results, ...Object.values(result)])
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

            <button type="button" className="example-button" onClick={searchButton}><i className="fa fa-search"></i></button>

                
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

