
const postGetPath = (data) => {
    fetch('http://localhost:5000//get-path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': String.valueOf(data.length),
            'Host': 'localhost:5000'
        },
        body: data
    })
        .then(response => response.json())
        .catch(error => console.log(error))

}

export default postGetPath



